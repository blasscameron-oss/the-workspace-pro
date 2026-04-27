// ============================================
// NAV.JS - Top Persistent Navigation controls
// ============================================

// --- MOBILE MENU (side drawer) ---
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    if (!menu || !overlay) return;
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        // Reset scroll position
        menu.scrollTop = 0;
    } else {
        closeMobileMenu();
    }
}

function closeMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    if (menu) menu.classList.add('hidden');
    if (overlay) overlay.classList.add('hidden');
    document.body.style.overflow = '';
}

// Close mobile menu on Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const menu = document.getElementById('mobileMenu');
        if (menu && !menu.classList.contains('hidden')) {
            closeMobileMenu();
        }
    }
});

// --- SEARCH OVERLAY ---
function toggleSearch() {
    const overlay = document.getElementById('search-overlay');
    if (!overlay) return;
    if (overlay.classList.contains('hidden')) {
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        setTimeout(function() {
            const input = document.getElementById('search-input');
            if (input) input.focus();
        }, 150);
    } else {
        closeSearch();
    }
}

function closeSearch() {
    const overlay = document.getElementById('search-overlay');
    if (overlay) overlay.classList.add('hidden');
    document.body.style.overflow = '';
}

// Close search on Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const overlay = document.getElementById('search-overlay');
        if (overlay && !overlay.classList.contains('hidden')) {
            closeSearch();
        }
    }
});

// Close search on backdrop click
document.addEventListener('click', function(e) {
    const overlay = document.getElementById('search-overlay');
    if (overlay && !overlay.classList.contains('hidden') && e.target === overlay) {
        closeSearch();
    }
});

// --- DARK MODE ---
function updateDarkModeIcon() {
    const darkIcon = document.getElementById('navDarkIcon');
    const lightIcon = document.getElementById('navLightIcon');
    if (darkIcon && lightIcon) {
        const isDark = document.documentElement.classList.contains('dark');
        darkIcon.classList.toggle('hidden', isDark);
        lightIcon.classList.toggle('hidden', !isDark);
    }
}

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateDarkModeIcon);
} else {
    updateDarkModeIcon();
}
