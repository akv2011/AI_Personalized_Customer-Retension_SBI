import PyPDF2
import io
from langchain.text_splitter import RecursiveCharacterTextSplitter # Import the splitter

def extract_text_from_pdf(pdf_file_path: str) -> list[str]: # Changed return type hint
    """Extracts text content from a PDF file and splits it into chunks.

    Args:
        pdf_file_path: The path to the PDF file.

    Returns:
        A list of text chunks, or an empty list if extraction or chunking fails.
    """
    full_text = ""
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"Reading {num_pages} pages from PDF: {pdf_file_path}")
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n" # Add newline between pages
        print(f"Successfully extracted text ({len(full_text)} characters) from: {pdf_file_path}")

        if not full_text.strip():
            print("Extracted text is empty.")
            return []

        # Initialize the text splitter
        # Adjust chunk_size and chunk_overlap as needed for your embedding model and desired granularity
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, # Example size, adjust based on token limits and context needs
            chunk_overlap=200, # Overlap helps maintain context between chunks
            length_function=len,
            add_start_index=True, # Optional: adds start index to metadata if splitter supports it
        )

        # Split the text into chunks
        text_chunks = text_splitter.split_text(full_text.strip())
        print(f"Split text into {len(text_chunks)} chunks.")

        return text_chunks

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_file_path}")
        return []
    except Exception as e:
        print(f"Error extracting or chunking text from PDF {pdf_file_path}: {e}")
        return []

# Example usage (optional - can be run directly if needed)
if __name__ == '__main__':
    # Create a dummy PDF for testing if you don't have one
    # (Requires reportlab: pip install reportlab)
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        dummy_pdf_path = "dummy_test.pdf"
        c = canvas.Canvas(dummy_pdf_path, pagesize=letter)
        c.drawString(100, 750, "This is page 1 of the test PDF.")
        c.showPage()
        c.drawString(100, 750, "This is page 2. It contains some text.")
        c.save()
        print(f"Created dummy PDF: {dummy_pdf_path}")

        extracted_content = extract_text_from_pdf(dummy_pdf_path)

        if extracted_content:
            print("\n--- Extracted Text Chunks ---")
            for i, chunk in enumerate(extracted_content):
                print(f"Chunk {i+1}: {chunk}")
            print("-----------------------------")
        else:
            print("\nFailed to extract text from the dummy PDF.")

        # Clean up the dummy file
        import os
        os.remove(dummy_pdf_path)
        print(f"Removed dummy PDF: {dummy_pdf_path}")

    except ImportError:
        print("\nNote: reportlab is not installed. Skipping dummy PDF creation and test.")
        print("To run the example, install it: pip install reportlab")
    except Exception as e:
        print(f"An error occurred during the example: {e}")
