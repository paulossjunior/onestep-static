// Language Selector for MkDocs
(function() {
    'use strict';
    
    // Language configuration
    const languages = {
        'en': {
            name: 'English',
            flag: '🇺🇸',
            path: '/'
        },
        'pt': {
            name: 'Português (Brasil)',
            flag: '🇧🇷',
            path: '/pt/'
        }
    };
    
    // Detect current language from URL
    function getCurrentLanguage() {
        const path = window.location.pathname;
        if (path.startsWith('/pt/') || path === '/pt') {
            return 'pt';
        }
        return 'en';
    }
    
    // Get current page path without language prefix
    function getCurrentPage() {
        const path = window.location.pathname;
        const currentLang = getCurrentLanguage();
        
        if (currentLang === 'pt') {
            return path.replace('/pt/', '/').replace('/pt', '/');
        }
        return path;
    }
    
    // Build language URL
    function buildLanguageUrl(lang) {
        const currentPage = getCurrentPage();
        
        if (lang === 'en') {
            return currentPage;
        } else {
            // For Portuguese, add /pt/ prefix
            if (currentPage === '/' || currentPage === '') {
                return '/pt/';
            }
            return '/pt' + currentPage;
        }
    }
    
    // Create language selector
    function createLanguageSelector() {
        const currentLang = getCurrentLanguage();
        
        // Create container
        const container = document.createElement('div');
        container.className = 'language-selector';
        
        // Create select element
        const select = document.createElement('select');
        select.id = 'language-select';
        select.setAttribute('aria-label', 'Select Language');
        
        // Add options
        for (const [code, lang] of Object.entries(languages)) {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = `${lang.flag} ${lang.name}`;
            if (code === currentLang) {
                option.selected = true;
            }
            select.appendChild(option);
        }
        
        // Add change event
        select.addEventListener('change', function() {
            const selectedLang = this.value;
            const newUrl = buildLanguageUrl(selectedLang);
            window.location.href = newUrl;
        });
        
        container.appendChild(select);
        
        // Insert into page
        document.body.appendChild(container);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createLanguageSelector);
    } else {
        createLanguageSelector();
    }
})();
