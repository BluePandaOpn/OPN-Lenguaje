// Smooth scroll behavior for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href !== '#') {
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        history.pushState(null, null, href);
      }
    }
  });
});

// Update active nav link on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

function updateActiveLink() {
  let current = '';
  
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    if (window.pageYOffset >= (sectionTop - 200)) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${current}`) {
      link.classList.add('active');
    }
  });
}

window.addEventListener('scroll', updateActiveLink);

// Copy code to clipboard
document.querySelectorAll('.code-copy').forEach(button => {
  button.addEventListener('click', function () {
    const codeBlock = this.closest('.code-preview').querySelector('code');
    const text = codeBlock.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
      const originalText = this.textContent;
      this.textContent = '✓ Copiado';
      setTimeout(() => {
        this.textContent = originalText;
      }, 2000);
    });
  });
});

// Enhance details/summary behavior
document.querySelectorAll('details').forEach(detail => {
  detail.addEventListener('toggle', function () {
    if (this.open) {
      // Close other details
      document.querySelectorAll('details').forEach(d => {
        if (d !== this && d.open) {
          d.open = false;
        }
      });
    }
  });
});

// Add keyboard shortcuts
document.addEventListener('keydown', function (e) {
  // Ctrl/Cmd + K to focus search (future feature)
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    // Search feature placeholder
  }
  
  // Escape to close modals (future feature)
  if (e.key === 'Escape') {
    document.querySelectorAll('details[open]').forEach(detail => {
      detail.open = false;
    });
  }
});

// Dark mode toggle (if needed in future)
function setupThemeToggle() {
  const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  // Currently hardcoded to dark; can be made dynamic
}

setupThemeToggle();

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function (entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Observe elements for fade-in animation
document.querySelectorAll('.feature-card, .syntax-card, .command-card, .concept-group').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// Responsive sidebar toggle (future mobile menu)
let isSidebarOpen = true;

function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  isSidebarOpen = !isSidebarOpen;
  
  if (window.innerWidth <= 1200) {
    sidebar.style.display = isSidebarOpen ? 'flex' : 'none';
  }
}

window.addEventListener('resize', function () {
  const sidebar = document.querySelector('.sidebar');
  if (window.innerWidth > 1200) {
    sidebar.style.display = 'flex';
    isSidebarOpen = true;
  } else if (!isSidebarOpen) {
    sidebar.style.display = 'none';
  }
});

// Performance monitoring
if (window.performance && window.performance.timing) {
  window.addEventListener('load', function () {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log('Page Load Time: ' + pageLoadTime + 'ms');
  });
}

// Log component initialization
console.log('OPN Documentation Portal loaded');
console.log('Version: 1.0.0');
console.log('Theme: Dark Modern');
