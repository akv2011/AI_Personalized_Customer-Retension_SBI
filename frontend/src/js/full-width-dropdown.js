/**
 * Full-Width Navbar Dropdown Menu
 * This script extends dropdown menus to 100% viewport width with seamless gradient background
 */

document.addEventListener('DOMContentLoaded', function() {
  // Configuration for our dropdown system
  const config = {
    navbarSelector: '.navbar-container',
    navbarWrapperSelector: '.navbar-full-wrapper',
    navGroupSelector: '.nav-dropdown-group',
    dropdownSelector: '.nav-dropdown',
    navItemSelector: '.nav-tab-btn',
    submenuSelector: '.dropdown-submenu',
    zIndex: 1050,
    colors: {
      gradientStart: '#8B0000',
      gradientMiddle1: '#B22222',
      gradientMiddle2: '#4B0082',
      gradientEnd: '#2F1B69'
    }
  };
  
  /**
   * Directly modify existing dropdowns to be full viewport width with seamless gradient
   */
  function enhanceDropdowns() {
    // Get navbar and wrapper references
    const navbar = document.querySelector(config.navbarSelector);
    const navbarWrapper = document.querySelector(config.navbarWrapperSelector) || navbar.parentElement;
    
    if (!navbar) {
      console.warn('Navbar element not found with selector:', config.navbarSelector);
      return;
    }
    
    // Get all dropdowns
    const dropdowns = document.querySelectorAll(config.dropdownSelector);
    if (!dropdowns.length) {
      console.warn('No dropdowns found with selector:', config.dropdownSelector);
      return;
    }
    
    // Process each dropdown
    dropdowns.forEach(dropdown => {
      // Store the original parent for hover behavior
      const originalParent = dropdown.closest(config.navGroupSelector);
      if (!originalParent) return;
      
      // Store reference to original parent for event handling
      dropdown.originalParent = originalParent;
      
      // Get same gradient as the navbar
      const navbarComputedStyle = window.getComputedStyle(navbar);
      const navbarGradient = navbarComputedStyle.backgroundImage;
      
      // Remove the dropdown from its current location
      if (dropdown.parentElement) {
        dropdown.parentElement.removeChild(dropdown);
      }
      
      // Add it to the navbar container itself to ensure it's properly positioned
      navbar.appendChild(dropdown);
      
      // Make dropdown cover the entire navbar area
      dropdown.style.width = '100%';  // Full width of navbar
      dropdown.style.position = 'absolute';
      dropdown.style.left = '0';      // Align with left edge of navbar
      dropdown.style.right = '0';     // Align with right edge of navbar
      dropdown.style.top = '100%';    // Position directly below navbar
      dropdown.style.marginLeft = '0';
      dropdown.style.marginRight = '0';
      
      // Set z-index to appear above other navbar content
      dropdown.style.zIndex = '1000';  // High enough to cover navbar content

      // Apply exact same gradient as navbar for seamless transition
      dropdown.style.background = navbarGradient || `linear-gradient(to right, 
        ${config.colors.gradientStart}, 
        ${config.colors.gradientMiddle1}, 
        ${config.colors.gradientMiddle2}, 
        ${config.colors.gradientEnd})`;
      
      // Ensure no gap between navbar and dropdown
      dropdown.style.borderTop = 'none';
      dropdown.style.marginTop = '0';
      
      // Ensure the dropdown container spans full width
      const dropdownContainer = dropdown.querySelector('.dropdown-container');
      if (dropdownContainer) {
        dropdownContainer.style.width = '100%';
        dropdownContainer.style.padding = '0 24px';  // Match navbar padding
        dropdownContainer.style.boxSizing = 'border-box';
      }
      
      // Enhance submenu item spacing for better alignment
      const submenu = dropdown.querySelector(config.submenuSelector);
      if (submenu) {
        submenu.style.justifyContent = 'space-evenly';
        submenu.style.width = '100%';
        submenu.style.maxWidth = '1400px';
        submenu.style.margin = '0 auto';
        
        // Make sure submenu items are properly spaced
        const submenuItems = submenu.querySelectorAll('.dropdown-submenu-item');
        submenuItems.forEach(item => {
          item.style.flex = '0 0 auto';
          item.style.textAlign = 'center';
        });
      }
      
      // Update hover behavior for the original parent
      originalParent.addEventListener('mouseenter', () => {
        // Hide any other visible dropdowns first
        document.querySelectorAll(config.dropdownSelector).forEach(d => {
          if (d !== dropdown) {
            d.style.opacity = '0';
            d.style.visibility = 'hidden';
            d.style.transform = 'translateY(-10px)';
          }
        });
        
        // Show this dropdown immediately with no delay
        dropdown.style.opacity = '1';
        dropdown.style.visibility = 'visible';
        dropdown.style.transform = 'translateY(0)';
      });
      
      originalParent.addEventListener('mouseleave', (e) => {
        // Check if mouse moved to the dropdown itself
        if (!e.relatedTarget || !dropdown.contains(e.relatedTarget)) {
          setTimeout(() => {
            if (!dropdown.isHovered) {
              dropdown.style.opacity = '0';
              dropdown.style.visibility = 'hidden';
              dropdown.style.transform = 'translateY(-10px)';
            }
          }, 100);
        }
      });
      
      // Track hover state on dropdown itself
      dropdown.isHovered = false;
      dropdown.addEventListener('mouseenter', () => {
        dropdown.isHovered = true;
      });
      
      dropdown.addEventListener('mouseleave', () => {
        dropdown.isHovered = false;
        dropdown.style.opacity = '0';
        dropdown.style.visibility = 'hidden';
        dropdown.style.transform = 'translateY(-10px)';
      });
    });
    
    // Hide dropdowns when hovering non-dropdown nav items
    const navItems = document.querySelectorAll(config.navItemSelector);
    navItems.forEach(item => {
      if (!item.closest(config.navGroupSelector)) {
        item.addEventListener('mouseenter', hideAllDropdowns);
      }
    });
  }
  
  /**
   * Hide all dropdowns
   */
  function hideAllDropdowns() {
    document.querySelectorAll(config.dropdownSelector).forEach(dropdown => {
      dropdown.style.opacity = '0';
      dropdown.style.visibility = 'hidden';
      dropdown.style.transform = 'translateY(-10px)';
    });
  }
  
  /**
   * Update dropdown positions on window resize
   */
  function handleResize() {
    const dropdowns = document.querySelectorAll(config.dropdownSelector);
    const navbar = document.querySelector(config.navbarSelector);
    
    if (!navbar || !dropdowns.length) return;
    
    // Calculate the navbar's position and apply it to the dropdowns
    const navbarRect = navbar.getBoundingClientRect();
    
    dropdowns.forEach(dropdown => {
      dropdown.style.top = `${navbarRect.bottom}px`;
    });
  }
  
  // Set up event listeners
  window.addEventListener('resize', handleResize);
  
  // Initialize the dropdowns
  enhanceDropdowns();
  
  // Update positions on document load
  setTimeout(handleResize, 100);
});
