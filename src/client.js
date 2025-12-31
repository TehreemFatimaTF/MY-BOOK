// Client module to handle Urdu translation functionality
import { useTranslation } from './contexts/TranslationContext';

// Add a client module to handle the navbar translation button
if (typeof window !== 'undefined') {
  // Make handleLogoutClick globally available for navbar dropdown
  window.handleLogoutClick = function() {
    handleLogout();
  };

  // Wait for the page to load
  window.addEventListener('load', () => {
    // Find the navbar translation button
    const translationButtons = document.querySelectorAll('.urdu-translation-button');

    if (translationButtons.length > 0) {
      // Add click event to all translation buttons
      translationButtons.forEach(button => {
        // Update button text based on current language
        updateButtonText(button);

        button.addEventListener('click', function(event) {
          event.preventDefault();

          // Get the current language from the data attribute or default to 'en'
          const currentLang = document.body.getAttribute('data-language') || 'en';

          if (window.translationContext) {
            // Use the translation context if available
            if (currentLang === 'en') {
              window.translationContext.setUrdu();
              document.body.setAttribute('data-language', 'ur');
            } else {
              window.translationContext.setEnglish();
              document.body.setAttribute('data-language', 'en');
            }
          } else {
            // Fallback: toggle a class or trigger a custom event
            document.body.classList.toggle('urdu-mode');
            const newLang = document.body.classList.contains('urdu-mode') ? 'ur' : 'en';
            document.body.setAttribute('data-language', newLang);

            // Dispatch a custom event to notify other components
            window.dispatchEvent(new CustomEvent('languageChange', {
              detail: { language: newLang }
            }));
          }

          // Update button text after language change
          updateButtonText(button);
        });
      });
    }

    // Listen for language change events to update button text
    window.addEventListener('languageChange', function(e) {
      const buttons = document.querySelectorAll('.urdu-translation-button');
      buttons.forEach(btn => updateButtonText(btn));
    });

    // Add logout functionality
    initializeLogoutHandler();
  });

  // Function to update button text based on current language
  function updateButtonText(button) {
    const currentLang = document.body.getAttribute('data-language') || 'en';
    if (currentLang === 'ur') {
      button.querySelector('span') ?
        button.querySelector('span').textContent = 'Switch to English' :
        button.textContent = 'Switch to English';
    } else {
      button.querySelector('span') ?
        button.querySelector('span').textContent = 'Translate to Urdu' :
        button.textContent = 'Translate to Urdu';
    }
  }

  // Initialize logout handler
  function initializeLogoutHandler() {
    // Add event listener for the logout button
    document.addEventListener('click', function(event) {
      // Check if the clicked element or its parent has the logout-button class
      const logoutButton = event.target.closest('.logout-button');
      if (logoutButton) {
        event.preventDefault();
        handleLogout();
      }
    });
  }

  async function handleLogout() {
    try {
      // Dispatch a custom logout event that the AuthContext can listen for
      window.dispatchEvent(new CustomEvent('logoutRequested'));

      // Immediately redirect to the main page which will show login options for unauthenticated users
      // The AuthContext will handle the actual Firebase sign-out when it receives the event
      window.location.href = '/';
    } catch (error) {
      console.error('Error during logout:', error);
    }
  }
}