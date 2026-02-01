/* AI for Product Managers - Course JS
   Data Trainers LLC - 2026 */

// ===== Quiz Engine =====
function initQuizzes() {
  document.querySelectorAll('.quiz').forEach(quiz => {
    const options = quiz.querySelectorAll('.quiz-option');
    const feedback = quiz.querySelector('.quiz-feedback');
    let answered = false;

    options.forEach(option => {
      option.addEventListener('click', () => {
        if (answered) return;
        answered = true;

        const isCorrect = option.dataset.correct === 'true';
        option.classList.add(isCorrect ? 'correct' : 'incorrect');

        // Show correct answer if wrong
        if (!isCorrect) {
          options.forEach(o => {
            if (o.dataset.correct === 'true') o.classList.add('correct');
          });
        }

        // Show feedback
        if (feedback) {
          const feedbackText = isCorrect
            ? (option.dataset.feedbackCorrect || feedback.dataset.correct || 'Correct!')
            : (option.dataset.feedbackIncorrect || feedback.dataset.incorrect || 'Not quite.');
          feedback.innerHTML = feedbackText;
          feedback.className = 'quiz-feedback show ' + (isCorrect ? 'callout callout-success' : 'callout callout-failure');
        }
      });
    });
  });
}

// ===== Collapsible Sections =====
function initCollapsibles() {
  document.querySelectorAll('.collapsible-toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      const content = toggle.nextElementSibling;
      const isOpen = content.style.maxHeight;
      content.style.maxHeight = isOpen ? null : content.scrollHeight + 'px';
      toggle.classList.toggle('open');
    });
  });
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
  initQuizzes();
  initCollapsibles();
});
