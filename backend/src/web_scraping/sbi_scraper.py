import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SBILifeScraper:
    def __init__(self):
        self.base_url = "https://www.sbilife.co.in"
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def navigate_to_smart_swadhan_supreme(self):
        """Navigate through the REAL SBI Life website to Smart Swadhan Supreme page"""
        navigation_steps = []
        
        try:
            # Step 1: Go to main page
            logger.info("Step 1: Navigating to SBI Life homepage")
            self.driver.get(self.base_url)
            time.sleep(5)  # Give more time for page load
            
            # Take screenshot of homepage
            navigation_steps.append({
                "step": 1,
                "description": "SBI Life Homepage",
                "url": self.driver.current_url,
                "screenshot": self.take_screenshot("homepage"),
                "elements": self.extract_page_elements()
            })
            
            # Step 2: Try to find and hover over PRODUCTS menu (real website)
            logger.info("Step 2: Looking for PRODUCTS menu on real website")
            try:
                # Try multiple selectors for the PRODUCTS menu
                products_selectors = [
                    "//a[contains(text(), 'PRODUCTS')]",
                    "//nav//a[contains(text(), 'PRODUCTS')]",
                    "//div[contains(@class, 'nav')]//a[contains(text(), 'PRODUCTS')]",
                    "//ul//a[contains(text(), 'PRODUCTS')]",
                    "//*[contains(text(), 'PRODUCTS') and (name()='a' or name()='li')]"
                ]
                
                products_menu = None
                for selector in products_selectors:
                    try:
                        products_menu = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        logger.info(f"Found PRODUCTS menu with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if products_menu:
                    # Hover over the menu first (many sites require hover)
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(products_menu).perform()
                    time.sleep(2)
                    
                    navigation_steps.append({
                        "step": 2,
                        "description": "PRODUCTS Menu Hovered",
                        "url": self.driver.current_url,
                        "screenshot": self.take_screenshot("products_hover"),
                        "elements": self.extract_page_elements()
                    })
                else:
                    logger.warning("PRODUCTS menu not found with any selector")
                    
            except Exception as e:
                logger.warning(f"Error finding PRODUCTS menu: {e}")
                
            # Step 3: Look for Individual Life Insurance Plans (in dropdown or page)
            logger.info("Step 3: Looking for Individual Life Insurance Plans")
            try:
                individual_selectors = [
                    "//a[contains(text(), 'Individual Life Insurance')]",
                    "//a[contains(text(), 'Individual Life')]",
                    "//a[contains(text(), 'Life Insurance')]",
                    "//*[contains(text(), 'Individual') and contains(text(), 'Life')]//a",
                    "//div[contains(@class, 'dropdown')]//a[contains(text(), 'Individual')]"
                ]
                
                individual_plans = None
                for selector in individual_selectors:
                    try:
                        individual_plans = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        logger.info(f"Found Individual Life Insurance with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if individual_plans:
                    individual_plans.click()
                    time.sleep(3)
                    
                    navigation_steps.append({
                        "step": 3,
                        "description": "Individual Life Insurance Plans",
                        "url": self.driver.current_url,
                        "screenshot": self.take_screenshot("individual_plans"),
                        "elements": self.extract_page_elements()
                    })
                else:
                    logger.warning("Individual Life Insurance Plans not found")
                    
            except Exception as e:
                logger.warning(f"Error finding Individual Life Insurance: {e}")
                
            # Step 4: Look for Smart Swadhan Supreme (try multiple approaches)
            logger.info("Step 4: Looking for Smart Swadhan Supreme")
            try:
                # Try direct search first
                smart_swadhan_selectors = [
                    "//a[contains(text(), 'Smart Swadhan Supreme')]",
                    "//a[contains(text(), 'Smart Swadhan')]",
                    "//*[contains(text(), 'Smart Swadhan')]//a",
                    "//div[contains(text(), 'Smart Swadhan')]",
                    "//*[contains(@href, 'smart-swadhan')]",
                    "//*[contains(@href, 'swadhan')]",
                    "//a[contains(@title, 'Smart Swadhan')]"
                ]
                
                smart_swadhan = None
                for selector in smart_swadhan_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        if elements:
                            smart_swadhan = elements[0]
                            logger.info(f"Found Smart Swadhan with selector: {selector}")
                            break
                    except:
                        continue
                
                if smart_swadhan:
                    # Try to click if it's clickable
                    try:
                        smart_swadhan.click()
                        time.sleep(3)
                        
                        # Extract detailed information from the product page
                        product_info = self.extract_smart_swadhan_details()
                        
                        navigation_steps.append({
                            "step": 4,
                            "description": "Smart Swadhan Supreme Product Page",
                            "url": self.driver.current_url,
                            "screenshot": self.take_screenshot("smart_swadhan"),
                            "elements": self.extract_page_elements(),
                            "product_details": product_info
                        })
                    except Exception as e:
                        logger.warning(f"Found Smart Swadhan element but couldn't click: {e}")
                        # Still record that we found it
                        navigation_steps.append({
                            "step": 4,
                            "description": "Smart Swadhan Supreme Found (not clickable)",
                            "url": self.driver.current_url,
                            "screenshot": self.take_screenshot("smart_swadhan_found"),
                            "elements": self.extract_page_elements(),
                            "found_element": smart_swadhan.text if smart_swadhan else "Element found"
                        })
                else:
                    logger.warning("Smart Swadhan Supreme not found with any selector")
                    # Take a screenshot anyway to see what's on the page
                    navigation_steps.append({
                        "step": 4,
                        "description": "Current page content (Smart Swadhan not found)",
                        "url": self.driver.current_url,
                        "screenshot": self.take_screenshot("current_page"),
                        "elements": self.extract_page_elements()
                    })
                    
            except Exception as e:
                logger.warning(f"Error looking for Smart Swadhan Supreme: {e}")
                
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            
        return navigation_steps
    
    def extract_smart_swadhan_details(self):
        """Extract detailed information about Smart Swadhan Supreme"""
        try:
            details = {
                "title": "",
                "uin": "",
                "description": "",
                "key_features": [],
                "benefits": [],
                "important_notes": [],
                "premium_info": {},
                "eligibility": {}
            }
            
            # Extract title
            try:
                title_element = self.driver.find_element(By.TAG_NAME, "h1")
                details["title"] = title_element.text.strip()
            except NoSuchElementException:
                pass
                
            # Extract UIN
            try:
                uin_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'UIN:')]")
                details["uin"] = uin_element.text.strip()
            except NoSuchElementException:
                pass
                
            # Extract description
            try:
                desc_elements = self.driver.find_elements(By.TAG_NAME, "p")
                for elem in desc_elements[:3]:  # First few paragraphs
                    if elem.text.strip():
                        details["description"] += elem.text.strip() + " "
            except NoSuchElementException:
                pass
                
            # Extract key features
            try:
                feature_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'feature') or contains(@class, 'benefit')]//li")
                details["key_features"] = [elem.text.strip() for elem in feature_elements if elem.text.strip()]
            except NoSuchElementException:
                pass
                
            # Extract benefits section
            try:
                benefit_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Protection') or contains(text(), 'Security') or contains(text(), 'Return')]")
                details["benefits"] = [elem.text.strip() for elem in benefit_elements if elem.text.strip()]
            except NoSuchElementException:
                pass
                
            return details
        except Exception as e:
            logger.error(f"Error extracting Smart Swadhan details: {e}")
            return {}
    
    def extract_page_elements(self):
        """Extract key elements from current page"""
        try:
            elements = {
                "title": self.driver.title,
                "url": self.driver.current_url,
                "navigation_links": [],
                "buttons": [],
                "headings": []
            }
            
            # Extract navigation links
            nav_links = self.driver.find_elements(By.XPATH, "//nav//a | //header//a")
            elements["navigation_links"] = [{"text": link.text.strip(), "href": link.get_attribute("href")} 
                                         for link in nav_links if link.text.strip()]
            
            # Extract buttons
            buttons = self.driver.find_elements(By.XPATH, "//button | //a[contains(@class, 'btn')] | //input[@type='button']")
            elements["buttons"] = [{"text": btn.text.strip(), "class": btn.get_attribute("class")} 
                                 for btn in buttons if btn.text.strip()]
            
            # Extract headings
            headings = self.driver.find_elements(By.XPATH, "//h1 | //h2 | //h3")
            elements["headings"] = [h.text.strip() for h in headings if h.text.strip()]
            
            return elements
        except Exception as e:
            logger.error(f"Error extracting page elements: {e}")
            return {}
    
    def take_screenshot(self, name):
        """Take screenshot and return base64 encoded string"""
        try:
            screenshot_path = f"/tmp/sbi_screenshot_{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            # Convert to base64 for easy transmission
            import base64
            with open(screenshot_path, "rb") as img_file:
                screenshot_b64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            return screenshot_b64
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
    
    def get_guided_navigation_data(self):
        """Get complete navigation data for chatbot guidance"""
        logger.info("Starting guided navigation to Smart Swadhan Supreme")
        
        navigation_data = {
            "success": False,
            "steps": [],
            "final_product_info": {},
            "error": None
        }
        
        try:
            steps = self.navigate_to_smart_swadhan_supreme()
            navigation_data["steps"] = steps
            navigation_data["success"] = len(steps) > 0
            
            # Get final product info if we reached the product page
            if steps and "product_details" in steps[-1]:
                navigation_data["final_product_info"] = steps[-1]["product_details"]
                
        except Exception as e:
            navigation_data["error"] = str(e)
            logger.error(f"Error in guided navigation: {e}")
        
        return navigation_data
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser driver closed")

# Standalone function for easy API integration
def scrape_sbi_smart_swadhan():
    """Main function to scrape SBI Life Smart Swadhan Supreme information"""
    scraper = None
    try:
        scraper = SBILifeScraper()
        return scraper.get_guided_navigation_data()
    except Exception as e:
        logger.error(f"Error in scrape_sbi_smart_swadhan: {e}")
        return {
            "success": False,
            "steps": [],
            "final_product_info": {},
            "error": str(e)
        }
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    # Test the scraper
    result = scrape_sbi_smart_swadhan()
    print(json.dumps(result, indent=2))
