/**
 * Navbar Dropdown Menu Handler
 * This script handles dropdown functionality for the navigation bar items.
 */

document.addEventListener('DOMContentLoaded', function() {
  // Configuration
  const dropdownConfig = {
    navbarSelector: '.navbar-container',
    navItemsSelector: '.nav-tab-btn',
    serviceItemText: 'SERVICES', // Text to match for the SERVICES nav item
    dropdownZIndex: 1000,
    colors: {
      gradientStart: '#8B0000',
      gradientMiddle1: '#B22222',
      gradientMiddle2: '#4B0082',
      gradientEnd: '#2F1B69',
      textColor: 'rgba(255, 255, 255, 0.9)',
      textHoverColor: '#ffffff',
      itemHoverBg: 'rgba(255, 255, 255, 0.1)'
    }
  };

  // Nav items content for SERVICES dropdown
  const serviceDropdownItems = [
    'Account Services',
    'Loan Services',
    'Investment Advisory',
    'Insurance Services',
    'Digital Banking',
    'NRI Services',
    'Business Banking'
  ];

  // Store references to DOM elements
  let navbar = null;
  let navItems = [];
  let activeDropdown = null;
  
  // Initialize the navbar functionality
  function initNavbar() {
    // Get navbar element
    navbar = document.querySelector(dropdownConfig.navbarSelector);
    if (!navbar) {
      console.error('Navbar not found with selector:', dropdownConfig.navbarSelector);
      return;
    }
    
    // Get all nav items
    navItems = document.querySelectorAll(dropdownConfig.navItemsSelector);
    if (!navItems.length) {
      console.error('Nav items not found with selector:', dropdownConfig.navItemsSelector);
      return;
    }
    
    // Find the SERVICES nav item and attach event listeners
    navItems.forEach(item => {
      if (item.textContent.trim() === dropdownConfig.serviceItemText) {
        // Create dropdown for SERVICES
        createDropdown(item);
        
        // Add event listeners
        item.addEventListener('mouseenter', () => showDropdown(item));
        item.addEventListener('click', (e) => {
          e.preventDefault();
          showDropdown(item);
        });
      } else {
        // For other nav items, hide dropdown when hovered
        item.addEventListener('mouseenter', hideAllDropdowns);
      }
    });
    
    // Hide dropdowns when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest(dropdownConfig.navbarSelector)) {
        hideAllDropdowns();
      }
    });
  }
  
  // Create dropdown element for the given nav item
  function createDropdown(navItem) {
    // Get navbar dimensions for proper positioning
    const navbarRect = navbar.getBoundingClientRect();
    
    // Create dropdown container
    const dropdown = document.createElement('div');
    dropdown.className = 'nav-dropdown';
    dropdown.style.position = 'absolute';
    dropdown.style.top = `${navbarRect.height}px`;
    dropdown.style.left = '0';
    dropdown.style.width = '100%';
    dropdown.style.height = '48px';
    dropdown.style.background = `linear-gradient(to right, ${dropdownConfig.colors.gradientStart}, ${dropdownConfig.colors.gradientMiddle1}, ${dropdownConfig.colors.gradientMiddle2}, ${dropdownConfig.colors.gradientEnd})`;
    dropdown.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';
    dropdown.style.zIndex = dropdownConfig.dropdownZIndex;
    dropdown.style.display = 'none';
    dropdown.style.alignItems = 'center';
    
    // Create dropdown content container
    const dropdownContainer = document.createElement('div');
    dropdownContainer.className = 'dropdown-container';
    dropdownContainer.style.width = '100%';
    dropdownContainer.style.height = '100%';
    dropdownContainer.style.margin = '0';
    dropdownContainer.style.padding = '0 24px';
    dropdownContainer.style.display = 'flex';
    dropdownContainer.style.justifyContent = 'flex-start';
    dropdownContainer.style.alignItems = 'center';
    
    // Create dropdown submenu
    const submenu = document.createElement('div');
    submenu.className = 'dropdown-submenu';
    submenu.style.display = 'flex';
    submenu.style.justifyContent = 'flex-start';
    submenu.style.alignItems = 'center';
    submenu.style.gap = '40px';
    submenu.style.padding = '0';
    submenu.style.width = '100%';
    submenu.style.height = '100%';
    submenu.style.flexWrap = 'nowrap';
    
    // Add submenu items
    serviceDropdownItems.forEach(itemText => {
      const item = document.createElement('a');
      item.className = 'dropdown-submenu-item';
      item.href = '#'; // Use appropriate URLs here
      item.textContent = itemText;
      
      // Style submenu items
      item.style.color = dropdownConfig.colors.textColor;
      item.style.fontWeight = '500';
      item.style.fontSize = '14px';
      item.style.letterSpacing = '0.3px';
      item.style.background = 'transparent';
      item.style.border = 'none';
      item.style.cursor = 'pointer';
      item.style.transition = 'all 0.3s ease';
      item.style.padding = '8px 16px';
      item.style.borderRadius = '4px';
      item.style.whiteSpace = 'nowrap';
      item.style.textDecoration = 'none';
      item.style.display = 'flex';
      item.style.alignItems = 'center';
      
      // Hover effects
      item.addEventListener('mouseenter', () => {
        item.style.color = dropdownConfig.colors.textHoverColor;
        item.style.background = dropdownConfig.colors.itemHoverBg;
        item.style.transform = 'translateY(-1px)';
      });
      
      item.addEventListener('mouseleave', () => {
        item.style.color = dropdownConfig.colors.textColor;
        item.style.background = 'transparent';
        item.style.transform = 'none';
      });
      
      submenu.appendChild(item);
    });
    
    // Assemble dropdown
    dropdownContainer.appendChild(submenu);
    dropdown.appendChild(dropdownContainer);
    navbar.appendChild(dropdown);
    
    // Store dropdown reference with nav item
    navItem.dropdown = dropdown;
    
    // Add mouseenter/mouseleave events for the dropdown itself
    dropdown.addEventListener('mouseenter', () => {
      showDropdown(navItem);
    });
    
    dropdown.addEventListener('mouseleave', hideAllDropdowns);
  }
  
  // Show dropdown for specified nav item
  function showDropdown(navItem) {
    // Hide any existing dropdown first
    hideAllDropdowns();
    
    // Show this dropdown
    if (navItem.dropdown) {
      navItem.dropdown.style.display = 'flex';
      activeDropdown = navItem.dropdown;
    }
  }
  
  // Hide all dropdowns
  function hideAllDropdowns() {
    navItems.forEach(item => {
      if (item.dropdown) {
        item.dropdown.style.display = 'none';
      }
    });
    activeDropdown = null;
  }
  
  // Add window resize handler to update dropdown positioning
  window.addEventListener('resize', () => {
    if (navbar) {
      const navbarRect = navbar.getBoundingClientRect();
      navItems.forEach(item => {
        if (item.dropdown) {
          item.dropdown.style.top = `${navbarRect.height}px`;
        }
      });
    }
  });
  
  // Initialize the navbar
  initNavbar();
});
