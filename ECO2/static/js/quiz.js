// Quiz JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const quizContainer = document.querySelector('.quiz-container');
    if (!quizContainer) return;

    const lessonId = quizContainer.dataset.lessonId;
    let currentQuestionIndex = 0;
    let answers = {};
    const questions = document.querySelectorAll('.quiz-question');

    initializeQuiz();

    function initializeQuiz() {
        // Set up question navigation
        document.getElementById('next-question').addEventListener('click', nextQuestion);
        document.getElementById('prev-question').addEventListener('click', prevQuestion);
        document.getElementById('submit-quiz').addEventListener('click', submitQuiz);

        // Set up option selection
        document.querySelectorAll('.quiz-option').forEach(option => {
            option.addEventListener('click', selectOption);
        });

        updateProgress();
    }

    function selectOption(e) {
        const option = e.currentTarget;
        const questionDiv = option.closest('.quiz-question');
        const questionId = questionDiv.dataset.quizId;
        const value = option.dataset.value;

        // Remove previous selection
        questionDiv.querySelectorAll('.quiz-option').forEach(opt => {
            opt.classList.remove('selected');
        });

        // Select current option
        option.classList.add('selected');

        // Store answer
        answers[questionId] = value;

        // Enable next button
        document.getElementById('next-question').disabled = false;

        // If last question, show submit button
        if (currentQuestionIndex === questions.length - 1) {
            document.getElementById('next-question').style.display = 'none';
            document.getElementById('submit-quiz').style.display = 'inline-block';
        }
    }

    function nextQuestion() {
        if (currentQuestionIndex < questions.length - 1) {
            questions[currentQuestionIndex].style.display = 'none';
            currentQuestionIndex++;
            questions[currentQuestionIndex].style.display = 'block';

            // Show previous button
            document.getElementById('prev-question').style.display = 'inline-block';

            // Update next/submit button
            if (currentQuestionIndex === questions.length - 1) {
                document.getElementById('next-question').style.display = 'none';
                document.getElementById('submit-quiz').style.display = 'inline-block';
            }

            updateProgress();
        }
    }

    function prevQuestion() {
        if (currentQuestionIndex > 0) {
            questions[currentQuestionIndex].style.display = 'none';
            currentQuestionIndex--;
            questions[currentQuestionIndex].style.display = 'block';

            // Hide previous button if first question
            if (currentQuestionIndex === 0) {
                document.getElementById('prev-question').style.display = 'none';
            }

            // Show next button, hide submit button
            document.getElementById('next-question').style.display = 'inline-block';
            document.getElementById('submit-quiz').style.display = 'none';

            updateProgress();
        }
    }

    function updateProgress() {
        const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
        document.getElementById('quiz-progress').style.width = progress + '%';
        document.getElementById('quiz-progress-text').textContent =
            (currentQuestionIndex + 1) + '/' + questions.length;
    }

    function submitQuiz() {
        // Check if all questions are answered
        const totalQuestions = questions.length;
        const answeredQuestions = Object.keys(answers).length;

        if (answeredQuestions < totalQuestions) {
            EcoLearn.showNotification('Please answer all questions before submitting.', 'warning');
            return;
        }

        // Show loading state
        const submitBtn = document.getElementById('submit-quiz');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Submitting...';

        // Submit quiz
        fetch(`/submit_quiz/${lessonId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers: answers })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showResults(data);
            } else {
                EcoLearn.showNotification('Error submitting quiz. Please try again.', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit Quiz';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            EcoLearn.showNotification('Network error. Please check your connection and try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Submit Quiz';
        });
    }

    function showResults(data) {
        // Hide quiz form
        document.getElementById('quiz-form').style.display = 'none';

        // Create results display
        const resultsDiv = document.createElement('div');
        resultsDiv.className = 'quiz-results';
        resultsDiv.innerHTML = `
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: var(--primary-green);">Quiz Completed!</h2>
                <div style="font-size: 4rem; margin: 1rem 0; color: var(--primary-green);">🎉</div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
                <div class="stat-card">
                    <h3>Your Score</h3>
                    <div class="stat-number">${data.score}/${data.total}</div>
                    <p>${Math.round((data.score / data.total) * 100)}%</p>
                </div>

                <div class="stat-card">
                    <h3>Points Earned</h3>
                    <div class="stat-number">+${data.points_earned}</div>
                    <p>Eco Points</p>
                </div>
            </div>

            <div style="text-align: center;">
                <a href="{{ url_for('lessons') }}" class="btn btn-primary">Continue Learning</a>
                <a href="{{ url_for('dashboard') }}" class="btn btn-secondary" style="margin-left: 1rem;">View Dashboard</a>
            </div>
        `;

        quizContainer.appendChild(resultsDiv);

        // Animate results
        setTimeout(() => {
            resultsDiv.style.animation = 'fade-in 0.8s ease-out';
        }, 100);

        // Show points earned animation
        showPointsAnimation(data.points_earned);
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
        `;

        document.body.appendChild(pointsDiv);

        setTimeout(() => pointsDiv.remove(), 2000);
    }
});
