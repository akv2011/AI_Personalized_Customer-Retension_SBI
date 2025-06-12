import logging
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedSBIScraper:
    """Enhanced scraper specifically designed for the real SBI Life website"""
    
    def __init__(self):
        self.base_url = "https://www.sbilife.co.in"
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with enhanced options for real website"""
        chrome_options = Options()
        # Remove headless for debugging - we want to see what's happening
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Enhanced Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def debug_page_content(self, step_name):
        """Debug helper to log current page content"""
        try:
            logger.info(f"=== DEBUG: {step_name} ===")
            logger.info(f"Current URL: {self.driver.current_url}")
            logger.info(f"Page Title: {self.driver.title}")
            
            # Log all links on the page
            links = self.driver.find_elements(By.TAG_NAME, "a")
            logger.info(f"Found {len(links)} links on page")
            
            # Log navigation-related links
            nav_links = []
            for link in links[:20]:  # First 20 links
                text = link.text.strip()
                href = link.get_attribute("href")
                if text and any(keyword in text.lower() for keyword in ['product', 'insurance', 'life', 'plan', 'swadhan']):
                    nav_links.append(f"Text: '{text}' | Href: {href}")
            
            if nav_links:
                logger.info("Relevant navigation links found:")
                for nav_link in nav_links:
                    logger.info(f"  - {nav_link}")
            else:
                logger.info("No relevant navigation links found")
                
        except Exception as e:
            logger.error(f"Error in debug_page_content: {e}")
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Additional wait for dynamic content
        except TimeoutException:
            logger.warning("Page load timeout, continuing anyway")
    
    def navigate_to_smart_swadhan_supreme(self):
        """Navigate through the REAL SBI Life website with enhanced debugging"""
        navigation_steps = []
        
        try:
            # Step 1: Go to main page
            logger.info("Step 1: Navigating to SBI Life homepage")
            self.driver.get(self.base_url)
            self.wait_for_page_load(15)
            
            self.debug_page_content("Homepage")
            
            navigation_steps.append({
                "step": 1,
                "description": "SBI Life Homepage",
                "url": self.driver.current_url,
                "screenshot": self.take_screenshot("homepage"),
                "elements": self.extract_page_elements(),
                "success": True
            })
            
            # Step 2: Find and interact with PRODUCTS
            logger.info("Step 2: Looking for PRODUCTS menu")
            
            # Try multiple approaches to find PRODUCTS
            products_found = False
            
            # Approach 1: Direct click on PRODUCTS link
            try:
                products_selectors = [
                    "//a[contains(text(), 'PRODUCTS')]",
                    "//a[contains(text(), 'Products')]", 
                    "//a[contains(text(), 'PRODUCT')]",
                    "//*[contains(@class, 'nav')]//a[contains(text(), 'Product')]",
                    "//nav//a[contains(text(), 'Product')]"
                ]
                
                for selector in products_selectors:
                    try:
                        products_link = self.driver.find_element(By.XPATH, selector)
                        logger.info(f"Found PRODUCTS link with selector: {selector}")
                        
                        # Scroll to element and click
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", products_link)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", products_link)
                        self.wait_for_page_load()
                        products_found = True
                        break
                        
                    except NoSuchElementException:
                        continue
                        
                if not products_found:
                    logger.info("Direct PRODUCTS link not found, trying hover approach")
                    
                    # Approach 2: Hover over PRODUCTS
                    hover_selectors = [
                        "//*[contains(text(), 'PRODUCTS')]",
                        "//*[contains(text(), 'Products')]",
                        "//*[contains(@aria-label, 'Product')]"
                    ]
                    
                    for selector in hover_selectors:
                        try:
                            products_element = self.driver.find_element(By.XPATH, selector)
                            actions = ActionChains(self.driver)
                            actions.move_to_element(products_element).perform()
                            time.sleep(3)
                            logger.info(f"Hovered over PRODUCTS element with selector: {selector}")
                            products_found = True
                            break
                            
                        except NoSuchElementException:
                            continue
                
            except Exception as e:
                logger.warning(f"Error finding PRODUCTS: {e}")
            
            if products_found:
                self.debug_page_content("After PRODUCTS interaction")
                navigation_steps.append({
                    "step": 2,
                    "description": "PRODUCTS Menu Accessed",
                    "url": self.driver.current_url,
                    "screenshot": self.take_screenshot("products_menu"),
                    "elements": self.extract_page_elements(),
                    "success": True
                })
            else:
                # Fallback: Try direct URL navigation
                logger.info("Trying direct URL navigation to products page")
                try:
                    products_urls = [
                        f"{self.base_url}/products",
                        f"{self.base_url}/insurance-plans",
                        f"{self.base_url}/life-insurance-plans"
                    ]
                    
                    for url in products_urls:
                        try:
                            self.driver.get(url)
                            self.wait_for_page_load()
                            if "404" not in self.driver.page_source.lower():
                                logger.info(f"Successfully navigated to: {url}")
                                products_found = True
                                break
                        except Exception as e:
                            continue
                            
                except Exception as e:
                    logger.warning(f"Direct URL navigation failed: {e}")
                
                navigation_steps.append({
                    "step": 2,
                    "description": "PRODUCTS Menu (Direct Navigation Attempted)",
                    "url": self.driver.current_url,
                    "screenshot": self.take_screenshot("products_attempt"),
                    "elements": self.extract_page_elements(),
                    "success": products_found
                })
            
            # Step 3: Look for Individual Life Insurance Plans
            logger.info("Step 3: Looking for Individual Life Insurance Plans")
            
            individual_found = False
            individual_selectors = [
                "//a[contains(text(), 'Individual Life Insurance Plans')]",
                "//a[contains(text(), 'Individual Life Insurance')]",
                "//a[contains(text(), 'Individual Plans')]",
                "//*[contains(text(), 'Individual') and contains(text(), 'Life')]",
                "//div[contains(@class, 'dropdown')]//a[contains(text(), 'Individual')]"
            ]
            
            for selector in individual_selectors:
                try:
                    individual_element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logger.info(f"Found Individual Life Insurance with selector: {selector}")
                    individual_element.click()
                    self.wait_for_page_load()
                    individual_found = True
                    break
                except TimeoutException:
                    continue
            
            if individual_found:
                self.debug_page_content("Individual Life Insurance Plans")
                navigation_steps.append({
                    "step": 3,
                    "description": "Individual Life Insurance Plans",
                    "url": self.driver.current_url,
                    "screenshot": self.take_screenshot("individual_plans"),
                    "elements": self.extract_page_elements(),
                    "success": True
                })
            else:
                logger.warning("Individual Life Insurance Plans not found")
                navigation_steps.append({
                    "step": 3,
                    "description": "Individual Life Insurance Plans Not Found",
                    "url": self.driver.current_url,
                    "screenshot": self.take_screenshot("individual_not_found"),
                    "elements": self.extract_page_elements(),
                    "success": False
                })
            
            # Step 4: Look for Smart Swadhan Supreme
            logger.info("Step 4: Looking for Smart Swadhan Supreme")
            
            smart_swadhan_found = False
            smart_swadhan_selectors = [
                "//a[contains(text(), 'Smart Swadhan Supreme')]",
                "//a[contains(text(), 'Smart Swadhan')]",
                "//*[contains(text(), 'Smart Swadhan')]",
                "//div[contains(text(), 'Smart Swadhan')]",
                "//*[contains(@href, 'smart-swadhan')]",
                "//*[contains(@href, 'swadhan')]",
                "//a[contains(@title, 'Smart Swadhan')]",
                "//*[contains(text(), 'Swadhan')]"
            ]
            
            for selector in smart_swadhan_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        smart_swadhan_element = elements[0]
                        logger.info(f"Found Smart Swadhan with selector: {selector}")
                        logger.info(f"Element text: {smart_swadhan_element.text}")
                        
                        # Enhanced clicking approach
                        try:
                            # Method 1: Check if element is directly clickable
                            if smart_swadhan_element.is_enabled() and smart_swadhan_element.is_displayed():
                                # Scroll to element first
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", smart_swadhan_element)
                                time.sleep(1)
                                
                                if smart_swadhan_element.tag_name == 'a':
                                    # For anchor tags, try JavaScript click first
                                    try:
                                        self.driver.execute_script("arguments[0].click();", smart_swadhan_element)
                                        logger.info("JavaScript click successful")
                                    except:
                                        # Fallback to regular click
                                        smart_swadhan_element.click()
                                        logger.info("Regular click successful")
                                else:
                                    # Find parent link if element is not directly clickable
                                    try:
                                        parent_link = smart_swadhan_element.find_element(By.XPATH, "./ancestor-or-self::a")
                                        self.driver.execute_script("arguments[0].click();", parent_link)
                                        logger.info("Parent link JavaScript click successful")
                                    except:
                                        # Try action chains as fallback
                                        actions = ActionChains(self.driver)
                                        actions.move_to_element(smart_swadhan_element).click().perform()
                                        logger.info("ActionChains click successful")
                            else:
                                # Element not directly interactable, try parent navigation
                                href = smart_swadhan_element.get_attribute("href")
                                if href:
                                    logger.info(f"Navigating directly to href: {href}")
                                    self.driver.get(href)
                                else:
                                    # Try to get href from parent element
                                    parent = smart_swadhan_element.find_element(By.XPATH, "./..")
                                    parent_href = parent.get_attribute("href")
                                    if parent_href:
                                        logger.info(f"Navigating to parent href: {parent_href}")
                                        self.driver.get(parent_href)
                                    else:
                                        raise Exception("Element not interactable and no href found")
                            
                            self.wait_for_page_load()
                            smart_swadhan_found = True
                            
                            # Extract product details
                            product_info = self.extract_smart_swadhan_details()
                            
                            navigation_steps.append({
                                "step": 4,
                                "description": "Smart Swadhan Supreme Product Page",
                                "url": self.driver.current_url,
                                "screenshot": self.take_screenshot("smart_swadhan"),
                                "elements": self.extract_page_elements(),
                                "product_details": product_info,
                                "success": True
                            })
                            break
                            
                        except Exception as click_error:
                            logger.warning(f"Found Smart Swadhan element but couldn't click: {click_error}")
                            navigation_steps.append({
                                "step": 4,
                                "description": "Smart Swadhan Supreme Found (not clickable)",
                                "url": self.driver.current_url,
                                "screenshot": self.take_screenshot("smart_swadhan_found"),
                                "elements": self.extract_page_elements(),
                                "found_element": smart_swadhan_element.text,
                                "success": False
                            })
                            smart_swadhan_found = True
                            break
                            
                except Exception as e:
                    continue
            
            if not smart_swadhan_found:
                logger.info("Smart Swadhan Supreme not found with selectors, trying direct URL navigation")
                
                # Final fallback: Try direct URL navigation to Smart Swadhan Supreme
                try:
                    smart_swadhan_urls = [
                        f"{self.base_url}/smart-swadhan-supreme",
                        f"{self.base_url}/products/smart-swadhan-supreme",
                        f"{self.base_url}/life-insurance/smart-swadhan-supreme",
                        f"{self.base_url}/insurance-plans/smart-swadhan-supreme",
                        f"{self.base_url}/individual-plans/smart-swadhan-supreme"
                    ]
                    
                    for url in smart_swadhan_urls:
                        try:
                            logger.info(f"Trying direct navigation to: {url}")
                            self.driver.get(url)
                            self.wait_for_page_load()
                            
                            # Check if we found the right page
                            page_source = self.driver.page_source.lower()
                            if "smart swadhan" in page_source and "404" not in page_source:
                                logger.info(f"Successfully found Smart Swadhan at: {url}")
                                smart_swadhan_found = True
                                
                                # Extract product details
                                product_info = self.extract_smart_swadhan_details()
                                
                                navigation_steps.append({
                                    "step": 4,
                                    "description": "Smart Swadhan Supreme (Direct URL)",
                                    "url": self.driver.current_url,
                                    "screenshot": self.take_screenshot("smart_swadhan_direct"),
                                    "elements": self.extract_page_elements(),
                                    "product_details": product_info,
                                    "success": True
                                })
                                break
                                
                        except Exception as url_error:
                            logger.warning(f"Direct URL {url} failed: {url_error}")
                            continue
                            
                except Exception as e:
                    logger.warning(f"Direct URL navigation failed: {e}")
                
                # If still not found, record the failure
                if not smart_swadhan_found:
                    logger.warning("Smart Swadhan Supreme not found with any method")
                    self.debug_page_content("Smart Swadhan Search Failed")
                    navigation_steps.append({
                        "step": 4,
                        "description": "Smart Swadhan Supreme Not Found (All methods attempted)",
                        "url": self.driver.current_url,
                        "screenshot": self.take_screenshot("smart_swadhan_not_found"),
                        "elements": self.extract_page_elements(),
                        "methods_attempted": ["Element selectors", "Direct URLs"],
                        "success": False
                    })
                
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            navigation_steps.append({
                "step": -1,
                "description": f"Navigation Error: {str(e)}",
                "url": self.driver.current_url if self.driver else "Unknown",
                "success": False
            })
            
        return navigation_steps
    
    def extract_smart_swadhan_details(self):
        """Extract detailed information about Smart Swadhan Supreme from real website"""
        try:
            details = {
                "title": "",
                "uin": "",
                "description": "",
                "key_features": [],
                "benefits": [],
                "important_notes": [],
                "buttons": []
            }
            
            # Extract title (try multiple selectors)
            title_selectors = ["h1", "h2", ".product-title", ".main-title"]
            for selector in title_selectors:
                try:
                    title_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if title_element.text.strip():
                        details["title"] = title_element.text.strip()
                        break
                except NoSuchElementException:
                    continue
                    
            # Extract UIN
            try:
                uin_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'UIN') or contains(text(), 'uin')]")
                details["uin"] = uin_element.text.strip()
            except NoSuchElementException:
                pass
                
            # Extract description paragraphs
            try:
                desc_elements = self.driver.find_elements(By.TAG_NAME, "p")
                for elem in desc_elements[:5]:  # First few paragraphs
                    text = elem.text.strip()
                    if text and len(text) > 20:  # Only meaningful descriptions
                        details["description"] += text + " "
            except NoSuchElementException:
                pass
                
            # Extract features and benefits
            try:
                list_elements = self.driver.find_elements(By.XPATH, "//ul//li | //ol//li")
                for elem in list_elements:
                    text = elem.text.strip()
                    if text and len(text) > 10:
                        details["key_features"].append(text)
            except NoSuchElementException:
                pass
                
            # Extract buttons
            try:
                button_selectors = ["button", "a[class*='btn']", "input[type='button']", ".button"]
                for selector in button_selectors:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        text = btn.text.strip()
                        if text:
                            details["buttons"].append(text)
            except Exception:
                pass
                
            return details
        except Exception as e:
            logger.error(f"Error extracting Smart Swadhan details: {e}")
            return {}
    
    def extract_page_elements(self):
        """Extract comprehensive page elements for analysis"""
        try:
            elements = {
                "title": self.driver.title,
                "url": self.driver.current_url,
                "navigation_links": [],
                "buttons": [],
                "headings": [],
                "all_text_content": ""
            }
            
            # Extract all links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links[:50]:  # Limit to prevent overload
                text = link.text.strip()
                href = link.get_attribute("href")
                if text:
                    elements["navigation_links"].append({"text": text, "href": href})
            
            # Extract buttons
            buttons = self.driver.find_elements(By.XPATH, "//button | //input[@type='button'] | //*[contains(@class, 'btn')]")
            for btn in buttons[:20]:
                text = btn.text.strip()
                if text:
                    elements["buttons"].append(text)
            
            # Extract headings
            headings = self.driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4")
            for h in headings:
                text = h.text.strip()
                if text:
                    elements["headings"].append(text)
            
            # Get page text for analysis
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                elements["all_text_content"] = body.text[:1000]  # First 1000 chars
            except:
                pass
                
            return elements
        except Exception as e:
            logger.error(f"Error extracting page elements: {e}")
            return {"error": str(e)}
    
    def take_screenshot(self, name):
        """Take screenshot and return base64 encoded string"""
        try:
            screenshot_path = f"/tmp/sbi_enhanced_{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            # Convert to base64
            with open(screenshot_path, "rb") as img_file:
                screenshot_b64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_b64
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
    
    def get_guided_navigation_data(self):
        """Get complete navigation data with enhanced debugging"""
        logger.info("Starting ENHANCED guided navigation to Smart Swadhan Supreme")
        
        navigation_data = {
            "success": False,
            "steps": [],
            "final_product_info": {},
            "error": None,
            "debug_info": {}
        }
        
        try:
            steps = self.navigate_to_smart_swadhan_supreme()
            navigation_data["steps"] = steps
            
            # Check if we found Smart Swadhan Supreme
            success_steps = [step for step in steps if step.get("success", False)]
            navigation_data["success"] = len(success_steps) > 0
            
            # Get final product info if we reached the product page
            for step in reversed(steps):
                if "product_details" in step:
                    navigation_data["final_product_info"] = step["product_details"]
                    break
                    
            navigation_data["debug_info"] = {
                "total_steps_attempted": len(steps),
                "successful_steps": len(success_steps),
                "final_url": steps[-1]["url"] if steps else "No steps completed"
            }
                
        except Exception as e:
            navigation_data["error"] = str(e)
            logger.error(f"Error in enhanced guided navigation: {e}")
        
        return navigation_data
    
    def close(self):
        """Close the browser driver with a delay to allow viewing"""
        if self.driver:
            logger.info("🔍 Keeping browser open for 15 seconds for viewing the result...")
            time.sleep(15)  # Keep browser open for 15 seconds
            self.driver.quit()
            logger.info("Enhanced browser driver closed")

# Enhanced function for API integration
def scrape_sbi_smart_swadhan_enhanced():
    """Enhanced scraper for real SBI Life website"""
    scraper = None
    try:
        scraper = EnhancedSBIScraper()
        return scraper.get_guided_navigation_data()
    except Exception as e:
        logger.error(f"Error in enhanced scraper: {e}")
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
    # Test the enhanced scraper
    result = scrape_sbi_smart_swadhan_enhanced()
    print(f"Success: {result['success']}")
    print(f"Steps completed: {len(result['steps'])}")
    if result.get('debug_info'):
        print(f"Debug info: {result['debug_info']}")
    if result.get('error'):
        print(f"Error: {result['error']}")
