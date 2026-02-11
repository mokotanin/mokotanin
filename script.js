// Mobile Navigation
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Consolidated Scroll Handler with throttling
let scrollTimeout;
const navbar = document.querySelector('.navbar');
const hero = document.querySelector('.hero');
const sections = document.querySelectorAll('section[id]');

function handleScroll() {
    const scrollY = window.pageYOffset;
    
    // Navbar background
    if (scrollY > 50) {
        navbar.style.background = 'rgba(0, 0, 0, 0.98)';
        navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.5)';
    } else {
        navbar.style.background = 'rgba(0, 0, 0, 0.95)';
        navbar.style.boxShadow = 'none';
    }
    
    // Parallax effect for hero
    if (hero) {
        hero.style.transform = `translateY(${scrollY * 0.5}px)`;
    }
    
    // Active navigation highlighting
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLink?.classList.add('active');
        } else {
            navLink?.classList.remove('active');
        }
    });
}

// Throttled scroll event
window.addEventListener('scroll', () => {
    if (!scrollTimeout) {
        scrollTimeout = setTimeout(() => {
            handleScroll();
            scrollTimeout = null;
        }, 10);
    }
});

// Intersection Observer for Scroll Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            
            // Animate skill bars
            if (entry.target.classList.contains('skill-card')) {
                const progressBar = entry.target.querySelector('.skill-progress');
                const targetWidth = progressBar.getAttribute('data-progress');
                setTimeout(() => {
                    progressBar.style.width = targetWidth + '%';
                }, 200);
            }
            
            // Animate counters
            if (entry.target.classList.contains('stat-item')) {
                const counter = entry.target.querySelector('.stat-number');
                if (!counter.dataset.animated) {
                    const target = parseInt(counter.getAttribute('data-target'));
                    counter.dataset.animated = 'true';
                    animateCounter(counter, target);
                }
            }
        }
    });
}, observerOptions);

// Observe elements
document.querySelectorAll('.skill-card, .project-card, .fade-in, .stat-item').forEach(el => {
    observer.observe(el);
});

// Counter Animation
function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 30);
}

// Form Submission
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const subject = document.getElementById('subject').value;
        const message = document.getElementById('message').value;
        
        // Simple validation
        if (name && email && subject && message) {
            // Create success message
            const successMsg = document.createElement('div');
            successMsg.className = 'success-message';
            successMsg.textContent = 'Message sent successfully! ✓';
            document.body.appendChild(successMsg);
            
            // Reset form
            contactForm.reset();
            
            // Remove message after 3 seconds
            setTimeout(() => {
                successMsg.classList.add('fade-out');
                setTimeout(() => {
                    document.body.removeChild(successMsg);
                }, 500);
            }, 3000);
        }
    });
}

// Typing Effect for Hero Section (optional enhancement)
const heroSubtitle = document.querySelector('.hero-subtitle');
if (heroSubtitle) {
    const text = heroSubtitle.textContent;
    heroSubtitle.textContent = '';
    let i = 0;
    
    function typeWriter() {
        if (i < text.length) {
            heroSubtitle.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    }
    
    // Start typing after page load
    setTimeout(typeWriter, 1000);
}


// Active class styling is now consolidated in handleScroll above

// Cursor Effect (optional - adds a custom cursor trail)
const cursor = document.createElement('div');
cursor.style.cssText = `
    position: fixed;
    width: 20px;
    height: 20px;
    border: 2px solid var(--accent-color);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transition: transform 0.1s ease;
    display: none;
`;
document.body.appendChild(cursor);

let cursorX = 0;
let cursorY = 0;
let animationFrameId = null;

function updateCursor() {
    cursor.style.left = cursorX - 10 + 'px';
    cursor.style.top = cursorY - 10 + 'px';
    animationFrameId = null;
}

document.addEventListener('mousemove', (e) => {
    cursor.style.display = 'block';
    cursorX = e.clientX;
    cursorY = e.clientY;
    
    if (!animationFrameId) {
        animationFrameId = requestAnimationFrame(updateCursor);
    }
});

// Scale cursor on clickable elements
const clickables = document.querySelectorAll('a, button, .btn');
clickables.forEach(el => {
    el.addEventListener('mouseenter', () => {
        cursor.style.transform = 'scale(1.5)';
        cursor.style.borderColor = '#fff';
    });
    el.addEventListener('mouseleave', () => {
        cursor.style.transform = 'scale(1)';
        cursor.style.borderColor = 'var(--accent-color)';
    });
});

console.log('%c Portfolio Loaded Successfully! ', 'background: #00ff88; color: #000; font-size: 20px; font-weight: bold; padding: 10px;');
console.log('%c Built with ❤️ by Mokotanin ', 'background: #000; color: #00ff88; font-size: 14px; padding: 5px;');
