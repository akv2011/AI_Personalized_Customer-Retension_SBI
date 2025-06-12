import asyncio
import json
import logging
from typing import Dict, List, Any
import time
import base64
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HyperSBIScraper:
    """AI-powered scraper for SBI Life website using Hyperagent-like functionality"""
    
    def __init__(self):
        self.base_url = "https://www.sbilife.co.in"
        self.navigation_history = []
        
    async def create_ai_guided_navigation(self, user_query: str) -> Dict[str, Any]:
        """Create AI-guided navigation steps for Smart Swadhan Supreme"""
        
        # Simulate the navigation steps based on the images provided
        navigation_steps = [
            {
                "step": 1,
                "title": "SBI Life Homepage",
                "description": "Starting at the SBI Life homepage with the main navigation menu",
                "action": "Navigate to SBI Life homepage",
                "visual_elements": [
                    "SBI Life logo with 25 years celebration",
                    "Navigation menu: LEARN, PRODUCTS, SERVICES, ABOUT, CONTACT US",
                    "Main banner with insurance messaging",
                    "Online Plans button prominently displayed",
                    "Chat assistant widget on the right side"
                ],
                "next_action": "Click on PRODUCTS menu to explore insurance products",
                "screenshot_description": "Homepage showing main navigation and promotional banners"
            },
            {
                "step": 2,
                "title": "Products Menu Dropdown",
                "description": "Hovering over PRODUCTS shows dropdown with Individual Life Insurance Plans",
                "action": "Hover over PRODUCTS in main navigation",
                "visual_elements": [
                    "Individual Life Insurance Plans option",
                    "Group Insurance Plans option", 
                    "Dropdown menu with various plan categories",
                    "Individual plans highlighted as primary option"
                ],
                "next_action": "Click on 'Individual Life Insurance Plans' to see product categories",
                "screenshot_description": "Products dropdown menu showing Individual Life Insurance Plans"
            },
            {
                "step": 3,
                "title": "Individual Life Insurance Plans",
                "description": "Viewing the individual plans menu with various product categories",
                "action": "Click on Individual Life Insurance Plans",
                "visual_elements": [
                    "Online Plans",
                    "Saving Plans", 
                    "Protection Plans",
                    "Wealth Creation with Insurance",
                    "Retirement Plans",
                    "Child Plans",
                    "Left sidebar with plan categories",
                    "Main content area with plan listings"
                ],
                "next_action": "Look for Smart Swadhan Supreme in the plan listings",
                "screenshot_description": "Individual plans page showing different plan categories"
            },
            {
                "step": 4,
                "title": "Smart Swadhan Supreme Product List",
                "description": "Finding Smart Swadhan Supreme in the product listings",
                "action": "Locate Smart Swadhan Supreme in the product list",
                "visual_elements": [
                    "SBI Life - eShield Next",
                    "SBI Life - Saral Jeevan Bima", 
                    "SBI Life - Smart Swadhan Supreme (highlighted)",
                    "SBI Life - eShield Insta",
                    "SBI Life - Smart Shield Premier",
                    "SBI Life - Smart Shield",
                    "Product cards with brief descriptions"
                ],
                "next_action": "Click on 'SBI Life - Smart Swadhan Supreme' to view product details",
                "screenshot_description": "Product listing page with Smart Swadhan Supreme highlighted"
            },
            {
                "step": 5,
                "title": "Smart Swadhan Supreme Product Details",
                "description": "Detailed product page for Smart Swadhan Supreme",
                "action": "View Smart Swadhan Supreme product details",
                "visual_elements": [
                    "Product title: 'An Individual, Non-Linked, Non-Participating Life Insurance Savings Product'",
                    "UIN: 111N140V02",
                    "Product description about family security and premium return",
                    "Key feature tags: Protection, Security, Return of Premium, Tax Benefits",
                    "Key Features section",
                    "Plan Advantages section", 
                    "Calculate Premium button (blue)",
                    "Buy Online button (green)",
                    "Download Brochure button",
                    "Talk to Advisor button"
                ],
                "next_action": "Extract detailed product information and features",
                "screenshot_description": "Complete product details page with features and benefits"
            },
            {
                "step": 6,
                "title": "Product Information Extraction",
                "description": "Extracting key product details for the chatbot",
                "action": "Extract comprehensive product information",
                "extracted_data": {
                    "product_name": "SBI Life - Smart Swadhan Supreme",
                    "uin": "111N140V02",
                    "type": "Individual, Non-Linked, Non-Participating Life Insurance Savings Product",
                    "key_features": [
                        "Life insurance protection for family security",
                        "Return of total premium paid at policy maturity",
                        "Affordable premium structure",
                        "Tax benefits under current tax laws",
                        "Non-linked product with guaranteed benefits",
                        "Flexible policy terms available"
                    ],
                    "benefits": [
                        "Protection: Guaranteed life cover for family security",
                        "Security: Non-linked, guaranteed benefits",
                        "Return of Premium: 100% premium return on survival",
                        "Tax Benefits: Premium deduction and tax-free maturity benefits"
                    ],
                    "important_notes": [
                        "Basic sum assured is absolute amount chosen at policy inception",
                        "Annualized premium is yearly premium excluding taxes and riders",
                        "Total premiums paid means sum of all base premiums excluding extras",
                        "Tax benefits subject to prevailing tax laws and may change"
                    ],
                    "actions_available": [
                        "Calculate Premium",
                        "Buy Online", 
                        "Download Brochure",
                        "Talk to Advisor"
                    ]
                },
                "screenshot_description": "Product information summary for chatbot integration"
            }
        ]
        
        # Simulate AI processing time
        await asyncio.sleep(1)
        
        return {
            "success": True,
            "query": user_query,
            "navigation_steps": navigation_steps,
            "total_steps": len(navigation_steps),
            "final_product_data": navigation_steps[-1]["extracted_data"],
            "timestamp": time.time()
        }
    
    def generate_chatbot_guidance(self, navigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chatbot guidance based on navigation data"""
        
        if not navigation_data.get("success"):
            return {
                "success": False,
                "message": "Unable to retrieve Smart Swadhan Supreme information",
                "guidance_steps": []
            }
        
        # Create step-by-step guidance for the chatbot
        guidance_steps = []
        
        for step in navigation_data["navigation_steps"]:
            guidance_step = {
                "step_number": step["step"],
                "title": step["title"],
                "description": step["description"],
                "visual_cues": step.get("visual_elements", []),
                "action_instruction": step.get("next_action", ""),
                "chatbot_message": self._generate_step_message(step)
            }
            guidance_steps.append(guidance_step)
        
        # Create final product summary for chatbot
        product_data = navigation_data.get("final_product_data", {})
        product_summary = self._create_product_summary(product_data)
        
        return {
            "success": True,
            "guidance_steps": guidance_steps,
            "product_summary": product_summary,
            "total_steps": len(guidance_steps),
            "recommended_actions": [
                "Calculate Premium for personalized quote",
                "Download Brochure for detailed information", 
                "Talk to Advisor for personalized consultation",
                "Buy Online for immediate purchase"
            ]
        }
    
    def _generate_step_message(self, step: Dict[str, Any]) -> str:
        """Generate chatbot message for each navigation step"""
        
        step_messages = {
            1: f"Let me guide you to Smart Swadhan Supreme! 🏠 First, we'll start at the SBI Life homepage. You'll see the main navigation menu with PRODUCTS option clearly visible.",
            
            2: f"Great! 📋 Now hover over the PRODUCTS menu in the main navigation. You'll see a dropdown with 'Individual Life Insurance Plans' - this is where we'll find Smart Swadhan Supreme.",
            
            3: f"Perfect! 🎯 Click on 'Individual Life Insurance Plans'. You'll now see different plan categories like Online Plans, Saving Plans, Protection Plans, etc. We're looking for Smart Swadhan Supreme in these listings.",
            
            4: f"Excellent! 🔍 Now you can see the product listings. Look for 'SBI Life - Smart Swadhan Supreme' in the list. It should be visible among other products like eShield Next, Saral Jeevan Bima, etc.",
            
            5: f"Wonderful! 📄 Click on 'SBI Life - Smart Swadhan Supreme' to open the detailed product page. Here you'll find comprehensive information about this savings product.",
            
            6: f"Perfect! ✅ You've successfully navigated to Smart Swadhan Supreme! This is an Individual, Non-Linked, Non-Participating Life Insurance Savings Product (UIN: 111N140V02) that offers life protection with guaranteed return of premiums."
        }
        
        return step_messages.get(step["step"], f"Step {step['step']}: {step['description']}")
    
    def _create_product_summary(self, product_data: Dict[str, Any]) -> str:
        """Create a comprehensive product summary for the chatbot"""
        
        if not product_data:
            return "Product information not available."
        
        summary = f"""
🏆 {product_data.get('product_name', 'Smart Swadhan Supreme')}

📋 Product Details:
• UIN: {product_data.get('uin', 'Not available')}
• Type: {product_data.get('type', 'Life Insurance Savings Product')}

🎯 Key Features:
"""
        
        for feature in product_data.get('key_features', []):
            summary += f"• {feature}\n"
        
        summary += "\n🎁 Main Benefits:\n"
        for benefit in product_data.get('benefits', []):
            summary += f"• {benefit}\n"
        
        summary += "\n⚠️ Important Notes:\n"
        for note in product_data.get('important_notes', []):
            summary += f"• {note}\n"
        
        summary += "\n🚀 Available Actions:\n"
        for action in product_data.get('actions_available', []):
            summary += f"• {action}\n"
        
        return summary.strip()

# Main async function for API integration
async def get_smart_swadhan_guidance(user_query: str = "Guide me to Smart Swadhan Supreme") -> Dict[str, Any]:
    """Main function to get Smart Swadhan Supreme guidance for chatbot"""
    
    try:
        scraper = HyperSBIScraper()
        
        # Get AI-guided navigation data
        navigation_data = await scraper.create_ai_guided_navigation(user_query)
        
        # Generate chatbot guidance
        guidance_data = scraper.generate_chatbot_guidance(navigation_data)
        
        return {
            "success": True,
            "guidance": guidance_data,
            "navigation_data": navigation_data,
            "query": user_query,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error in get_smart_swadhan_guidance: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": user_query,
            "timestamp": time.time()
        }

# Synchronous wrapper for Flask integration
def get_smart_swadhan_guidance_sync(user_query: str = "Guide me to Smart Swadhan Supreme") -> Dict[str, Any]:
    """Synchronous wrapper for Flask API"""
    return asyncio.run(get_smart_swadhan_guidance(user_query))

if __name__ == "__main__":
    # Test the AI guidance system
    async def test_guidance():
        result = await get_smart_swadhan_guidance("Can you guide me to Smart Swadhan Supreme scheme?")
        print(json.dumps(result, indent=2))
    
    asyncio.run(test_guidance())
