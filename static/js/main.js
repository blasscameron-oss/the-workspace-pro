/* The Workspace Pro - Main JavaScript */
document.addEventListener('DOMContentLoaded', function() {
    console.log('The Workspace Pro loaded');
    
    // ========== DARK MODE TOGGLE ==========
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkIcon = darkModeToggle.querySelector('.fa-moon');
    const lightIcon = darkModeToggle.querySelector('.fa-sun');
    
    // Check for saved theme or prefer-color-scheme
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.classList.add('dark');
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
    }
    
    darkModeToggle.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark');
        darkIcon.classList.toggle('hidden', isDark);
        lightIcon.classList.toggle('hidden', !isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
    
    // ========== MOBILE MENU ==========
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            mobileMenuToggle.querySelector('i').classList.toggle('fa-bars');
            mobileMenuToggle.querySelector('i').classList.toggle('fa-times');
        });
        
        // Close menu when clicking a link
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                mobileMenuToggle.querySelector('i').classList.add('fa-bars');
                mobileMenuToggle.querySelector('i').classList.remove('fa-times');
            });
        });
    }
    
    // ========== SEARCH OVERLAY ==========
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const searchResults = document.getElementById('searchResults');
    
    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', () => {
            searchOverlay.classList.remove('hidden');
            searchInput.focus();
        });
        
        searchClose.addEventListener('click', () => {
            searchOverlay.classList.add('hidden');
            searchResults.classList.add('hidden');
            searchInput.value = '';
        });
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !searchOverlay.classList.contains('hidden')) {
                searchOverlay.classList.add('hidden');
                searchResults.classList.add('hidden');
                searchInput.value = '';
            }
        });
        
        // Sample search data (would be fetched from API in production)
        const searchData = [
            { title: 'Ergonomic Desk Setup', url: '/guides/ergonomic-desk-setup/', category: 'Guide' },
            { title: 'Cable Management Solutions', url: '/guides/cable-management/', category: 'Guide' },
            { title: 'Video Call Lighting Guide', url: '/guides/video-call-lighting/', category: 'Guide' },
            { title: 'Choosing the Perfect Monitor', url: '/guides/choose-monitor/', category: 'Guide' },
            { title: 'IKEA BEKANT Sit/Stand Desk Review', url: '/products/bekant-desk/', category: 'Product' },
            { title: 'Daily Tip: Desk Organization', url: '/tips/organization/', category: 'Tip' },
            { title: 'Workspace Personality Quiz', url: '/quiz/', category: 'Quiz' },
            { title: 'About The Workspace Pro', url: '/about/', category: 'Page' }
        ];
        
        function performSearch(query) {
            if (!query.trim()) {
                searchResults.classList.add('hidden');
                return;
            }
            
            const results = searchData.filter(item => 
                item.title.toLowerCase().includes(query.toLowerCase()) ||
                item.category.toLowerCase().includes(query.toLowerCase())
            );
            
            searchResults.innerHTML = '';
            
            if (results.length === 0) {
                searchResults.innerHTML = '<p class="p-4 text-text-light text-center">No results found. Try a different keyword.</p>';
                searchResults.classList.remove('hidden');
                return;
            }
            
            results.forEach(result => {
                const div = document.createElement('div');
                div.className = 'p-4 border-b border-border hover:bg-surface transition-colors';
                div.innerHTML = `
                    <a href="${result.url}" class="block">
                        <h4 class="font-bold text-text">${result.title}</h4>
                        <p class="text-sm text-text-light mt-1">${result.category}</p>
                    </a>
                `;
                searchResults.appendChild(div);
            });
            
            searchResults.classList.remove('hidden');
        }
        
        // Debounce search input
        let searchTimeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(searchInput.value);
            }, 300);
        });
        
        searchButton.addEventListener('click', () => performSearch(searchInput.value));
        
        // Search on Enter
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch(searchInput.value);
        });
    }
    
    // ========== TIP OF THE DAY CAROUSEL ==========
    const tipContent = document.getElementById('tipContent');
    const tipDate = document.getElementById('tipDate');
    const copyTipBtn = document.getElementById('copyTipBtn');
    const shareTipBtn = document.getElementById('shareTipBtn');
    const prevTipBtn = document.getElementById('prevTipBtn');
    const nextTipBtn = document.getElementById('nextTipBtn');
    
    const tips = [
        {
            text: 'Keep your desk surface clutter-free—use cable trays and drawer organizers to maintain a clean, focused environment.',
            date: 'April 18, 2026',
            tags: ['Organization', 'Productivity', 'Desk Setup']
        },
        {
            text: 'Position your monitor so the top of the screen is at or slightly below eye level to reduce neck strain.',
            date: 'April 17, 2026',
            tags: ['Ergonomics', 'Health', 'Monitor']
        },
        {
            text: 'Use natural light whenever possible, but add a desk lamp with adjustable brightness for evening work.',
            date: 'April 16, 2026',
            tags: ['Lighting', 'Eye Health', 'Comfort']
        },
        {
            text: 'Take a 5‑minute break every hour to stand, stretch, and look at something 20 feet away.',
            date: 'April 15, 2026',
            tags: ['Health', 'Productivity', 'Break']
        },
        {
            text: 'Invest in a quality chair with lumbar support—your back will thank you after long work sessions.',
            date: 'April 14, 2026',
            tags: ['Ergonomics', 'Chair', 'Investment']
        }
    ];
    
    let currentTipIndex = 0;
    
    function updateTipDisplay() {
        const tip = tips[currentTipIndex];
        tipContent.textContent = tip.text;
        tipDate.textContent = tip.date;
        
        // Update tags (simplified - in a real app you'd update the tag elements)
        console.log('Current tip tags:', tip.tags);
    }
    
    if (prevTipBtn && nextTipBtn) {
        prevTipBtn.addEventListener('click', () => {
            currentTipIndex = (currentTipIndex - 1 + tips.length) % tips.length;
            updateTipDisplay();
        });
        
        nextTipBtn.addEventListener('click', () => {
            currentTipIndex = (currentTipIndex + 1) % tips.length;
            updateTipDisplay();
        });
    }
    
    // ========== COPY TIP BUTTON ==========
    if (copyTipBtn) {
        copyTipBtn.addEventListener('click', async () => {
            const tipText = tipContent.textContent;
            
            try {
                await navigator.clipboard.writeText(tipText);
                
                // Show feedback
                const originalHtml = copyTipBtn.innerHTML;
                copyTipBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                copyTipBtn.classList.add('bg-green-100', 'text-green-800');
                copyTipBtn.classList.remove('bg-surface', 'hover:bg-border', 'text-text');
                
                setTimeout(() => {
                    copyTipBtn.innerHTML = originalHtml;
                    copyTipBtn.classList.remove('bg-green-100', 'text-green-800');
                    copyTipBtn.classList.add('bg-surface', 'hover:bg-border', 'text-text');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
                alert('Could not copy tip. Please try again.');
            }
        });
    }
    
    // ========== SHARE TIP BUTTON ==========
    if (shareTipBtn) {
        shareTipBtn.addEventListener('click', async () => {
            const tipText = tipContent.textContent;
            const shareData = {
                title: 'Workspace Tip of the Day',
                text: tipText,
                url: window.location.href
            };
            
            if (navigator.share) {
                try {
                    await navigator.share(shareData);
                } catch (err) {
                    console.log('Share cancelled:', err);
                }
            } else {
                // Fallback: copy to clipboard
                await navigator.clipboard.writeText(`${tipText}\n\n${window.location.href}`);
                alert('Tip link copied to clipboard!');
            }
        });
    }
    
    // ========== SOCIAL SHARING BUTTONS ==========
    document.querySelectorAll('.share-social').forEach(button => {
        button.addEventListener('click', function() {
            const network = this.getAttribute('data-network');
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);
            const text = encodeURIComponent('Check out this workspace tip from The Workspace Pro!');
            
            let shareUrl;
            
            switch (network) {
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
                    break;
                case 'linkedin':
                    shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
                    break;
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                    break;
                default:
                    return;
            }
            
            window.open(shareUrl, '_blank', 'width=600,height=400');
        });
    });
    
    // ========== NEWSLETTER FORMS ==========
    const newsletterForm = document.getElementById('newsletterForm');
    const footerNewsletter = document.getElementById('footerNewsletter');
    const exitNewsletterForm = document.getElementById('exitNewsletterForm');
    
    function handleNewsletterSubmit(form, emailInput) {
        const email = emailInput.value.trim();
        
        if (!email || !validateEmail(email)) {
            alert('Please enter a valid email address.');
            return false;
        }
        
        // Simulate submission
        console.log('Newsletter submission:', email);
        
        // Show success modal
        document.getElementById('newsletterModal').classList.remove('hidden');
        
        // Reset form
        form.reset();
        
        return false; // Prevent actual submit for demo
    }
    
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('newsletterEmail');
            handleNewsletterSubmit(newsletterForm, emailInput);
        });
    }
    
    if (footerNewsletter) {
        footerNewsletter.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = footerNewsletter.querySelector('input[type="email"]');
            handleNewsletterSubmit(footerNewsletter, emailInput);
        });
    }
    
    if (exitNewsletterForm) {
        exitNewsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = exitNewsletterForm.querySelector('input[type="email"]');
            if (handleNewsletterSubmit(exitNewsletterForm, emailInput)) {
                document.getElementById('exitIntentModal').classList.add('hidden');
            }
        });
    }
    
    // ========== EXIT-INTENT MODAL ==========
    const exitIntentModal = document.getElementById('exitIntentModal');
    const closeExitModal = document.getElementById('closeExitModal');
    
    if (exitIntentModal && closeExitModal) {
        closeExitModal.addEventListener('click', () => {
            exitIntentModal.classList.add('hidden');
        });
        
        // Show modal when mouse leaves window
        let mouseY = 0;
        document.addEventListener('mouseleave', (e) => {
            mouseY = e.clientY;
            if (mouseY < 10) {
                // Only show once per session
                if (!sessionStorage.getItem('exitIntentShown')) {
                    setTimeout(() => {
                        exitIntentModal.classList.remove('hidden');
                        sessionStorage.setItem('exitIntentShown', 'true');
                    }, 500);
                }
            }
        });
        
        // Also show after 30 seconds if user hasn't interacted
        setTimeout(() => {
            if (!sessionStorage.getItem('exitIntentShown')) {
                exitIntentModal.classList.remove('hidden');
                sessionStorage.setItem('exitIntentShown', 'true');
            }
        }, 30000);
    }
    
    // ========== NEWSLETTER MODAL ==========
    const newsletterModal = document.getElementById('newsletterModal');
    const closeNewsletterModal = document.getElementById('closeNewsletterModal');
    
    if (newsletterModal && closeNewsletterModal) {
        closeNewsletterModal.addEventListener('click', () => {
            newsletterModal.classList.add('hidden');
        });
    }
    
    // ========== SUBMIT TIP MODAL ==========
    const submitTipModal = document.getElementById('submitTipModal');
    const closeTipModal = document.getElementById('closeTipModal');
    const tipForm = document.getElementById('tipForm');
    
    // Button to open modal (not in HTML yet, but we'll add later)
    const submitTipButtons = document.querySelectorAll('[data-open-tip-modal]');
    submitTipButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            submitTipModal.classList.remove('hidden');
        });
    });
    
    if (closeTipModal) {
        closeTipModal.addEventListener('click', () => {
            submitTipModal.classList.add('hidden');
        });
    }
    
    if (tipForm) {
        tipForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('tipName').value;
            const text = document.getElementById('tipText').value;
            const category = document.getElementById('tipCategory').value;
            
            if (!text.trim()) {
                alert('Please enter a tip before submitting.');
                return;
            }
            
            // Simulate submission
            console.log('Tip submitted:', { name, text, category });
            
            // Show success message
            alert('Thank you for your tip! We\'ll review it and may feature it on the site.');
            
            // Reset and close
            tipForm.reset();
            submitTipModal.classList.add('hidden');
        });
    }
    
    // ========== PRINT BUTTON ==========
    const printButton = document.getElementById('printButton');
    if (printButton) {
        printButton.addEventListener('click', () => {
            window.print();
        });
    }
    
    // ========== STICKY BAR ==========
    const stickyBar = document.getElementById('stickyBar');
    if (stickyBar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                stickyBar.classList.remove('hidden');
            } else {
                stickyBar.classList.add('hidden');
            }
        });
    }
    
    // ========== SMOOTH SCROLL FOR ANCHOR LINKS ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ========== INITIALIZE TIP DISPLAY ==========
    updateTipDisplay();
    
    // ========== ADD PRINT BUTTON TO GUIDES ==========
    // This would be added dynamically on guide pages
    if (window.location.pathname.includes('/guides/')) {
        const guideContent = document.querySelector('article');
        if (guideContent) {
            const printBtn = document.createElement('button');
            printBtn.className = 'print-button bg-primary hover:bg-primary-light text-white font-semibold py-2 px-4 rounded-lg transition-colors';
            printBtn.innerHTML = '<i class="fas fa-print mr-2"></i> Print Guide';
            printBtn.addEventListener('click', () => window.print());
            
            guideContent.insertBefore(printBtn, guideContent.firstChild);
        }
    }
    
    // ========== LAZY LOAD IMAGES ==========
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
        
        document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
    }
    
    // ========== IMAGE ERROR HANDLING ==========
    // Graceful fallback for broken images
    document.querySelectorAll('img').forEach(img => {
        // Skip hero/background banners and decorative images
        img.addEventListener('error', function() {
            // If image has a fallback data attribute, use it
            if (this.dataset.fallback) {
                this.src = this.dataset.fallback;
                this.onerror = null; // prevent infinite loop
                return;
            }
            
            // Generic fallbacks based on context
            const fallbacks = {
                'hero': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
                'product': 'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                'guide': 'https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'default': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            };
            
            // Determine context from parent or class
            const parentClasses = (this.parentElement?.className || '') + ' ' + (this.className || '');
            let type = 'default';
            if (parentClasses.includes('hero') || parentClasses.includes('Hero')) type = 'hero';
            else if (parentClasses.includes('product') || parentClasses.includes('Product')) type = 'product';
            else if (parentClasses.includes('guide') || parentClasses.includes('Guide')) type = 'guide';
            
            this.src = fallbacks[type] || fallbacks.default;
            this.onerror = null; // prevent infinite loop on fallback
        });
    });
});