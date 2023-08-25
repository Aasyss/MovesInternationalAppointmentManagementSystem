// navbar.js - Add this to your JavaScript files
const sidebar = document.getElementById('sidebar');
const contentContainer = document.querySelector('.content-container');
const triggerOffset = 200; // Adjust as needed

function toggleSidebar() {
  if (window.scrollY > triggerOffset) {
    sidebar.classList.add('active');
  } else {
    sidebar.classList.remove('active');
  }
}

window.addEventListener('scroll', toggleSidebar);
