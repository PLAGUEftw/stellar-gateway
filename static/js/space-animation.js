// Stars Canvas Animation
class StarField {
    constructor() {
        this.canvas = document.getElementById('stars-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.stars = [];
        this.shootingStars = [];
        this.resize();
        this.createStars();
        this.animate();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createStars() {
        const starCount = Math.floor((this.canvas.width * this.canvas.height) / 3000);
        for (let i = 0; i < starCount; i++) {
            this.stars.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 2,
                opacity: Math.random(),
                speed: Math.random() * 0.02 + 0.005,
                twinkleSpeed: Math.random() * 0.03 + 0.01,
                color: this.getStarColor()
            });
        }
    }

    getStarColor() {
        const colors = ['#ffffff', '#00d4ff', '#ffd60a', '#ff006e', '#8338ec'];
        return Math.random() > 0.8 ? colors[Math.floor(Math.random() * colors.length)] : '#ffffff';
    }

    createShootingStar() {
        if (Math.random() < 0.01 && this.shootingStars.length < 3) {
            this.shootingStars.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height * 0.5,
                length: Math.random() * 80 + 50,
                speed: Math.random() * 10 + 6,
                opacity: 1,
                angle: Math.PI / 4
            });
        }
    }

    drawStar(star) {
        this.ctx.save();
        this.ctx.globalAlpha = Math.abs(Math.sin(Date.now() * star.twinkleSpeed)) * star.opacity;
        this.ctx.fillStyle = star.color;
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = star.color;
        this.ctx.beginPath();
        this.ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.restore();
    }

    drawShootingStar(star) {
        this.ctx.save();
        this.ctx.globalAlpha = star.opacity;
        const gradient = this.ctx.createLinearGradient(
            star.x, star.y,
            star.x - Math.cos(star.angle) * star.length,
            star.y - Math.sin(star.angle) * star.length
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        gradient.addColorStop(0.5, 'rgba(0, 212, 255, 0.5)');
        gradient.addColorStop(1, 'rgba(0, 212, 255, 0)');
        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = 2;
        this.ctx.lineCap = 'round';
        this.ctx.beginPath();
        this.ctx.moveTo(star.x, star.y);
        this.ctx.lineTo(
            star.x - Math.cos(star.angle) * star.length,
            star.y - Math.sin(star.angle) * star.length
        );
        this.ctx.stroke();
        this.ctx.restore();
    }

    update() {
        this.stars.forEach(star => {
            star.y += star.speed;
            if (star.y > this.canvas.height) {
                star.y = 0;
                star.x = Math.random() * this.canvas.width;
            }
        });

        this.shootingStars = this.shootingStars.filter(star => {
            star.x += Math.cos(star.angle) * star.speed;
            star.y += Math.sin(star.angle) * star.speed;
            star.opacity -= 0.015;
            return star.opacity > 0 && star.x < this.canvas.width + 100 && star.y < this.canvas.height + 100;
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.createShootingStar();
        this.stars.forEach(star => this.drawStar(star));
        this.shootingStars.forEach(star => this.drawShootingStar(star));
        this.update();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new StarField());
} else {
    new StarField();
}