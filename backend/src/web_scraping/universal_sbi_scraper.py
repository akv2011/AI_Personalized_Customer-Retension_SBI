import logging
import time
from typing import Dict, Any, List
from .enhanced_sbi_scraper import EnhancedSBIScraper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversalSBIScraper(EnhancedSBIScraper):
    """Universal scraper that can find any SBI Life product"""
    
    def __init__(self):
        super().__init__()
        
        # Product mapping based on your screenshot
        self.sbi_products = {
            "smart swadhan supreme": {
                "selectors": [
                    "//a[contains(text(), 'Smart Swadhan Supreme')]",
                    "//*[contains(text(), 'Smart Swadhan Supreme')]",
                    "//*[contains(@href, 'smart-swadhan-supreme')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/traditional/smart-swadhan-supreme",
                    "/smart-swadhan-supreme",
                    "/products/smart-swadhan-supreme"
                ]
            },
            "smart swadhan neo": {
                "selectors": [
                    "//a[contains(text(), 'Smart Swadhan Neo')]",
                    "//*[contains(text(), 'Smart Swadhan Neo')]",
                    "//*[contains(@href, 'smart-swadhan-neo')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/traditional/smart-swadhan-neo",
                    "/smart-swadhan-neo",
                    "/products/smart-swadhan-neo"
                ]
            },
            "saral swadhan supreme": {
                "selectors": [
                    "//a[contains(text(), 'Saral Swadhan Supreme')]",
                    "//*[contains(text(), 'Saral Swadhan Supreme')]",
                    "//*[contains(@href, 'saral-swadhan-supreme')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/traditional/saral-swadhan-supreme",
                    "/saral-swadhan-supreme",
                    "/products/saral-swadhan-supreme"
                ]
            },
            "saral jeevan bima": {
                "selectors": [
                    "//a[contains(text(), 'Saral Jeevan Bima')]",
                    "//*[contains(text(), 'Saral Jeevan Bima')]",
                    "//*[contains(@href, 'saral-jeevan-bima')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/traditional/saral-jeevan-bima",
                    "/en/individual-life-insurance/protection-plans/saral-jeevan-bima",
                    "/saral-jeevan-bima",
                    "/products/saral-jeevan-bima"
                ]
            },
            "eshield next": {
                "selectors": [
                    "//a[contains(text(), 'eShield Next')]",
                    "//*[contains(text(), 'eShield Next')]",
                    "//*[contains(@href, 'eshield-next')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/protection-plans/eshield-next",
                    "/eshield-next",
                    "/products/eshield-next"
                ]
            },
            "eshield insta": {
                "selectors": [
                    "//a[contains(text(), 'eShield Insta')]",
                    "//*[contains(text(), 'eShield Insta')]",
                    "//*[contains(@href, 'eshield-insta')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/protection-plans/eshield-insta",
                    "/eshield-insta",
                    "/products/eshield-insta"
                ]
            },
            "smart shield premier": {
                "selectors": [
                    "//a[contains(text(), 'Smart Shield Premier')]",
                    "//*[contains(text(), 'Smart Shield Premier')]",
                    "//*[contains(@href, 'smart-shield-premier')]"
                ],
                "urls": [
                    "/en/individual-life-insurance/protection-plans/smart-shield-premier",
                    "/smart-shield-premier",
                    "/products/smart-shield-premier"
                ]
            },
            "smart shield": {
                "selectors": [
                    "//a[contains(text(), 'Smart Shield') and not(contains(text(), 'Premier'))]",
                    "//*[contains(text(), 'Smart Shield') and not(contains(text(), 'Premier'))]",
                    "//*[contains(@href, 'smart-shield') and not(contains(@href, 'premier'))]"
                ],
                "urls": [
                    "/en/individual-life-insurance/protection-plans/smart-shield",
                    "/smart-shield",
                    "/products/smart-shield"
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
        product_keywords = {
            "smart swadhan supreme": ["smart swadhan supreme", "swadhan supreme"],
            "smart swadhan neo": ["smart swadhan neo", "swadhan neo"],
            "saral swadhan supreme": ["saral swadhan supreme", "saral swadhan"],
            "saral jeevan bima": ["saral jeevan", "jeevan bima"],
            "eshield next": ["eshield next", "e-shield next"],
            "eshield insta": ["eshield insta", "e-shield insta"],
            "smart shield premier": ["smart shield premier", "shield premier"],
            "smart shield": ["smart shield"]
        }
        
        for product_key, keywords in product_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    logger.info(f"Detected product via keyword '{keyword}': {product_key}")
                    return product_key
        
        # Default to Smart Swadhan Supreme if nothing detected
        logger.info("No specific product detected, defaulting to Smart Swadhan Supreme")
        return "smart swadhan supreme"
    
    def navigate_to_product(self, product_name: str) -> List[Dict[str, Any]]:
        """Navigate to any SBI Life product"""
        product_key = product_name.lower()
        product_config = self.sbi_products.get(product_key)
        
        if not product_config:
            logger.error(f"Product '{product_name}' not found in configuration")
            return [{
                "step": -1,
                "description": f"Product '{product_name}' not supported",
                "success": False
            }]
        
        navigation_steps = []
        
        try:
            # Step 1: Go to main page
            logger.info(f"Step 1: Navigating to SBI Life homepage for {product_name}")
            self.driver.get(self.base_url)
            self.wait_for_page_load(15)
            
            navigation_steps.append({
                "step": 1,
                "description": f"SBI Life Homepage (Looking for {product_name.title()})",
                "url": self.driver.current_url,
                "screenshot": self.take_screenshot("homepage"),
                "elements": self.extract_page_elements(),
                "success": True
            })
            
            # Step 2: Access PRODUCTS
            logger.info("Step 2: Accessing PRODUCTS menu")
            products_accessed = self.access_products_menu()
            
            navigation_steps.append({
                "step": 2,
                "description": "PRODUCTS Menu",
                "url": self.driver.current_url,
                "screenshot": self.take_screenshot("products_menu"),
                "elements": self.extract_page_elements(),
                "success": products_accessed
            })
            
            # Step 3: Find the specific product
            logger.info(f"Step 3: Looking for {product_name.title()}")
            product_found = self.find_and_click_product(product_config)
            
            if product_found:
                # Extract product details
                product_info = self.extract_product_details(product_name)
                
                navigation_steps.append({
                    "step": 3,
                    "description": f"{product_name.title()} Product Page",
                    "url": self.driver.current_url,
                    "screenshot": self.take_screenshot(f"product_{product_key.replace(' ', '_')}"),
                    "elements": self.extract_page_elements(),
                    "product_details": product_info,
                    "success": True
                })
            else:
                navigation_steps.append({
                    "step": 3,
                    "description": f"{product_name.title()} Not Found",
                    "url": self.driver.current_url,
                    "screenshot": self.take_screenshot("product_not_found"),
                    "elements": self.extract_page_elements(),
                    "success": False
                })
                
        except Exception as e:
            logger.error(f"Navigation error for {product_name}: {e}")
            navigation_steps.append({
                "step": -1,
                "description": f"Navigation Error: {str(e)}",
                "url": self.driver.current_url if self.driver else "Unknown",
                "success": False
            })
            
        return navigation_steps
    
    def access_products_menu(self) -> bool:
        """Access the PRODUCTS menu with multiple strategies"""
        try:
            # Try hover first
            from selenium.webdriver.common.action_chains import ActionChains
            
            products_selectors = [
                "//a[contains(text(), 'PRODUCTS')]",
                "//a[contains(text(), 'Products')]",
                "//*[contains(@class, 'nav')]//a[contains(text(), 'Product')]"
            ]
            
            for selector in products_selectors:
                try:
                    products_element = self.driver.find_element(By.XPATH, selector)
                    actions = ActionChains(self.driver)
                    actions.move_to_element(products_element).perform()
                    time.sleep(3)
                    logger.info(f"Successfully hovered over PRODUCTS with selector: {selector}")
                    return True
                except:
                    continue
            
            logger.warning("Could not access PRODUCTS menu")
            return False
            
        except Exception as e:
            logger.error(f"Error accessing PRODUCTS menu: {e}")
            return False
    
    def find_and_click_product(self, product_config: Dict[str, Any]) -> bool:
        """Find and click on a specific product"""
        try:
            # Try element selectors first
            for selector in product_config["selectors"]:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        element = elements[0]
                        logger.info(f"Found product with selector: {selector}")
                        
                        # Enhanced clicking
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(1)
                        
                        # Try different click methods
                        try:
                            # Method 1: JavaScript click
                            self.driver.execute_script("arguments[0].click();", element)
                            self.wait_for_page_load()
                            return True
                        except:
                            # Method 2: Direct navigation if href available
                            href = element.get_attribute("href")
                            if href:
                                logger.info(f"Navigating directly to: {href}")
                                self.driver.get(href)
                                self.wait_for_page_load()
                                return True
                except:
                    continue
            
            # Fallback: Try direct URL navigation
            logger.info("Element selectors failed, trying direct URLs")
            for url_path in product_config["urls"]:
                try:
                    full_url = self.base_url + url_path
                    logger.info(f"Trying direct navigation to: {full_url}")
                    self.driver.get(full_url)
                    self.wait_for_page_load()
                    
                    # Check if page loaded successfully
                    if "404" not in self.driver.page_source.lower():
                        logger.info(f"Successfully navigated to: {full_url}")
                        return True
                except Exception as e:
                    logger.warning(f"Direct URL {full_url} failed: {e}")
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding product: {e}")
            return False
    
    def extract_product_details(self, product_name: str) -> Dict[str, Any]:
        """Extract details for any product"""
        try:
            details = {
                "title": product_name.title(),
                "uin": "",
                "description": "",
                "key_features": [],
                "benefits": [],
                "buttons": []
            }
            
            # Extract title
            title_selectors = ["h1", "h2", ".product-title", ".main-title"]
            for selector in title_selectors:
                try:
                    from selenium.webdriver.common.by import By
                    title_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if title_element.text.strip():
                        details["title"] = title_element.text.strip()
                        break
                except:
                    continue
            
            # Extract UIN
            try:
                uin_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'UIN') or contains(text(), 'uin')]")
                details["uin"] = uin_element.text.strip()
            except:
                pass
            
            # Extract description
            try:
                desc_elements = self.driver.find_elements(By.TAG_NAME, "p")
                for elem in desc_elements[:3]:
                    text = elem.text.strip()
                    if text and len(text) > 20:
                        details["description"] += text + " "
            except:
                pass
            
            # Extract features
            try:
                list_elements = self.driver.find_elements(By.XPATH, "//ul//li | //ol//li")
                for elem in list_elements[:10]:  # Limit to first 10
                    text = elem.text.strip()
                    if text and len(text) > 10:
                        details["key_features"].append(text)
            except:
                pass
            
            return details
            
        except Exception as e:
            logger.error(f"Error extracting product details: {e}")
            return {"title": product_name.title(), "error": str(e)}

# Main function for universal product guidance
def scrape_sbi_product_universal(user_query: str = "Guide me to Smart Swadhan Supreme"):
    """Universal scraper for any SBI Life product"""
    scraper = None
    try:
        scraper = UniversalSBIScraper()
        
        # Detect which product user wants
        product_name = scraper.detect_product_from_query(user_query)
        logger.info(f"User query: '{user_query}' -> Detected product: '{product_name}'")
        
        # Navigate to the detected product
        steps = scraper.navigate_to_product(product_name)
        
        # Build result
        success_steps = [step for step in steps if step.get("success", False)]
        final_product_info = {}
        
        for step in reversed(steps):
            if "product_details" in step:
                final_product_info = step["product_details"]
                break
        
        return {
            "success": len(success_steps) > 0,
            "product_name": product_name,
            "steps": steps,
            "final_product_info": final_product_info,
            "query": user_query,
            "debug_info": {
                "total_steps": len(steps),
                "successful_steps": len(success_steps)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in universal scraper: {e}")
        return {
            "success": False,
            "product_name": "unknown",
            "steps": [],
            "final_product_info": {},
            "error": str(e),
            "query": user_query
        }
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    # Test with different products
    test_queries = [
        "Guide me to Smart Swadhan Supreme",
        "Show me eShield Next",
        "Find Saral Jeevan Bima",
        "Navigate to Smart Shield Premier"
    ]
    
    for query in test_queries:
        print(f"\n=== Testing: {query} ===")
        result = scrape_sbi_product_universal(query)
        print(f"Product detected: {result['product_name']}")
        print(f"Success: {result['success']}")
        print(f"Steps: {len(result['steps'])}")
## hi