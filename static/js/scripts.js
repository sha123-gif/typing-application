let timeInterval;

function regenerateParagraph() {
    clearInterval(timeInterval); // Clear previous timer

    // Request new paragraph and time allocation from server
    $.ajax({
        url: '/generate_paragraph',
        type: 'GET',
        success: function(data) {
            displayParagraph(data.paragraph, data.time);
        }
    });
}

function displayParagraph(paragraph, time) {
    document.getElementById('original-text').innerText = paragraph;
    startTimer(time);
}

function startTimer(time) {
    let timer = time;
    displayTimer(timer);

    timeInterval = setInterval(function() {
        timer--;
        displayTimer(timer);
        if (timer <= 0) {
            clearInterval(timeInterval);
            document.getElementById('timer').innerText = "Time's up!";
        }
    }, 1000);
}

function displayTimer(time) {
    let minutes = Math.floor(time / 60);
    let seconds = time % 60;
    document.getElementById('timer').innerText = `Time remaining: ${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
}

function submitText() {
    clearInterval(timeInterval); // Stop timer
    let userText = document.getElementById('user-text').value;
    let originalText = document.getElementById('original-text').innerText;
    let startTime = new Date().getTime() / 1000;

    // Send data to server
    $.ajax({
        url: '/result',
        type: 'POST',
        data: {
            user_text: userText,
            original_text: originalText,
            start_time: startTime
        },
        success: function(result) {
            displayResult(result);
        }
    });
}

function displayResult(result) {
    let resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <p>Accuracy: ${result.accuracy.toFixed(2)}%</p>
    `;
    resultDiv.classList.add('fadeIn');
    resultDiv.classList.add('scaleIn');
}