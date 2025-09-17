// Advanced Interactive Features with Vanilla JS and Libraries

// Particle Animation System
class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: 0, y: 0 };
        
        this.resize();
        this.init();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
        canvas.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX - canvas.offsetLeft;
            this.mouse.y = e.clientY - canvas.offsetTop;
        });
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    init() {
        for (let i = 0; i < 100; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 3 + 1,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach((particle, i) => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
            
            // Mouse interaction
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 100) {
                particle.x -= dx * 0.02;
                particle.y -= dy * 0.02;
            }
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(91, 140, 255, ${particle.opacity})`;
            this.ctx.fill();
            
            // Draw connections
            this.particles.slice(i + 1).forEach(otherParticle => {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(otherParticle.x, otherParticle.y);
                    this.ctx.strokeStyle = `rgba(91, 140, 255, ${0.2 * (1 - distance / 150)})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Smooth Scroll with Intersection Observer
class SmoothAnimations {
    constructor() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1 });
        
        this.init();
    }
    
    init() {
        // Add animation classes
        const style = document.createElement('style');
        style.textContent = `
            .animate-on-scroll {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .animate-in {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
            .stagger-1 { transition-delay: 0.1s; }
            .stagger-2 { transition-delay: 0.2s; }
            .stagger-3 { transition-delay: 0.3s; }
            .stagger-4 { transition-delay: 0.4s; }
        `;
        document.head.appendChild(style);
        
        // Observe elements
        document.querySelectorAll('.card, .section-title, .hero-title').forEach((el, i) => {
            el.classList.add('animate-on-scroll');
            if (i % 4 === 0) el.classList.add('stagger-1');
            else if (i % 4 === 1) el.classList.add('stagger-2');
            else if (i % 4 === 2) el.classList.add('stagger-3');
            else el.classList.add('stagger-4');
            
            this.observer.observe(el);
        });
    }
}

// Advanced Form Validation
class FormValidator {
    constructor(form) {
        this.form = form;
        this.rules = {};
        this.init();
    }
    
    addRule(fieldName, validator, message) {
        if (!this.rules[fieldName]) this.rules[fieldName] = [];
        this.rules[fieldName].push({ validator, message });
    }
    
    init() {
        this.form.addEventListener('submit', (e) => {
            if (!this.validate()) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        this.form.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('blur', () => this.validateField(field.name));
            field.addEventListener('input', () => this.clearError(field.name));
        });
    }
    
    validate() {
        let isValid = true;
        Object.keys(this.rules).forEach(fieldName => {
            if (!this.validateField(fieldName)) isValid = false;
        });
        return isValid;
    }
    
    validateField(fieldName) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        const rules = this.rules[fieldName] || [];
        
        for (let rule of rules) {
            if (!rule.validator(field.value)) {
                this.showError(fieldName, rule.message);
                return false;
            }
        }
        
        this.clearError(fieldName);
        return true;
    }
    
    showError(fieldName, message) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        field.style.borderColor = '#ef4444';
        
        let errorEl = field.parentNode.querySelector('.error-message');
        if (!errorEl) {
            errorEl = document.createElement('div');
            errorEl.className = 'error-message';
            errorEl.style.cssText = 'color: #ef4444; font-size: 0.875rem; margin-top: 4px;';
            field.parentNode.appendChild(errorEl);
        }
        errorEl.textContent = message;
    }
    
    clearError(fieldName) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        field.style.borderColor = 'rgba(91,140,255,.2)';
        
        const errorEl = field.parentNode.querySelector('.error-message');
        if (errorEl) errorEl.remove();
    }
}

// Interactive Code Editor
class CodeEditor {
    constructor(container, language = 'javascript') {
        this.container = container;
        this.language = language;
        this.init();
    }
    
    init() {
        this.container.innerHTML = `
            <div style="background: #0d1117; border-radius: 12px; overflow: hidden; border: 1px solid rgba(91,140,255,.3);">
                <div style="background: rgba(91,140,255,.1); padding: 12px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(91,140,255,.2);">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #ef4444;"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #f59e0b;"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #22c55e;"></div>
                    <span style="color: #9fb0d9; font-size: 0.9rem; margin-left: 12px;">${this.language}</span>
                </div>
                <textarea style="
                    width: 100%; 
                    height: 300px; 
                    background: transparent; 
                    border: none; 
                    color: #e7ecf7; 
                    font-family: 'Courier New', monospace; 
                    font-size: 14px; 
                    padding: 20px; 
                    resize: none; 
                    outline: none;
                " placeholder="// Start coding here..."></textarea>
            </div>
        `;
        
        const textarea = this.container.querySelector('textarea');
        textarea.addEventListener('input', () => this.highlightSyntax(textarea));
    }
    
    highlightSyntax(textarea) {
        // Simple syntax highlighting
        let code = textarea.value;
        const keywords = ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return'];
        
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            code = code.replace(regex, `<span style="color: #5b8cff;">${keyword}</span>`);
        });
        
        // This is a simplified version - in production, use a proper syntax highlighter
    }
}

// Performance Monitor
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            loadTime: 0,
            renderTime: 0,
            memoryUsage: 0
        };
        this.init();
    }
    
    init() {
        // Measure page load time
        window.addEventListener('load', () => {
            this.metrics.loadTime = performance.now();
            this.updateDisplay();
        });
        
        // Monitor memory usage (if available)
        if ('memory' in performance) {
            setInterval(() => {
                this.metrics.memoryUsage = performance.memory.usedJSHeapSize / 1048576; // MB
                this.updateDisplay();
            }, 5000);
        }
    }
    
    updateDisplay() {
        const monitor = document.getElementById('performance-monitor');
        if (monitor) {
            monitor.innerHTML = `
                <div style="position: fixed; top: 80px; left: 20px; background: rgba(11,18,34,.9); padding: 12px; border-radius: 8px; font-size: 0.8rem; color: #9fb0d9; z-index: 999;">
                    Load: ${this.metrics.loadTime.toFixed(0)}ms<br>
                    Memory: ${this.metrics.memoryUsage.toFixed(1)}MB
                </div>
            `;
        }
    }
}

// Initialize all features
document.addEventListener('DOMContentLoaded', function() {
    // Add particle background to hero sections
    const heroSections = document.querySelectorAll('.hero');
    heroSections.forEach(hero => {
        const canvas = document.createElement('canvas');
        canvas.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;';
        hero.style.position = 'relative';
        hero.appendChild(canvas);
        new ParticleSystem(canvas);
    });
    
    // Initialize smooth animations
    new SmoothAnimations();
    
    // Add form validation to contact forms (exclude auth forms)
    const forms = document.querySelectorAll('form:not(.auth-form)');
    forms.forEach(form => {
        const validator = new FormValidator(form);
        
        // Add common validation rules
        validator.addRule('email', (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value), 'Please enter a valid email address');
        validator.addRule('name', (value) => value.length >= 2, 'Name must be at least 2 characters');
        validator.addRule('message', (value) => value.length >= 10, 'Message must be at least 10 characters');
    });
    
    // Add code editor to API docs
    const codeContainers = document.querySelectorAll('.code-editor');
    codeContainers.forEach(container => {
        new CodeEditor(container, container.dataset.language || 'javascript');
    });
    
    // Initialize performance monitor in development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        new PerformanceMonitor();
        document.body.insertAdjacentHTML('beforeend', '<div id="performance-monitor"></div>');
    }
    
    // Add smooth scrolling for anchor links
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
    
    // Removed problematic loading state code that was preventing form submission
});