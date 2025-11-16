// --- Initialize theme on page load ---
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

// --- Toggle dark mode ---
function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    
    // Optional: update button text/icon
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) toggleBtn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
}

// --- Call on window load ---
window.addEventListener('DOMContentLoaded', () => {
    initTheme();

    // Attach toggle function to button
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) toggleBtn.addEventListener('click', toggleTheme);
});
