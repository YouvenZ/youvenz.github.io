// static/js/filters.js

/**
 * Advanced filtering functionality for research, publications, and teaching
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeCVNavigation();
    initializeAdvancedFilters();
});

/**
 * Initialize CV page navigation highlighting and smooth scrolling
 */
function initializeCVNavigation() {
    const cvNavLinks = document.querySelectorAll('.cv-navigation a');
    if (cvNavLinks.length === 0) return;
    
    // Smooth scrolling for CV page navigation
    cvNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                // Calculate header offset for sticky navigation
                const navHeight = document.querySelector('.cv-nav-container').offsetHeight;
                const targetPosition = targetSection.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Update URL hash
                history.pushState(null, null, `#${targetId}`);
            }
        });
    });
    
    // Highlight active section on scroll
    window.addEventListener('scroll', debounce(function() {
        // Calculate header offset for sticky navigation
        const navHeight = document.querySelector('.cv-nav-container').offsetHeight;
        
        // Get all CV sections
        const sections = document.querySelectorAll('.cv-section');
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            
            if (window.pageYOffset >= sectionTop - navHeight - 100) {
                currentSection = section.getAttribute('id');
            }
        });
        
        // Update active navigation link
        cvNavLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }, 100));
    
    // Handle initial page load with hash
    if (window.location.hash) {
        const initialHash = window.location.hash.substring(1);
        const targetSection = document.getElementById(initialHash);
        
        if (targetSection) {
            // Wait for page to fully load before scrolling
            setTimeout(() => {
                const navHeight = document.querySelector('.cv-nav-container').offsetHeight;
                const targetPosition = targetSection.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Update active navigation link
                cvNavLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${initialHash}`) {
                        link.classList.add('active');
                    }
                });
            }, 100);
        }
    }
}

/**
 * Initialize advanced filtering functionality
 */
function initializeAdvancedFilters() {
    // Publications year filter
    const yearFilter = document.getElementById('year-filter');
    if (yearFilter) {
        yearFilter.addEventListener('change', function() {
            const selectedYear = this.value;
            const publications = document.querySelectorAll('.publication-item');
            
            publications.forEach(pub => {
                const pubYear = pub.dataset.year;
                if (selectedYear === '' || pubYear === selectedYear) {
                    pub.style.display = '';
                } else {
                    pub.style.display = 'none';
                }
            });
        });
    }
    
    // Publications type filter
    const typeFilter = document.getElementById('type-filter');
    if (typeFilter) {
        typeFilter.addEventListener('change', function() {
            const selectedType = this.value;
            const publications = document.querySelectorAll('.publication-item');
            
            publications.forEach(pub => {
                const pubType = pub.dataset.type;
                if (selectedType === '' || pubType === selectedType) {
                    pub.style.display = '';
                } else {
                    pub.style.display = 'none';
                }
            });
        });
    }
    
    // Tag filter functionality
    const tagButtons = document.querySelectorAll('.tag-filter');
    tagButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const selectedTag = this.dataset.tag;
            const items = document.querySelectorAll('[data-tags]');
            
            // Toggle active state on button
            tagButtons.forEach(b => b.classList.remove('active'));
            if (selectedTag !== 'all') {
                this.classList.add('active');
            }
            
            // Filter items
            items.forEach(item => {
                const itemTags = item.dataset.tags ? item.dataset.tags.split(',') : [];
                if (selectedTag === 'all' || itemTags.includes(selectedTag)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Combined filter functionality
    initializeCombinedFilters();
}

/**
 * Initialize combined filters (multiple filter criteria)
 */
function initializeCombinedFilters() {
    const filterForm = document.getElementById('combined-filters');
    if (!filterForm) return;
    
    const filterInputs = filterForm.querySelectorAll('select, input[type="checkbox"]');
    const targetContainer = document.querySelector(filterForm.dataset.target);
    
    if (!targetContainer) return;
    
    // Apply filters when any input changes
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            applyFilters(filterForm, targetContainer);
        });
    });
    
    // Reset filters button
    const resetButton = filterForm.querySelector('.reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Reset all form inputs
            filterForm.reset();
            
            // Update any custom select UI
            filterInputs.forEach(input => {
                if (input.tagName === 'SELECT') {
                    input.dispatchEvent(new Event('change'));
                }
            });
            
            // Apply filters (show all)
            applyFilters(filterForm, targetContainer);
        });
    }
}

/**
 * Apply multiple filters to a container
 * @param {HTMLFormElement} form - Filter form
 * @param {HTMLElement} container - Container with filterable items
 */
function applyFilters(form, container) {
    const filters = {};
    
    // Collect all filter values
    form.querySelectorAll('select').forEach(select => {
        const name = select.name;
        const value = select.value;
        if (value) filters[name] = value;
    });
    
    // Collect checked checkboxes
    const checkboxGroups = {};
    form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        if (!checkbox.checked) return;
        
        const name = checkbox.name;
        if (!checkboxGroups[name]) checkboxGroups[name] = [];
        checkboxGroups[name].push(checkbox.value);
    });
    
    // Add checkbox groups