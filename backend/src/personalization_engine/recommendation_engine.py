import json
import os
# Ensure relative imports work correctly
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from vector_database.vector_db_client import VectorDBClient
from embedding_service.embedding_generator import EmbeddingGenerator
from config import config
import pandas as pd
import openai # Keep for now as chat completion uses it
from collections import defaultdict # Import defaultdict for chat history
import re # Import regex for parsing sentiment
import time # Add time for unique IDs

class RecommendationEngine:
    def __init__(self):
        self.vector_db_client = VectorDBClient() # Uses FAISS client
        self.embedding_generator = EmbeddingGenerator() # Now uses Google client
        # Check for Google API key for embeddings
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in config for EmbeddingGenerator.")
        # Keep OpenAI key check for Chat Completion part
        if not config.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set in config. Chat completion might fail.")
        else:
             openai.api_key = config.OPENAI_API_KEY
        # Load system prompt from file
        try:
            with open(config.SYSTEM_PROMPT_PATH, 'r') as f:
                self.system_prompt = f.read().strip()
        except FileNotFoundError:
            print(f"Warning: System prompt file not found at {config.SYSTEM_PROMPT_PATH}. Using default prompt.")
            # Define a default prompt as a fallback
            self.system_prompt = "You are an AI assistant for SBI Life Insurance. Respond helpfully."
        except Exception as e:
            print(f"Error loading system prompt: {e}. Using default prompt.")
            self.system_prompt = "You are an AI assistant for SBI Life Insurance. Respond helpfully."

        # In-memory chat history store (simple implementation)
        # Stores history as {customer_id: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
        self.chat_history = defaultdict(list)

    def clean_json_response(self, response_text):
        """Clean OpenAI response text to ensure valid JSON"""
        # Remove potential markdown code fences
        cleaned = response_text.replace('```json', '').replace('```', '')
        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()
        return cleaned

    def process_user_interaction(self, customer_id, interaction_text, interaction_type="chatbot", user_language='en'): # Add user_language
        """Processes user interaction, stores it in FAISS, gets a personalized response, and updates chat history."""
        conversation_turn_id = f"{customer_id}_{int(pd.Timestamp.now().timestamp())}"
        # Embed interaction text (usually document context)
        embedding = self.embedding_generator.get_embedding(interaction_text, task_type="RETRIEVAL_DOCUMENT") # Specify task type
        if not embedding:
            print(f"Error: Failed to generate embedding for interaction: {interaction_text[:100]}...")
            # Decide how to handle embedding failure - maybe return an error response?
            return {"error": "Failed to process interaction due to embedding failure."}

        metadata = {
            "customer_id": customer_id,
            "conversation_id": "BASIC_CONVO_" + str(int(pd.Timestamp.now().timestamp())), # Basic convo ID for now
            "timestamp": str(pd.Timestamp.now()),
            "speaker": "customer",
            "text": interaction_text,
            "interaction_type": interaction_type,
            "outcome": "message_stored" # Basic outcome for now
        }
        if self.vector_db_client:
            success = self.vector_db_client.upsert_embedding(conversation_turn_id, embedding, metadata)
            if success:
                print(f"Stored interaction in FAISS: {conversation_turn_id}") # Confirmation log (Updated to FAISS)
            else:
                print(f"Failed to store interaction in FAISS: {conversation_turn_id}")
                # Decide how to handle storage failure
                return {"error": "Failed to store interaction."}
        else:
             print("Warning: Vector DB client not initialized. Interaction not stored.")
             # Decide how to handle missing DB client
             return {"error": "Internal server configuration error."}

        # Add user message to chat history BEFORE getting the response
        # Store the original English query for context
        self.chat_history[customer_id].append({"role": "user", "content": interaction_text})

        # Get personalized response, passing user_language
        response_data = self.get_rag_personalized_response(customer_id, interaction_text, user_language)

        # Add assistant response to chat history (use the English response before translation)
        if "response" in response_data and not response_data.get("error"):
             # Store the original English response from the LLM
             assistant_response_english = response_data.get('original_llm_response', response_data["response"]) # Get raw LLM response if available
             self.chat_history[customer_id].append({"role": "assistant", "content": assistant_response_english})
             # Limit history size (e.g., keep last 10 turns = 20 messages)
             self.chat_history[customer_id] = self.chat_history[customer_id][-20:]

        return response_data

    def get_rag_personalized_response(self, customer_id, user_input_text, user_language='en'): # Add user_language
        """Generates a formatted personalized response using RAG with FAISS, chat history, sentiment analysis, and OpenAI."""
        # Generate embedding for the query using the correct task type
        query_embedding = self.embedding_generator.get_embedding(user_input_text, task_type="RETRIEVAL_QUERY") # Specify task type

        # Handle embedding generation failure
        if not query_embedding:
            print("Error generating query embedding.")
            # Return structure consistent with successful response but indicating error
            return {
                "response": "Sorry, I encountered an issue understanding your request.",
                "source": "Embedding Error"
            }

        # Query similar embeddings from FAISS
        query_results = self.vector_db_client.query_similar_embeddings(query_embedding, top_k=5) # Use top_k=5 or more if needed for better context
        print(f"FAISS Query Results: {query_results}") # Updated print statement

        # Handle case when no similar interactions found or query fails
        # Updated check for dictionary format and 'matches' key
        if not query_results or not query_results.get('matches'):
            print("No similar interactions found in FAISS or query failed.")
            # Provide a generic, helpful response
            general_response_content = "I'm here to help you with SBI Life insurance. How can I assist you today?"
            return {
                "response": general_response_content,
                "source": "No Similar Interactions Found"
            }

        # Build context from similar interactions/documents
        # Use the full 'text' field from metadata, which now contains the complete PDF content
        context_parts = []
        # Correctly access the 'matches' key in the dictionary
        for match in query_results['matches']:
            # Correctly access the 'metadata' dictionary within the match dictionary
            metadata = match.get('metadata', {}) # Get the metadata dict safely
            source_text = metadata.get('text', 'No text available') # Get text from metadata
            source_type = metadata.get('source', 'unknown')
            filename = metadata.get('filename', 'N/A') if source_type == 'pdf' else None # Check if filename exists for PDFs

            # Adjust context string based on source type
            if source_type == 'pdf' and filename:
                context_parts.append(f"Context from PDF '{filename}':\n{source_text}")
            elif source_type != 'pdf': # Assuming other sources are interaction texts
                 context_parts.append(f"Similar interaction text: {source_text}")
            else: # Fallback if source is pdf but no filename, or unknown source
                 context_parts.append(f"Relevant context: {source_text}")

        context_string = "\n\n---\n\n".join(context_parts) # Join parts with separator

        # --- OpenAI Prompt ---
        # Retrieve chat history for the customer
        history = self.chat_history.get(customer_id, [])

        prompt_messages = [
            # Use the system prompt loaded during initialization
            {"role": "system", "content": self.system_prompt},
            *history,
            {"role": "system", "content": f"Context from similar past interactions or documents:\n{context_string}" if context_string else "No relevant context found in knowledge base."},
            # Pass the user input in English for sentiment analysis by the LLM
            {"role": "user", "content": f"User query (English for analysis): {user_input_text}\nRespond considering this query and the history, addressing the user in language code: {user_language}."}
        ]

        try:
            print("\n--- Calling OpenAI for RAG response --- ")
            print(f"Target Language: {user_language}")
            # ... existing print statements ...
            openai_response = openai.chat.completions.create(
                model="gpt-4o",
                messages=prompt_messages,
                max_tokens=450 # Slightly more tokens for response + sentiment line
            )
            raw_llm_output = openai_response.choices[0].message.content.strip()
            print(f"Raw OpenAI Output:\n{raw_llm_output}")

            # Parse the response and sentiment
            response_lines = raw_llm_output.split('\n')
            detected_sentiment = "Neutral" # Default sentiment
            main_response = raw_llm_output # Default to full output if parsing fails

            if len(response_lines) > 1 and response_lines[-1].lower().startswith("sentiment:"):
                sentiment_line = response_lines[-1].split(':', 1)
                if len(sentiment_line) > 1:
                    detected_sentiment = sentiment_line[1].strip()
                    # Validate sentiment (optional)
                    if detected_sentiment not in ["Positive", "Negative", "Neutral"]:
                        print(f"Warning: Unexpected sentiment value '{detected_sentiment}'. Defaulting to Neutral.")
                        detected_sentiment = "Neutral"
                main_response = "\n".join(response_lines[:-1]).strip()
            else:
                print("Warning: Could not parse sentiment from LLM response. Defaulting to Neutral.")

            # --- ADD MARKDOWN CLEANING STEP ---
            # Remove bold (**text**)
            cleaned_response = re.sub(r'\*\*(.*?)\*\*', r'\1', main_response)
            # Remove italics (*text* or _text_)
            cleaned_response = re.sub(r'[_*]([^*_]+?)[_*]', r'\1', cleaned_response)
            # Remove inline code (`text`)
            cleaned_response = re.sub(r'`(.*?)`', r'\1', cleaned_response)
            # Standardize list markers (* or - at start of line) to just '-'
            cleaned_response = re.sub(r'^\s*[\*\-]\s+', '- ', cleaned_response, flags=re.MULTILINE)

            print(f"Cleaned Response (No Markdown):\n{cleaned_response}")
            print(f"Detected Sentiment: {detected_sentiment}")

            # Return the cleaned response, sentiment, and original LLM output
            return {
                "response": cleaned_response, # Use the cleaned response
                "sentiment": detected_sentiment,
                "original_llm_response": raw_llm_output, # Store the raw output for history
                "source": "RAG+OpenAI (FAISS + History + Sales Guidance + Sentiment)" # Updated source
            }

        except Exception as e:
            error_message = f"Error calling OpenAI API for RAG response: {e}"
            print(f"ERROR in get_rag_personalized_response (OpenAI call): {error_message}")
            # Return structure consistent with successful response but indicating error
            return {
                "response": "Sorry, I encountered an issue generating a personalized response at this time.",
                "sentiment": "Neutral", # Default sentiment on error
                "source": "RAG+OpenAI Error"
            }


if __name__ == '__main__':
    # Example Usage for testing
    print("\n--- Running RecommendationEngine Example ---")
    if not config.OPENAI_API_KEY or not config.GOOGLE_API_KEY: # Check both keys needed for example
        print("Cannot run example: OPENAI_API_KEY or GOOGLE_API_KEY not set.")
    else:
        try:
            recommender = RecommendationEngine()
            test_customer_id = "TEST_USER_FAISS_002" # Use a new ID for regular tests

            # --- Seeding a Successful Purchase Path Example ---
            print("\n--- Seeding Successful Purchase Path Example ---")
            successful_customer_id = "SUCCESSFUL_USER_ROHAN_001" # Updated ID for clarity
            # --- ENHANCED DETAILED CONVERSATION ---
            successful_conversation = [
                {"role": "assistant", "content": "Hello Rohan, good afternoon! 👋 I noticed you've been exploring options for financial security. Based on your profile (around 38, likely focused on family protection and potentially long-term savings goals) and recent browsing, I believe the SBI Life - Smart Swadhan Supreme plan (UIN: 111N140V02) could be particularly relevant. It uniquely combines life insurance cover with a 100% return of your total paid premiums if you survive the policy term. Would you like a detailed walkthrough of how it could work for you?"},
                {"role": "user", "content": "Return of premium sounds good, but usually those plans are expensive. How does this one work? And who is it for?"},
                {"role": "assistant", "content": "That's a valid point, Rohan. Let's break it down. This plan is designed for individuals like yourself (Age 18-60, looking for cover up to Age 75) who want guaranteed protection for their family and ensure their premiums aren't just an expense if they outlive the policy. It's a Non-Linked, Non-Participating plan, meaning the benefits are guaranteed and not dependent on market performance.\n\n*   **Core Protection:** It provides a guaranteed lump sum ('Sum Assured on Death') to your nominee if the unforeseen happens during the policy term, ensuring your family's financial stability. The death benefit is the highest of: a) Basic Sum Assured chosen, b) 11 times the Annualized Premium, or c) 105% of Total Premiums Paid till death.\n*   **Return of Premium (Maturity Benefit):** This is the key feature you liked. If you survive until the end of the chosen policy term (anywhere from 10 to 30 years), you get back 100% of all the base premiums you've paid over the years, lump sum. It's like getting your money back after the protection period ends.\n*   **Affordability:** While it might be slightly higher than a pure term plan, the 'return of premium' feature provides value back, making it attractive for many. We aim to offer this cover at an affordable cost.\n*   **Tax Benefits:** As per current laws, premiums often qualify for deduction under Sec 80C, and the death/maturity benefit is typically tax-free under Sec 10(10D). It's always best to consult your tax advisor for specifics related to your situation."},
                {"role": "user", "content": "Okay, that makes sense. Let's say I want a ₹1 Crore cover. I'm 38 now. What would the premium be, and what term options do I have?"},
                {"role": "assistant", "content": "Excellent! A ₹1 Crore cover is a popular choice for providing substantial support. For your age (38), you have flexibility:\n\n*   **Policy Term:** You can choose a term from 10 years up to 30 years. A longer term, say 25 or 30 years, would cover you through a significant portion of your working life and family responsibilities. Let's consider a 25-year policy term (covers you till age 63).\n*   **Premium Payment:** You can choose:\n    *   **Regular Pay (RP):** Pay premiums every year for the entire 25-year policy term.\n    *   **Limited Premium Payment Term (LPPT):** Pay for a shorter duration, like 7, 10, or 15 years, but stay covered for the full 25 years. This usually means higher annual premiums but freedom from payments sooner.\n*   **Premium Estimate (Regular Pay):** For a 38-year-old, ₹1 Crore cover, 25-year policy term with *Regular Premium payment*:\n    *   The approximate annual premium would be around **₹30,000** (excluding taxes and any rider premiums). This is an illustrative value.\n    *   You'd pay this amount each year for 25 years. Total Paid ≈ ₹7,50,000.\n    *   Benefit: ₹1 Cr death benefit anytime during 25 years, OR ~₹7,50,000 back at age 63 if you survive."},
                {"role": "user", "content": "What if I miss a payment?"},
                {"role": "assistant", "content": "Good question about practicality. There's a **Grace Period**: 30 days for yearly/half-yearly payments and 15 days for monthly payments. If you pay within this period, the policy continues without interruption. If premiums stop after the grace period (and at least the first full year's premium has been paid), the policy doesn't necessarily lapse immediately. It may acquire a **'Reduced Paid-up' Value**. This means a proportionately reduced death benefit and maturity benefit would still be payable, based on the premiums you have paid. You also have the option to **Revive** the policy within 5 years by paying overdue premiums with interest."},
                {"role": "user", "content": "Okay, that's reassuring. I like the idea of paying for only 15 years (LPPT-15). How much would that cost for the same cover?"},
                {"role": "assistant", "content": "Opting for LPPT-15 (Pay for 15 years, Cover for 25 years) is a great way to manage cash flow later in life. Let's estimate:\n\n*   **Premium Estimate (LPPT-15):** For a 38-year-old, ₹1 Crore cover, 25-year policy term, paying premiums only for the first 15 years:\n    *   The approximate annual premium would be higher, around **₹45,000** (excluding taxes/riders).\n    *   You pay this only for 15 years. Total Paid ≈ ₹6,75,000.\n    *   Benefit: ₹1 Cr death benefit anytime during the full 25 years, OR ~₹6,75,000 back at age 63 if you survive (even though you stopped paying after 15 years).\n*   \"So, you pay more per year, but for 10 fewer years. Does this trade-off look appealing?\""},
                {"role": "user", "content": "Yes, significantly. Finishing payments by age 53 is much better. What about extra protection like for accidents?"},
                {"role": "assistant", "content": "Absolutely essential to consider. You can enhance your cover significantly by adding the **SBI Life - Accident Benefit Rider** (UIN: 111B041V01). This rider offers two main options, and you can choose one or both:\n\n*   **Option A: Accidental Death Benefit (ADB):** Provides an additional lump sum if death occurs specifically due to an accident. The maximum ADB Sum Assured can be substantial (up to ₹2 Crore, but cannot exceed the base policy Sum Assured for APPD, nor 3 times base Sum Assured for ADB, and is subject to underwriting limits). For a ₹1 Cr base policy, you could potentially add ₹1 Cr ADB cover.\n*   **Option B: Accidental Partial Permanent Disability (APPD):** Provides a payout (often a percentage of the rider sum assured) in case of specific permanent disabilities resulting from an accident, like loss of a limb. The maximum APPD Sum Assured is also capped (e.g., ₹1.5 Cr, cannot exceed base sum assured).\n*   \"Given your family responsibilities, adding the **Accidental Death Benefit (ADB)** is highly recommended by many financial advisors for comprehensive protection. The premium for this rider is quite affordable. Would you like me to add an estimated ₹1 Crore ADB rider to your illustration?\""},
                {"role": "user", "content": "Yes, please add the ₹1 Cr ADB rider. Let's see the total cost."},
                {"role": "assistant", "content": "Okay, Rohan. Here's the refined illustration:\n\n*   **Plan:** SBI Life - Smart Swadhan Supreme\n*   **Age:** 38\n*   **Base Sum Assured:** ₹1 Crore\n*   **Policy Term:** 25 Years (Cover till Age 63)\n*   **Premium Payment Term:** 15 Years (Pay till Age 53)\n*   **Rider:** Accidental Death Benefit (ADB) Sum Assured: ₹1 Crore\n*   **Estimated Total Annual Premium:** Approximately **₹52,000** (Base ~₹45k + ADB Rider ~₹7k). Please note: This is indicative and excludes GST. The final premium depends on underwriting assessment.\n*   **Key Benefits Summary:**\n    *   Death (Non-Accidental): ₹1 Crore (or higher based on the formula) payable anytime during 25 years.\n    *   Death (Accidental): ₹1 Crore (Base) + ₹1 Crore (ADB) = Total ₹2 Crore payable.\n    *   Survival till Age 63: ~₹6,75,000 (100% of base premiums paid) returned lump sum.\n*   \"This structure provides strong protection against unforeseen events (doubling the cover for accidental death) while ensuring you get your base premium investment back if you complete the term. How does this complete package look to you?\""},
                {"role": "user", "content": "The total premium is a bit higher than the regular pay option you mentioned earlier. Can you quickly compare the total payout vs total paid for both LPPT-15 and Regular Pay?"},
                {"role": "assistant", "content": "Good point, let's compare:\n\n*   **Regular Pay (Pay for 25 years):**\n    *   Approx. Annual Premium: ₹30,000 (+ Rider, let's say ~₹7k = ₹37,000 total)\n    *   Total Paid over 25 years: ~₹9,25,000\n    *   Maturity Benefit (Return of Base Premium): ~₹7,50,000\n    *   Death Benefit: ₹1 Cr (Non-Accidental) / ₹2 Cr (Accidental)\n*   **LPPT-15 (Pay for 15 years):**\n    *   Approx. Annual Premium: ₹45,000 (+ Rider ~₹7k = ₹52,000 total)\n    *   Total Paid over 15 years: ~₹7,80,000\n    *   Maturity Benefit (Return of Base Premium): ~₹6,75,000\n    *   Death Benefit: ₹1 Cr (Non-Accidental) / ₹2 Cr (Accidental)\n\n\"So with LPPT-15, you pay significantly less overall (~₹1.45 Lakhs less) and finish payments 10 years earlier, though the maturity return is slightly lower because the base premium component was paid over fewer years. Many find the earlier payment freedom and lower total cost outweigh the slightly lower maturity amount. Does this clarify the trade-off?\""},
                {"role": "user", "content": "Yes, that comparison helps. What if I need money urgently and have to stop the policy midway? Is there any surrender value?"},
                {"role": "assistant", "content": "That's an important consideration. Yes, the policy acquires a 'Guaranteed Surrender Value' (GSV) after you have paid premiums for at least the first two consecutive years. There's also a potential 'Special Surrender Value' (SSV), which might be higher than the GSV, depending on SBI Life's assessment at the time.\n\n*   **Guaranteed Surrender Value:** It's calculated as a percentage of the total base premiums paid, plus a percentage of the surrender value of any vested bonuses (though this plan is non-participating, so bonuses aren't typical). The exact percentage depends on the policy year you surrender.\n*   **Special Surrender Value:** This is determined by SBI Life based on prevailing conditions and is often higher than the GSV, but it's not guaranteed upfront.\n\n\"Surrendering a policy, especially early on, usually results in getting back less than the total premiums paid. It's generally advisable to continue the policy for the full term to get the maximum benefits, including the full return of premium at maturity. However, the surrender option provides some liquidity if absolutely necessary. Does knowing this option exists provide some comfort?\""},
                {"role": "user", "content": "That looks comprehensive and the premium seems reasonable for the combined benefit. The 15-year payment is the clincher. I think I'm ready to consider applying."},
                {"role": "assistant", "content": "That's an excellent decision, Rohan! Securing this level of protection with a return benefit is a very prudent step for your family's future. The next step is the online application. It's a secure process:\n\n1.  **Personal & Nominee Details:** We can pre-fill some basics to speed things up.\n2.  **Health Declarations:** You'll need to answer some standard questions about your health and lifestyle honestly (critical for the policy - see Non-Disclosure section in policy docs).\n3.  **KYC Verification:** Standard identity and address verification.\n4.  **Premium Payment:** Secure online payment setup.\n*   \"The whole process usually takes about 20-25 minutes online. Once submitted, it goes for underwriting review. You also get a **30-day Free Look Period** after receiving the policy document to review everything, and you can cancel if needed.\"\n*   \"Shall we begin the secure application process now? I can guide you step-by-step.\""},
                {"role": "user", "content": "Yes, let's do it."},
                {"role": "assistant", "content": "Fantastic! Launching the secure application portal within this chat window now. The first section is confirming your personal details... Please verify the information displayed."}
            ]
            # --- END OF ENHANCED CONVERSATION ---

            conversation_id_seed = f"SEED_CONVO_{int(pd.Timestamp.now().timestamp())}"
            for i, turn in enumerate(successful_conversation):
                text_to_embed = turn["content"]
                # Use RETRIEVAL_DOCUMENT type for storing context
                embedding = recommender.embedding_generator.get_embedding(text_to_embed, task_type="RETRIEVAL_DOCUMENT")
                if embedding:
                    # Create a unique ID for each turn, ensuring chronological order if needed later
                    turn_id = f"{successful_customer_id}_{conversation_id_seed}_turn{i:02d}"
                    metadata = {
                        "customer_id": successful_customer_id,
                        "conversation_id": conversation_id_seed,
                        "timestamp": str(pd.Timestamp.now()),
                        "speaker": turn["role"],
                        "text": text_to_embed,
                        "interaction_type": "chatbot_seed",
                        "outcome": "successful_purchase_path" # Mark this as part of a successful path
                    }
                    success = recommender.vector_db_client.upsert_embedding(turn_id, embedding, metadata)
                    if success:
                        print(f"Seeded turn {i} for {successful_customer_id} into FAISS.")
                    else:
                        print(f"Failed to seed turn {i} for {successful_customer_id}.")
                    time.sleep(0.1) # Small delay to ensure distinct timestamps if needed
                else:
                    print(f"Failed to generate embedding for seeding turn {i}.")
            print("--- Seeding Complete ---")

            # --- Regular Testing Starts Here ---
            test_query = "Tell me about term insurance plans"

            print(f"\nProcessing interaction for '{test_customer_id}': '{test_query}'")
            test_result = recommender.process_user_interaction(test_customer_id, test_query)

            print("\n--- Test Result ---")
            # Pretty print the JSON-like dictionary result
            print(json.dumps(test_result, indent=2))
            print("-------------------")

            # Example of querying directly (might require existing data in index)
            print(f"\nDirect RAG query example for {test_customer_id}: '{test_query}'")
            direct_rag_result = recommender.get_rag_personalized_response(test_customer_id, test_query)
            print("\n--- Direct RAG Result ---")
            print(json.dumps(direct_rag_result, indent=2))
            print("-------------------------")

            # Add a test case relevant to the new guidance (using the regular test user)
            print("\n--- Testing Sales Guidance (New User) ---")
            test_query_product = "Tell me about Smart Swadhan Supreme."
            print(f"\nProcessing interaction for '{test_customer_id}': '{test_query_product}'")
            # Use the regular process_user_interaction which includes RAG
            product_test_result = recommender.process_user_interaction(test_customer_id, test_query_product)
            print("\n--- Product Query Result (New User) ---")
            print(json.dumps(product_test_result, indent=2))
            print("---------------------------------------")

            # Add a test case for sentiment (using the regular test user)
            print("\n--- Testing Sentiment (Negative Example) ---")
            test_query_sentiment = "I'm really unhappy with the claim process, it's taking too long!"
            print(f"\nProcessing interaction for '{test_customer_id}': '{test_query_sentiment}'")
            sentiment_test_result = recommender.process_user_interaction(test_customer_id, test_query_sentiment, user_language='en') # Test with English
            print("\n--- Sentiment Query Result ---")
            print(json.dumps(sentiment_test_result, indent=2))
            print("----------------------------")

        except Exception as e:
            print(f"\nError during RecommendationEngine example: {e}")
            import traceback
            traceback.print_exc()
    print("\n--- Example Finished ---")