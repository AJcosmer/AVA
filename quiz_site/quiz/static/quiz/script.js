let questions = [];
let currentQuestion = 0;
let score = 0;
let timer;
let timePerQuestion = 15;
let selectedAnswers = [];
let token = null;

function register() {
  const username = document.getElementById("new-username").value;
  const password = document.getElementById("new-password").value;

  // Validar los datos antes de enviarlos
  if (!username || !password) {
    document.getElementById("register-error").textContent = 'Usuario y contraseña son requeridos.';
    return;
  }

  fetch("/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ 
      username: username, 
      password: password, 
      email: document.getElementById("new-email").value,
      first_name: document.getElementById("new-first-name").value,
      last_name: document.getElementById("new-last-name").value
    })
  })
  .then(response => {
    if (!response.ok) {
      return response.json().then(data => { throw new Error(data.error || "Error al registrar") });
    }
    return response.json();  // Expecting a JSON response
  })
  .then(data => {
    if (data.message) {
      alert(data.message);  // Show success message
      toggleForm();  // Switch to login form
    }
  })
  .catch(err => {
    document.getElementById("register-error").textContent = err.message;
  });
}

// Login con JWT
function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorDiv = document.getElementById("login-error");

  fetch("/api/token/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  })
    .then(res => {
      if (!res.ok) throw new Error("Credenciales inválidas");
      return res.json();
    })
    .then(data => {
      token = data.access;
      document.getElementById("login-container").classList.add("hidden");
      document.getElementById("config").classList.remove("hidden");
      document.getElementById("toggle-button").classList.add("hidden");
      errorDiv.innerText = "";
    })
    .catch(err => {
      errorDiv.innerText = err.message;
    });
}

function startGame() {
  const difficulty = document.getElementById("difficulty").value;
  const numQuestions = document.getElementById("num-questions").value;
  timePerQuestion = parseInt(document.getElementById("time-question").value);

  fetch(`/get-questions/?difficulty=${difficulty}&num=${numQuestions}&_=${Date.now()}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
    .then(res => {
      if (!res.ok) throw new Error("No autorizado o error al obtener preguntas");
      return res.json();
    })
    .then(data => {
      questions = data;
      score = 0;
      currentQuestion = 0;
      selectedAnswers = [];
      document.getElementById("config").style.display = "none";
      document.getElementById("score-container").classList.add("hidden");
      document.getElementById("quiz-container").classList.remove("hidden");
      showQuestion();
    })
    .catch(err => {
      alert(err.message);
    });
}

function showQuestion() {
  if (currentQuestion >= questions.length) {
    endGame();
    return;
  }

  const q = questions[currentQuestion];
  document.getElementById("question-number").innerText = `Pregunta ${currentQuestion + 1}/${questions.length}`;
  document.getElementById("question").innerText = q.question;

  const optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";
  q.options.forEach(opt => {
    const btn = document.createElement("button");
    btn.innerText = opt;
    btn.onclick = () => checkAnswer(btn);
    optionsDiv.appendChild(btn);
  });

  updateProgress();
  clearInterval(timer);
  startTimer();
}

function checkAnswer(selectedOption) {
  clearInterval(timer);
  const answer = selectedOption.innerText;
  selectedAnswers.push(answer);
  if (answer === questions[currentQuestion].answer) {
    score++;
  }
  currentQuestion++;
  showQuestion();
}

function nextQuestion() {
  clearInterval(timer);
  selectedAnswers.push(null);
  currentQuestion++;
  showQuestion();
}

function endGame() {
  document.getElementById("quiz-container").classList.add("hidden");
  document.getElementById("score-container").classList.remove("hidden");

  let mensaje = '';
  if (score === questions.length) {
    mensaje = "🎉 ¡Perfecto! Muchas felicitaciones.";
  } else if (score >= Math.ceil(questions.length / 2)) {
    mensaje = "✅ ¡Aprobado!";
  } else {
    mensaje = "❌ Mejor suerte la próxima vez.";
  }

  document.getElementById("final-score").innerHTML = `Puntaje: ${score}/${questions.length}<br>${mensaje}`;

  let reviewHTML = "<h3>Revisión de preguntas:</h3><ul>";
  questions.forEach((q, i) => {
    const userAnswer = selectedAnswers[i] ?? "No respondida";
    const isCorrect = userAnswer === q.answer;
    reviewHTML += `
      <li>
        <strong>${i + 1}. ${q.question}</strong><br>
        Tu respuesta: <span style="color:${isCorrect ? 'green' : 'red'}">${userAnswer}</span><br>
        Respuesta correcta: ${q.answer}
      </li>
    `;
  });
  reviewHTML += "</ul>";
  document.getElementById("review").innerHTML = reviewHTML;
}

function resetGame() {
  document.getElementById("quiz-container").classList.add("hidden");
  document.getElementById("score-container").classList.add("hidden");
  document.getElementById("config").style.display = "block";
}

function startTimer() {
  let countdown = timePerQuestion;
  const timerDisplay = document.getElementById("timer");
  timerDisplay.innerText = `Tiempo: ${countdown}s`;

  timer = setInterval(() => {
    countdown--;
    timerDisplay.innerText = `Tiempo: ${countdown}s`;
    if (countdown <= 0) {
      clearInterval(timer);
      selectedAnswers.push(null);
      currentQuestion++;
      showQuestion();
    }
  }, 1000);
}

function updateProgress() {
  const progress = document.getElementById("progress-bar");
  const percentage = ((currentQuestion) / questions.length) * 100;
  progress.style.width = `${percentage}%`;
}
