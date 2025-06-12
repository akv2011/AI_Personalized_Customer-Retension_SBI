import asyncio
import json
import logging
from typing import Dict, List, Any
import time
import re

# Import both scrapers
from .universal_sbi_scraper import scrape_sbi_product_universal
from .hyper_sbi_scraper import get_smart_swadhan_guidance_sync

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridSBIScraper:
    """Hybrid scraper that switches between real-time scraping and fast simulation"""
    
    def __init__(self):
        self.real_time_keywords = [
            'live'  # Only "live" keyword triggers real-time scraping
        ]
        
    def detect_scraping_mode(self, user_query: str) -> str:
        """Detect if user wants real-time scraping or fast simulation"""
        query_lower = user_query.lower()
        
        # Check for real-time scraping keywords
        for keyword in self.real_time_keywords:
            if keyword in query_lower:
                logger.info(f"Real-time scraping detected for keyword: '{keyword}'")
                return "real_time"
        
        logger.info("Fast simulation mode selected")
        return "simulation"
    
    def get_smart_swadhan_guidance(self, user_query: str = "Guide me to Smart Swadhan Supreme") -> Dict[str, Any]:
        """Main function that routes to appropriate scraping method"""
        
        scraping_mode = self.detect_scraping_mode(user_query)
        
        logger.info(f"Processing query: '{user_query}' with mode: {scraping_mode}")
        
        try:
            if scraping_mode == "real_time":
                return self._get_real_time_guidance(user_query)
            else:
                return self._get_simulation_guidance(user_query)
                
        except Exception as e:
            logger.error(f"Error in hybrid scraper: {e}")
            # Fallback to simulation if real-time fails
            if scraping_mode == "real_time":
                logger.info("Real-time scraping failed, falling back to simulation")
                return self._get_simulation_guidance(user_query)
            
            return {
                "success": False,
                "error": str(e),
                "query": user_query,
                "mode": scraping_mode,
                "timestamp": time.time()
            }
    
    def _get_real_time_guidance(self, user_query: str) -> Dict[str, Any]:
        """Get guidance using real-time web scraping"""
        logger.info("🌐 Starting REAL-TIME web scraping...")
        
        start_time = time.time()
        
        # Use the universal Selenium scraper that can handle any product
        scraping_result = scrape_sbi_product_universal(user_query)
        
        processing_time = time.time() - start_time
        
        # Handle both dict and non-dict responses from scraper
        if isinstance(scraping_result, dict) and scraping_result.get("success"):
            logger.info(f"✅ Real-time scraping completed in {processing_time:.2f} seconds")
            
            # Convert real scraping result to guidance format
            guidance_data = self._convert_real_scraping_to_guidance(scraping_result)
            
            return {
                "success": True,
                "mode": "real_time_scraping",
                "guidance": guidance_data,
                "navigation_steps": scraping_result.get("steps", []),
                "product_summary": self._extract_product_summary_from_real_data(scraping_result),
                "processing_time": processing_time,
                "query": user_query,
                "timestamp": time.time(),
                "note": "This data was scraped live from the SBI Life website"
            }
        elif isinstance(scraping_result, dict):
            # Scraper returned dict but with error
            logger.error(f"❌ Real-time scraping failed: {scraping_result.get('error', 'Unknown error')}")
            raise Exception(f"Real-time scraping failed: {scraping_result.get('error', 'Unknown error')}")
        else:
            # Scraper returned unexpected format
            logger.error(f"❌ Real-time scraper returned unexpected format: {type(scraping_result)}")
            raise Exception(f"Real-time scraper returned unexpected format: {type(scraping_result)}")
    
    def _get_simulation_guidance(self, user_query: str) -> Dict[str, Any]:
        """Get guidance using fast simulation"""
        logger.info("⚡ Using FAST simulation mode...")
        
        start_time = time.time()
        
        # Use the AI simulation scraper
        simulation_result = get_smart_swadhan_guidance_sync(user_query)
        
        processing_time = time.time() - start_time
        
        if simulation_result.get("success"):
            logger.info(f"✅ Simulation completed in {processing_time:.2f} seconds")
            
            return {
                "success": True,
                "mode": "fast_simulation",
                "guidance": simulation_result.get("guidance"),
                "navigation_steps": simulation_result.get("navigation_data", {}).get("navigation_steps", []),
                "product_summary": simulation_result.get("guidance", {}).get("product_summary", ""),
                "processing_time": processing_time,
                "query": user_query,
                "timestamp": time.time(),
                "note": "This is an AI-powered simulation based on SBI Life website structure"
            }
        else:
            logger.error(f"❌ Simulation failed: {simulation_result.get('error')}")
            raise Exception(f"Simulation failed: {simulation_result.get('error')}")
    
    def _convert_real_scraping_to_guidance(self, scraping_result: Dict[str, Any]) -> Dict[str, Any]:
        """Convert real scraping result to guidance format"""
        steps = scraping_result.get("steps", [])
        
        guidance_steps = []
        for i, step in enumerate(steps):
            # Ensure step is a dictionary
            if not isinstance(step, dict):
                logger.warning(f"Step {i} is not a dictionary: {type(step)}")
                continue
                
            # Safely extract elements, ensuring it's a dict
            elements = step.get("elements", {})
            if not isinstance(elements, dict):
                elements = {}
                
            guidance_step = {
                "step_number": step.get("step", i + 1),
                "title": step.get("description", f"Step {i + 1}"),
                "description": step.get("description", ""),
                "url": step.get("url", ""),
                "visual_cues": self._extract_visual_cues_from_elements(elements),
                "screenshot_available": step.get("screenshot") is not None,
                "chatbot_message": f"Step {i + 1}: {step.get('description', 'Navigation step')}"
            }
            guidance_steps.append(guidance_step)
        
        return {
            "success": True,
            "guidance_steps": guidance_steps,
            "total_steps": len(guidance_steps),
            "final_product_data": scraping_result.get("final_product_info", {}),
            "recommended_actions": [
                "Calculate Premium for personalized quote",
                "Download Brochure for detailed information",
                "Talk to Advisor for consultation",
                "Buy Online for immediate purchase"
            ]
        }
    
    def _extract_visual_cues_from_elements(self, elements: Dict[str, Any]) -> List[str]:
        """Extract visual cues from scraped page elements"""
        visual_cues = []
        
        # Ensure elements is a dictionary
        if not isinstance(elements, dict):
            logger.warning(f"Elements is not a dictionary: {type(elements)}")
            return ["Visual elements could not be processed"]
        
        # Add navigation links
        nav_links = elements.get("navigation_links", [])
        if isinstance(nav_links, list):
            for link in nav_links[:5]:  # Limit to first 5
                if isinstance(link, dict) and link.get("text"):
                    visual_cues.append(f"Navigation: {link['text']}")
        
        # Add buttons
        buttons = elements.get("buttons", [])
        if isinstance(buttons, list):
            for button in buttons[:3]:  # Limit to first 3
                if isinstance(button, dict) and button.get("text"):
                    visual_cues.append(f"Button: {button['text']}")
                elif isinstance(button, str) and button:
                    visual_cues.append(f"Button: {button}")
        
        # Add headings
        headings = elements.get("headings", [])
        if isinstance(headings, list):
            for heading in headings[:3]:  # Limit to first 3
                if isinstance(heading, str) and heading:
                    visual_cues.append(f"Heading: {heading}")
        
        return visual_cues[:10] if visual_cues else ["Page elements detected"]  # Limit total visual cues
    
    def _extract_product_summary_from_real_data(self, scraping_result: Dict[str, Any]) -> str:
        """Extract product summary from real scraping data"""
        product_info = scraping_result.get("final_product_info", {})
        product_name = scraping_result.get("product_name", "SBI Life Product")
        
        # Ensure product_info is a dictionary
        if not isinstance(product_info, dict):
            logger.warning(f"Product info is not a dictionary: {type(product_info)}")
            return f"Product information was extracted but could not be processed from the live website for {product_name.title()}."
        
        if not product_info:
            return f"Product information was not fully extracted from the live website for {product_name.title()}."
        
        summary = f"🏆 SBI Life - {product_name.title()} (Live Data)\n\n"
        
        if product_info.get("title"):
            summary += f"📋 Product Title: {product_info['title']}\n"
        
        if product_info.get("uin"):
            summary += f"• UIN: {product_info['uin']}\n"
        
        if product_info.get("description"):
            summary += f"\n📝 Description:\n{product_info['description']}\n"
        
        # Handle key_features safely
        key_features = product_info.get("key_features", [])
        if isinstance(key_features, list) and key_features:
            summary += "\n🎯 Key Features:\n"
            for feature in key_features[:5]:  # Limit to first 5
                if isinstance(feature, str) and feature.strip():
                    summary += f"• {feature}\n"
        
        # Handle benefits safely  
        benefits = product_info.get("benefits", [])
        if isinstance(benefits, list) and benefits:
            summary += "\n🎁 Benefits:\n"
            for benefit in benefits[:5]:  # Limit to first 5
                if isinstance(benefit, str) and benefit.strip():
                    summary += f"• {benefit}\n"
        
        summary += f"\n📅 Data freshness: Scraped live from SBI Life website for {product_name.title()}"
        
        return summary

# Main function for API integration
def get_hybrid_smart_swadhan_guidance(user_query: str = "Guide me to Smart Swadhan Supreme") -> Dict[str, Any]:
    """Main function for hybrid Smart Swadhan guidance"""
    
    try:
        hybrid_scraper = HybridSBIScraper()
        return hybrid_scraper.get_smart_swadhan_guidance(user_query)
        
    except Exception as e:
        logger.error(f"Error in hybrid guidance: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": user_query,
            "timestamp": time.time()
        }

if __name__ == "__main__":
    # Test both modes
    print("=== Testing Simulation Mode ===")
    result1 = get_hybrid_smart_swadhan_guidance("Guide me to Smart Swadhan Supreme")
    print(f"Mode: {result1.get('mode')}")
    print(f"Success: {result1.get('success')}")
    print(f"Processing time: {result1.get('processing_time', 0):.2f}s")
    
    print("\n=== Testing Real-Time Mode ===")
    result2 = get_hybrid_smart_swadhan_guidance("Show me live scrape data for Smart Swadhan Supreme")
    print(f"Mode: {result2.get('mode')}")
    print(f"Success: {result2.get('success')}")
    print(f"Processing time: {result2.get('processing_time', 0):.2f}s")
