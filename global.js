// Global JS
document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.glass-nav');
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            nav.style.padding = '0.5rem 0';
            nav.style.background = 'rgba(15, 23, 42, 0.9)';
        } else {
            nav.style.padding = '0.75rem 0';
            nav.style.background = 'rgba(15, 23, 42, 0.7)';
        }
    });
});
