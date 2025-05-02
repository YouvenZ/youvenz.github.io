// static/js/search.js

/**
 * Enhanced search functionality for academic website
 */
 
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    initializeFilters();
});

/**
 * Initialize search functionality for publications and research
 */
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[id$="-search"]');
    
    searchInputs.forEach(searchInput => {
        const clearButton = document.getElementById(`clear-${searchInput.id}`);
        const targetId = searchInput.id.split('-')[0] + '-list';
        const targetList = document.getElementById(targetId);
        
        if (!searchInput || !targetList) return;
        
        // Search functionality
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            const items = targetList.querySelectorAll('.publication-item, .research-item');
            let resultsFound = false;
            
            items.forEach(item => {
                const content = item.textContent.toLowerCase();
                const shouldShow = content.includes(searchTerm);
                
                item.style.display = shouldShow ? '' : 'none';
                if (shouldShow) resultsFound = true;
            });
            
            // Handle no results state
            handleNoResults(targetList, resultsFound, searchTerm);
            
            // Toggle clear button
            if (clearButton) {
                clearButton.style.display = searchTerm !== '' ? 'block' : 'none';
            }
        });
        
        // Clear search button
        if (clearButton) {
            clearButton.addEventListener('click', function() {
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
                this.style.display = 'none';
                searchInput.focus();
            });
        }
    });
}

/**
 * Initialize filtering functionality
 */
function initializeFilters() {
    const filters = document.querySelectorAll('.filter-select');
    
    filters.forEach(filter => {
        const targetId = filter.id.split('-')[0] + '-grid';
        const targetGrid = document.getElementById(targetId);
        
        if (!filter || !targetGrid) return;
        
        filter.addEventListener('change', function() {
            const category = this.value.toLowerCase();
            const items = targetGrid.querySelectorAll('[data-categories]');
            let itemsVisible = false;
            
            items.forEach(item => {
                const itemCategories = item.dataset.categories ? item.dataset.categories.toLowerCase() : '';
                const shouldShow = category === '' || itemCategories.includes(category);
                
                item.style.display = shouldShow ? '' : 'none';
                if (shouldShow) itemsVisible = true;
            });
            
            // Handle no results state
            handleNoResults(targetGrid, itemsVisible, category);
        });
    });
}

/**
 * Handle no results state for search and filtering
 */
function handleNoResults(container, resultsFound, searchTerm) {
    const noResultsId = `no-results-${container.id}`;
    const existingMessage = document.getElementById(noResultsId);
    
    if (!resultsFound && searchTerm !== '') {
        if (!existingMessage) {
            const message = document.createElement('p');
            message.id = noResultsId;
            message.className = 'no-results';
            message.textContent = `No results found${searchTerm ? ' for "' + searchTerm + '"' : ''}.`;
            container.appendChild(message);
        }
    } else if (existingMessage) {
        existingMessage.remove();
    }
}

/**
 * Highlight search term in content
 * @param {string} content - The content to search within
 * @param {string} term - The term to highlight
 * @returns {string} - Content with highlighted term
 */
function highlightSearchTerm(content, term) {
    if (!term) return content;
    
    const regex = new RegExp(`(${escapeRegExp(term)})`, 'gi');
    return content.replace(regex, '<mark>$1</mark>');
}

/**
 * Escape special characters for RegExp
 * @param {string} text - Text to escape
 * @returns {string} - Escaped text
 */
function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Debounce function for search optimization
 * @param {Function} func - Function to debounce
 * @param {number} wait - Milliseconds to wait
 * @returns {Function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

/**
 * Add lazy loading for images
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);