// Mobile Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });
}

// Auto-hide flash messages after 5 seconds
setTimeout(() => {
    document.querySelectorAll('.flash').forEach(flash => {
        flash.style.animation = 'fadeOut 0.5s forwards';
        setTimeout(() => flash.remove(), 500);
    });
}, 5000);

// Animated counter for stats
const animateCounters = () => {
    const counters = document.querySelectorAll('.stat-number[data-count]');
    const speed = 200;

    counters.forEach(counter => {
        const animate = () => {
            const target = +counter.getAttribute('data-count');
            const count = +counter.innerText.replace(/,/g, '');
            const increment = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + increment).toLocaleString();
                setTimeout(animate, 10);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };
        animate();
    });
};

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            if (entry.target.classList.contains('stats')) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .stats, .planet-card, .mission-card, .gallery-item').forEach(el => {
    observer.observe(el);
});

// Cursor trail effect
const createCursorTrail = () => {
    const trails = [];
    const trailLength = 15;

    for (let i = 0; i < trailLength; i++) {
        const trail = document.createElement('div');
        trail.className = 'cursor-trail';
        trail.style.cssText = `
            position: fixed;
            width: ${8 - i * 0.4}px;
            height: ${8 - i * 0.4}px;
            background: radial-gradient(circle, #00d4ff, transparent);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            opacity: ${1 - i * 0.06};
            transition: transform 0.1s ease;
            mix-blend-mode: screen;
        `;
        document.body.appendChild(trail);
        trails.push(trail);
    }

    let mouseX = 0, mouseY = 0;
    const positions = Array(trailLength).fill({ x: 0, y: 0 });

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    const animateTrail = () => {
        positions.unshift({ x: mouseX, y: mouseY });
        positions.pop();

        trails.forEach((trail, i) => {
            trail.style.left = positions[i].x + 'px';
            trail.style.top = positions[i].y + 'px';
        });

        requestAnimationFrame(animateTrail);
    };

    animateTrail();
};

// Only create trail on desktop
if (window.matchMedia('(min-width: 768px)').matches && !window.matchMedia('(hover: none)').matches) {
    createCursorTrail();
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Parallax effect for nebulas
document.addEventListener('mousemove', (e) => {
    const nebulas = document.querySelectorAll('.nebula');
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    
    nebulas.forEach((nebula, i) => {
        const speed = (i + 1) * 0.5;
        nebula.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
    });
});

// Add visible class styles
const style = document.createElement('style');
style.textContent = `
    .feature-card, .planet-card, .mission-card, .gallery-item {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }
    .feature-card.visible, .planet-card.visible, .mission-card.visible, .gallery-item.visible {
        opacity: 1;
        transform: translateY(0);
    }
    .menu-toggle.active span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
    .menu-toggle.active span:nth-child(2) { opacity: 0; }
    .menu-toggle.active span:nth-child(3) { transform: rotate(-45deg) translate(7px, -6px); }
`;
document.head.appendChild(style);

// Password match validation for register
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm_password');

if (password && confirmPassword) {
    const validatePassword = () => {
        if (confirmPassword.value && password.value !== confirmPassword.value) {
            confirmPassword.style.borderColor = '#ef4444';
            confirmPassword.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15)';
        } else if (confirmPassword.value) {
            confirmPassword.style.borderColor = '#10b981';
            confirmPassword.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.15)';
        }
    };
    password.addEventListener('input', validatePassword);
    confirmPassword.addEventListener('input', validatePassword);
}

console.log('%c🚀 Welcome to Stellar Gateway!', 'color: #00d4ff; font-size: 20px; font-weight: bold; text-shadow: 0 0 10px #00d4ff;');
console.log('%cJourney through space, wonder to chase!', 'color: #ffd60a; font-size: 14px;');

const reveals = document.querySelectorAll('.reveal');

window.addEventListener('scroll', () => {
    reveals.forEach(el => {
        const top = el.getBoundingClientRect().top;
        if (top < window.innerHeight - 100) {
            el.classList.add('active');
        }
    });
});