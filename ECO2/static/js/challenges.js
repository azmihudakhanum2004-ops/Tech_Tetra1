// Challenges JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeChallengeActions();
    initializeCarbonCalculator();
});

function initializeChallengeActions() {
    // Join challenge buttons
    document.querySelectorAll('.join-challenge').forEach(button => {
        button.addEventListener('click', function() {
            const challengeId = this.dataset.challengeId;
            joinChallenge(challengeId, this);
        });
    });

    // Complete challenge buttons
    document.querySelectorAll('.complete-challenge').forEach(button => {
        button.addEventListener('click', function() {
            const challengeId = this.dataset.challengeId;
            completeChallenge(challengeId, this);
        });
    });
}

function joinChallenge(challengeId, button) {
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Joining...';

    fetch(`/join_challenge/${challengeId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update button and show success
                button.closest('.challenge-actions').innerHTML = `
                    <span style="color: var(--primary-green); font-weight: bold;">Challenge Joined!</span>
                    <span style="color: var(--primary-green); font-weight: bold;">In Progress</span>
                `;

                // Add challenge progress indicator
                const challengeCard = button.closest('.challenge-card');
                const progressDiv = document.createElement('div');
                progressDiv.className = 'challenge-progress';
                progressDiv.innerHTML = `
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Progress</span>
                        <span>0 days left</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%;"></div>
                    </div>
                `;
                challengeCard.insertBefore(progressDiv, challengeCard.querySelector('.challenge-actions'));

                // Animate the card
                challengeCard.classList.add('challenge-joined');

                EcoLearn.showNotification(data.message, 'success');
            } else {
                EcoLearn.showNotification(data.message, 'error');
                button.disabled = false;
                button.innerHTML = 'Join Challenge';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            EcoLearn.showNotification('Network error. Please try again.', 'error');
            button.disabled = false;
            button.innerHTML = 'Join Challenge';
        });
}

function completeChallenge(challengeId, button) {
    if (!confirm('Are you sure you want to mark this challenge as completed? This action cannot be undone.')) {
        return;
    }

    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Completing...';

    fetch(`/complete_challenge/${challengeId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update challenge card
            const challengeCard = button.closest('.challenge-card');
            challengeCard.querySelector('.challenge-actions').innerHTML = `
                <span style="color: var(--primary-green); font-weight: bold;">✓ Challenge Completed!</span>
            `;

            // Remove progress bar and add completion styling
            const progressDiv = challengeCard.querySelector('.challenge-progress');
            if (progressDiv) {
                progressDiv.innerHTML = `
                    <div style="text-align: center; padding: 0.5rem; background: #E8F5E8; border-radius: 8px;">
                        <span style="color: var(--primary-green); font-weight: bold;">✓ Challenge Completed!</span>
                    </div>
                `;
            }

            // Show points earned
            showPointsAnimation(data.points_earned);

            EcoLearn.showNotification(data.message, 'success');
        } else {
            EcoLearn.showNotification(data.message, 'error');
            button.disabled = false;
            button.innerHTML = 'Mark Complete';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        EcoLearn.showNotification('Network error. Please try again.', 'error');
        button.disabled = false;
        button.innerHTML = 'Mark Complete';
    });
}

function showPointsAnimation(points) {
    const pointsDiv = document.createElement('div');
    pointsDiv.textContent = `+${points} Points!`;
    pointsDiv.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--primary-green);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        z-index: 1000;
        animation: points-float 2s ease-out forwards;
        box-shadow: 0 4px 20px rgba(46, 139, 87, 0.3);
    `;

    document.body.appendChild(pointsDiv);

    setTimeout(() => pointsDiv.remove(), 2000);
}

// Carbon Footprint Calculator
function initializeCarbonCalculator() {
    const calculator = document.getElementById('carbon-calculator');
    if (!calculator) return;

    calculator.addEventListener('submit', function(e) {
        e.preventDefault();
        calculateFootprint();
    });
}

function calculateFootprint() {
    const formData = new FormData(document.getElementById('carbon-calculator'));
    const data = Object.fromEntries(formData);

    // Simple carbon footprint calculation (tons CO2 per year)
    let footprint = 0;

    // Electricity (assuming average emissions factor)
    footprint += (parseFloat(data.electricity) || 0) * 12 * 0.0005; // kWh to tons CO2

    // Car travel (assuming average car emissions)
    footprint += (parseFloat(data.car_km) || 0) * 12 * 0.0002; // km to tons CO2

    // Public transport (lower emissions)
    footprint += (parseFloat(data.bus_km) || 0) * 12 * 0.00008; // km to tons CO2

    // Diet factor
    const dietFactors = {
        'average': 1,
        'vegetarian': 0.8,
        'vegan': 0.6
    };
    footprint += 2.5 * (dietFactors[data.diet] || 1); // Base diet emissions

    // Waste factor
    const wasteFactors = {
        'low': 0.8,
        'medium': 1,
        'high': 1.2
    };
    footprint += 0.5 * (wasteFactors[data.waste] || 1); // Base waste emissions

    displayFootprintResults(footprint);
}

function displayFootprintResults(footprint) {
    const resultsDiv = document.getElementById('carbon-results');
    resultsDiv.innerHTML = '';

    const roundedFootprint = footprint.toFixed(2);

    // Determine comparison and recommendations
    let comparison = '';
    let recommendations = [];

    if (footprint < 2) {
        comparison = 'Excellent! Your footprint is below the global average.';
        recommendations = [
            'Keep up the great work!',
            'Consider mentoring others on sustainable living.',
            'Share your tips on social media.'
        ];
    } else if (footprint < 4) {
        comparison = 'Good! Your footprint is around the global average.';
        recommendations = [
            'Try reducing meat consumption.',
            'Use public transport more often.',
            'Consider installing solar panels.'
        ];
    } else if (footprint < 6) {
        comparison = 'Your footprint is above average. There\'s room for improvement!';
        recommendations = [
            'Reduce air travel when possible.',
            'Switch to a more fuel-efficient vehicle.',
            'Implement recycling and composting.'
        ];
    } else {
        comparison = 'Your footprint is quite high. Let\'s work on reducing it!';
        recommendations = [
            'Consider lifestyle changes for significant impact.',
            'Join environmental challenges on EcoLearn.',
            'Calculate your footprint regularly to track progress.'
        ];
    }

    resultsDiv.innerHTML = `
        <div class="feature-card" data-animate="fade-in">
            <h3 style="text-align: center; margin-bottom: 1rem; color: var(--dark-green);">Your Carbon Footprint</h3>

            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 3rem; font-weight: bold; color: var(--primary-green); margin-bottom: 0.5rem;">
                    ${roundedFootprint}
                </div>
                <div style="font-size: 1.2rem; color: #666;">tons CO₂ per year</div>
            </div>

            <div style="background: var(--light-gray); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <p style="margin-bottom: 0.5rem;"><strong>Global Comparison:</strong></p>
                <p>${comparison}</p>
                <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
                    Global average: ~4.5 tons CO₂ per person per year
                </p>
            </div>

            <div style="margin-bottom: 1.5rem;">
                <h4 style="color: var(--dark-green); margin-bottom: 1rem;">Recommendations:</h4>
                <ul style="padding-left: 1.5rem;">
                    ${recommendations.map(rec => `<li style="margin-bottom: 0.5rem;">${rec}</li>`).join('')}
                </ul>
            </div>

            <div style="text-align: center;">
                <button onclick="location.reload()" class="btn btn-secondary">Recalculate</button>
                <a href="{{ url_for('challenges') }}" class="btn btn-primary" style="margin-left: 1rem;">Join Challenges</a>
            </div>
        </div>
    `;

    // Animate the results
    setTimeout(() => {
        resultsDiv.querySelector('.feature-card').style.animation = 'fade-in 0.8s ease-out';
    }, 100);
}

// Make functions globally available
window.challengeActions = {
    joinChallenge,
    completeChallenge,
    showPointsAnimation
};

window.carbonCalculator = {
    calculateFootprint,
    displayFootprintResults
};
