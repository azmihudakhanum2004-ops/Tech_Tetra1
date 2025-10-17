// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboardCharts();
    initializeProgressAnimations();
    updateLiveStats();
});

function initializeDashboardCharts() {
    // Simple progress chart using CSS (could be enhanced with Chart.js if needed)
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const progress = bar.getAttribute('data-progress') || 0;
        setTimeout(() => {
            bar.style.width = progress + '%';
        }, 500);
    });
}

function initializeProgressAnimations() {
    // Animate stat numbers
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent.replace(/[^\d]/g, '')) || 0;
        animateNumber(stat, 0, target, 1000);
    });
}

function animateNumber(element, start, end, duration) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (end - start) * easeOutQuart);

        element.textContent = EcoLearn.formatNumber(current);

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function updateLiveStats() {
    // Update user progress stats every 30 seconds
    setInterval(() => {
        fetch('/api/user_progress')
            .then(response => response.json())
            .then(data => {
                updateProgressDisplay(data);
            })
            .catch(error => {
                console.error('Error updating live stats:', error);
            });
    }, 30000);
}

function updateProgressDisplay(data) {
    // Update lesson completion
    const lessonStat = document.querySelector('.stat-number');
    if (lessonStat && lessonStat.nextElementSibling && lessonStat.nextElementSibling.textContent.includes('Lessons Completed')) {
        const currentValue = parseInt(lessonStat.textContent);
        if (currentValue !== data.completed_lessons) {
            animateNumber(lessonStat, currentValue, data.completed_lessons, 500);
        }
    }

    // Update progress bars
    const lessonProgressBar = document.querySelector('.progress-fill[data-progress]');
    if (lessonProgressBar) {
        const progressPercent = Math.round((data.completed_lessons / data.total_lessons) * 100);
        lessonProgressBar.style.width = progressPercent + '%';
    }

    // Show notification for new completion
    if (data.completed_lessons > parseInt(document.querySelector('.stat-number').textContent || 0)) {
        EcoLearn.showNotification('New lesson completed! Keep up the great work!', 'success');
    }
}

// Activity feed enhancements
function enhanceActivityFeed() {
    const activities = document.querySelectorAll('.activity-item');

    activities.forEach((activity, index) => {
        // Add hover effects
        activity.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.background = 'var(--light-gray)';
        });

        activity.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
            this.style.background = 'transparent';
        });

        // Add click to expand (if needed)
        activity.addEventListener('click', function() {
            // Could expand to show more details
            this.classList.toggle('expanded');
        });
    });
}

// Quick actions
function initializeQuickActions() {
    const quickActionButtons = document.querySelectorAll('.btn');

    quickActionButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add loading state
            if (this.href && !this.href.includes('#')) {
                this.innerHTML = '<span class="loading"></span> Loading...';
            }
        });
    });
}

// Achievement notifications
function checkForNewAchievements() {
    // This would typically check with the server for new badges earned
    // For now, we'll simulate this with local storage

    const lastCheck = localStorage.getItem('lastAchievementCheck');
    const now = Date.now();

    if (!lastCheck || (now - parseInt(lastCheck)) > 3600000) { // Check every hour
        // Simulate checking for new achievements
        setTimeout(() => {
            showAchievementNotification('Eco Warrior', 'Completed 5 challenges!');
        }, 2000);

        localStorage.setItem('lastAchievementCheck', now.toString());
    }
}

function showAchievementNotification(badgeName, description) {
    const notification = document.createElement('div');
    notification.className = 'achievement-notification';
    notification.innerHTML = `
        <div style="display: flex; align-items: center; background: var(--primary-green); color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);">
            <div style="font-size: 2rem; margin-right: 1rem;">🏆</div>
            <div>
                <h4 style="margin: 0; font-size: 1.1rem;">New Achievement!</h4>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">${badgeName}: ${description}</p>
            </div>
        </div>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        animation: slide-in 0.5s ease-out;
        cursor: pointer;
    `;

    notification.addEventListener('click', () => {
        notification.style.animation = 'fade-out 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    });

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'fade-out 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Initialize all dashboard features
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboardCharts();
    initializeProgressAnimations();
    initializeQuickActions();
    enhanceActivityFeed();
    updateLiveStats();
    checkForNewAchievements();
});

// Add CSS for achievement notifications
const style = document.createElement('style');
style.textContent = `
@keyframes fade-out {
    to {
        opacity: 0;
        transform: translateX(100%);
    }
}
.achievement-notification {
    max-width: 300px;
}
`;
document.head.appendChild(style);
