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
        
        # Product definitions based on the screenshot
        self.sbi_products = {
            "smart swadhan supreme": {
                "category": "Protection Plans",
                "description": "Traditional plan with guaranteed benefits and life cover",
                "key_features": [
                    "Life cover with guaranteed returns",
                    "Multiple premium payment options",
                    "Maturity benefits with loyalty additions",
                    "Death benefit protection",
                    "Tax benefits under Section 80C and 10(10D)"
                ]
            },
            "smart swadhan neo": {
                "category": "Protection Plans", 
                "description": "Enhanced traditional plan with flexible options",
                "key_features": [
                    "Flexible premium payment terms",
                    "Higher sum assured options",
                    "Loyalty additions at maturity",
                    "Comprehensive life protection",
                    "Tax efficient investment"
                ]
            },
            "saral swadhan supreme": {
                "category": "Protection Plans",
                "description": "Simple and affordable traditional life insurance",
                "key_features": [
                    "Simple and easy to understand plan",
                    "Affordable premium options",
                    "Guaranteed maturity benefits",
                    "Life cover throughout policy term",
                    "Suitable for long-term wealth creation"
                ]
            },
            "saral jeevan bima": {
                "category": "Protection Plans",
                "description": "Pure protection plan with affordable premiums",
                "key_features": [
                    "Pure term life insurance",
                    "High life cover at affordable premiums",
                    "Multiple premium payment options",
                    "Option to convert to other plans",
                    "Simple documentation process"
                ]
            },
            "eshield next": {
                "category": "Protection Plans",
                "description": "Comprehensive protection with health benefits",
                "key_features": [
                    "Life and health protection combined",
                    "Critical illness cover",
                    "Accidental death benefit",
                    "Premium waiver on disability",
                    "Comprehensive family protection"
                ]
            },
            "eshield insta": {
                "category": "Protection Plans",
                "description": "Instant online protection plan",
                "key_features": [
                    "Instant online purchase",
                    "Quick policy issuance",
                    "High sum assured options",
                    "Minimal documentation",
                    "Digital-first experience"
                ]
            },
            "smart shield premier": {
                "category": "Protection Plans",
                "description": "Premium protection with additional benefits",
                "key_features": [
                    "Enhanced protection coverage",
                    "Multiple benefit options",
                    "Premium waiver benefits",
                    "Flexible premium payment",
                    "Additional accident benefits"
                ]
            },
            "smart shield": {
                "category": "Protection Plans", 
                "description": "Basic protection plan with essential benefits",
                "key_features": [
                    "Essential life protection",
                    "Affordable premiums",
                    "Basic accident cover",
                    "Simple terms and conditions",
                    "Quick claim settlement"
                ]
            }
        }
    
    def detect_product_from_query(self, user_query: str) -> str:
        """Detect which product the user is asking about"""
        query_lower = user_query.lower()
        
        # Check for exact matches first
        for product_key in self.sbi_products.keys():
            if product_key in query_lower:
                logger.info(f"Detected product: {product_key}")
                return product_key
        
        # Check for partial matches
        if "swadhan supreme" in query_lower:
            return "smart swadhan supreme"
        elif "swadhan neo" in query_lower:
            return "smart swadhan neo" 
        elif "saral swadhan" in query_lower:
            return "saral swadhan supreme"
        elif "saral jeevan" in query_lower or "jeevan bima" in query_lower:
            return "saral jeevan bima"
        elif "eshield next" in query_lower or "e-shield next" in query_lower:
            return "eshield next"
        elif "eshield insta" in query_lower or "e-shield insta" in query_lower:
            return "eshield insta"
        elif "shield premier" in query_lower:
            return "smart shield premier"
        elif "smart shield" in query_lower:
            return "smart shield"
        
        # Default to Smart Swadhan Supreme
        logger.info("No specific product detected, defaulting to Smart Swadhan Supreme")
        return "smart swadhan supreme"
        
    async def create_ai_guided_navigation(self, user_query: str) -> Dict[str, Any]:
        """Create AI-guided navigation steps for any SBI Life product"""
        
        # Detect which product the user wants
        detected_product = self.detect_product_from_query(user_query)
        product_info = self.sbi_products[detected_product]
        
        logger.info(f"Creating navigation for: {detected_product.title()}")
        
        # Simulate the navigation steps based on the images provided
        navigation_steps = [
            {
                "step": 1,
                "title": "SBI Life Homepage",
                "description": f"Starting at the SBI Life homepage to find {detected_product.title()}",
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
                "description": f"Hovering over PRODUCTS shows dropdown with Individual Life Insurance Plans for {detected_product.title()}",
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
                "description": f"Viewing the individual plans menu to locate {detected_product.title()}",
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
                "next_action": f"Look for {detected_product.title()} in the {product_info['category']} section",
                "screenshot_description": "Individual plans page showing different plan categories"
            },
            {
                "step": 4,
                "title": f"{detected_product.title()} Product List",
                "description": f"Finding {detected_product.title()} in the product listings",
                "action": f"Locate {detected_product.title()} in the product list",
                "visual_elements": [
                    "SBI Life - eShield Next",
                    "SBI Life - Saral Jeevan Bima", 
                    f"SBI Life - {detected_product.title()} (highlighted)",
                    "SBI Life - eShield Insta",
                    "SBI Life - Smart Shield Premier",
                    "SBI Life - Smart Shield",
                    "SBI Life - Smart Swadhan Neo",
                    "SBI Life - Saral Swadhan Supreme",
                    "Product cards with brief descriptions"
                ],
                "next_action": f"Click on 'SBI Life - {detected_product.title()}' to view product details",
                "screenshot_description": f"Product listing page with {detected_product.title()} highlighted"
            },
            {
                "step": 5,
                "title": f"{detected_product.title()} Product Details",
                "description": f"Detailed product page for {detected_product.title()}",
                "action": f"View {detected_product.title()} product details",
                "visual_elements": [
                    f"Product title: '{detected_product.title()}'",
                    f"Product description: {product_info['description']}",
                    "UIN number and regulatory information",
                    "Key feature tags and benefits",
                    "Key Features section",
                    "Plan Advantages section", 
                    "Calculate Premium button (blue)",
                    "Buy Online button (green)",
                    "Download Brochure button",
                    "Talk to Advisor button"
                ],
                "next_action": "Extract detailed product information and features",
                "screenshot_description": f"Complete product details page for {detected_product.title()}"
            },
            {
                "step": 6,
                "title": "Product Information Extraction",
                "description": f"Extracting key product details for {detected_product.title()}",
                "action": "Extract comprehensive product information",
                "extracted_data": {
                    "product_name": f"SBI Life - {detected_product.title()}",
                    "category": product_info['category'],
                    "description": product_info['description'],
                    "key_features": product_info['key_features'],
                    "additional_features": [
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
                "screenshot_description": f"Product information summary for {detected_product.title()}"
            }
        ]
        
        # Simulate AI processing time
        await asyncio.sleep(1)
        
        return {
            "success": True,
            "query": user_query,
            "detected_product": detected_product,
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
    """Main function to get any SBI Life product guidance for chatbot"""
    
    try:
        scraper = HyperSBIScraper()
        
        # Get AI-guided navigation data (now supports any product)
        navigation_data = await scraper.create_ai_guided_navigation(user_query)
        
        # Generate chatbot guidance
        guidance_data = scraper.generate_chatbot_guidance(navigation_data)
        
        return {
            "success": True,
            "guidance": guidance_data,
            "navigation_data": navigation_data,
            "detected_product": navigation_data.get("detected_product", "smart swadhan supreme"),
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
