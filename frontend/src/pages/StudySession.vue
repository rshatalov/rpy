<template>
  <div class="study-session-page">
    <h1>Учебная сессия</h1>
    

    <div v-if="sessions.length > 0 && !currentSession">

        <div v-for="session in sessions" :key="session.id">
            <h2>{{ session.name }}</h2>
            <p>{{ session.description }}</p>
            <p>{{ session.start_date }}</p>
            <p>{{ session.end_date }}</p>
            <p>{{ session.is_active }}</p>
            <p>{{ session.created_at }}</p>
            <button @click="startSession(session.id)">Начать сессию</button>
            <button @click="deleteSession(session.id)">Удалить сессию</button>

        </div>
    </div>
    <!-- Создание новой сессии -->
    <div v-if="!currentSession" class="create-session">
      <h2>Создать новую сессию</h2>
      <form @submit.prevent="createSession">
        <div>
          <label>Название сессии:</label>
          <input v-model="sessionForm.name" required placeholder="Например: Python основы">
        </div>
        <div>
          <label>Описание (необязательно):</label>
          <textarea v-model="sessionForm.description" placeholder="Описание сессии..."></textarea>
        </div>
        <button type="submit">Начать сессию</button>
      </form>
    </div>

    <!-- Активная сессия -->
    <div v-else class="active-session">
      <div class="session-header">
        <h2>{{ currentSession.name }}</h2>
        <div class="session-actions">
          <button @click="endSession" class="end-session-btn">
            Завершить сессию
          </button>
        </div>
      </div>

      <!-- Статистика сессии -->
      <div class="session-stats">
        <div class="stat-item">
          <span class="stat-label">Всего вопросов:</span>
          <span class="stat-value">{{ sessionStats.total_questions || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Легких:</span>
          <span class="stat-value easy">{{ sessionStats.easy_questions || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Средних:</span>
          <span class="stat-value medium">{{ sessionStats.medium_questions || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Сложных:</span>
          <span class="stat-value hard">{{ sessionStats.hard_questions || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Показано раз:</span>
          <span class="stat-value">{{ sessionStats.total_shows || 0 }}</span>
        </div>
      </div>

      <!-- Текущий вопрос -->
      <div v-if="currentQuestion" class="question-container">
        <div class="question-header">
          <h3>Вопрос #{{ currentQuestion.id }}</h3>
          <div class="question-meta">
            <span>Показан: {{ currentQuestionTimesShown }} раз</span>
          </div>
        </div>

        <div class="question-content">
          <div class="question-text">
            <div class="markdown-content" v-html="renderMarkdown(currentQuestion.q)"></div>
          </div>
          
          <div v-if="showAnswer" class="answer-text">
            <strong>Ответ:</strong>
            <div class="markdown-content" v-html="renderMarkdown(currentQuestion.a)"></div>
          </div>
          
          <div v-else class="answer-toggle">
            <button @click="showAnswer = true" class="show-answer-btn">
              Показать ответ
            </button>
          </div>
        </div>

        <!-- Оценка вопроса -->
        <div v-if="showAnswer" class="question-rating">
          <h4>Как вам этот вопрос?</h4>
          <div class="rating-buttons">
            <button @click="rateQuestion('easy')" class="rating-btn easy">
              😊 Легко
            </button>
            <button @click="rateQuestion('medium')" class="rating-btn medium">
              😐 Средне
            </button>
            <button @click="rateQuestion('hard')" class="rating-btn hard">
              😰 Сложно
            </button>
          </div>
        </div>
      </div>

      <!-- Нет вопросов -->
      <div v-else class="no-questions">
        <h3>Поздравляем! 🎉</h3>
        <p>Вы изучили все доступные вопросы в этой сессии.</p>
        <button @click="endSession" class="end-session-btn">
          Завершить сессию
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

// Настройка marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
})

const sessions = ref([])
const currentSession = ref(null)
const currentQuestion = ref(null)
const currentQuestionTimesShown = ref(0)
const showAnswer = ref(false)
const sessionStats = ref({})

const sessionForm = ref({
  name: '',
  description: ''
})

const renderMarkdown = (text) => {
  if (!text) return ''
  return marked(text)
}

const getSessions = async () => {
  try {
    const response = await axios.get('/api/v1/study-sessions/')
    sessions.value = response.data
    console.log(sessions.value)
  } catch (error) {
    console.error('Ошибка получения сессий:', error)
  }
}

const startSession = async (sessionId) => {
    const response = await axios.get(`/api/v1/study-sessions/${sessionId}`)
    currentSession.value = response.data
    await loadSessionStats()
    await getNextQuestion()

}
const createSession = async () => {
  try {
    const response = await axios.post('/api/v1/study-sessions/', sessionForm.value)
    currentSession.value = response.data
    sessionForm.value = { name: '', description: '' }
    await loadSessionStats()
    await getNextQuestion()
  } catch (error) {
    console.error('Ошибка создания сессии:', error)
    alert('Ошибка создания сессии')
  }
}

const deleteSession = async (sessionId) => {
  try {
    await axios.delete(`http://localhost:8000/api/v1/study-sessions/${sessionId}`)
    getSessions()
    currentSession.value = null
    currentQuestion.value = null
    showAnswer.value = false
  } catch (error) {
    console.error('Ошибка удаления сессии:', error)
  }
}

const endSession = async () => {
  if (!currentSession.value) return
  
  try {
    await axios.post(`/api/v1/study-sessions/${currentSession.value.id}/end`)
    currentSession.value = null
    currentQuestion.value = null
    showAnswer.value = false
  } catch (error) {
    console.error('Ошибка завершения сессии:', error)
  }
}

const getNextQuestion = async () => {
  if (!currentSession.value) return
  
  try {
    const response = await axios.get(`/api/v1/study-sessions/${currentSession.value.id}/next-question`)
    
    if (response.data.message) {
      // Нет доступных вопросов
      currentQuestion.value = null
      return
    }
    
    currentQuestion.value = response.data.question
    currentQuestionTimesShown.value = response.data.times_shown
    showAnswer.value = false
  } catch (error) {
    console.error('Ошибка получения вопроса:', error)
  }
}

const rateQuestion = async (rating) => {
  if (!currentSession.value || !currentQuestion.value) return
  
  try {
    await axios.post(`/api/v1/study-sessions/${currentSession.value.id}/rate-question`, {
      session_id: currentSession.value.id,
      question_id: currentQuestion.value.id,
      rating: rating
    })
    
    // Обновляем статистику
    await loadSessionStats()
    
    // Получаем следующий вопрос
    await getNextQuestion()
  } catch (error) {
    console.error('Ошибка оценки вопроса:', error)
  }
}

const loadSessionStats = async () => {
  if (!currentSession.value) return
  
  try {
    const response = await axios.get(`/api/v1/study-sessions/${currentSession.value.id}/statistics`)
    sessionStats.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
  }
}

onMounted(() => {
  // Можно добавить логику для восстановления активной сессии
  getSessions()
})
</script>

<style scoped>
.study-session-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.create-session {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.create-session form div {
  margin-bottom: 15px;
}

.create-session label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.create-session input,
.create-session textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.create-session textarea {
  height: 80px;
  resize: vertical;
}

.active-session {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e1e4e8;
}

.session-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
}

.stat-value.easy {
  color: #28a745;
}

.stat-value.medium {
  color: #ffc107;
}

.stat-value.hard {
  color: #dc3545;
}

.question-container {
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-meta {
  font-size: 12px;
  color: #666;
}

.question-content {
  margin-bottom: 20px;
}

.answer-toggle {
  text-align: center;
  margin: 20px 0;
}

.show-answer-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.show-answer-btn:hover {
  background: #0056b3;
}

.question-rating {
  border-top: 1px solid #e1e4e8;
  padding-top: 20px;
}

.question-rating h4 {
  margin-bottom: 15px;
  text-align: center;
}

.rating-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.rating-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.2s;
}

.rating-btn.easy {
  background: #d4edda;
  color: #155724;
}

.rating-btn.easy:hover {
  background: #c3e6cb;
}

.rating-btn.medium {
  background: #fff3cd;
  color: #856404;
}

.rating-btn.medium:hover {
  background: #ffeaa7;
}

.rating-btn.hard {
  background: #f8d7da;
  color: #721c24;
}

.rating-btn.hard:hover {
  background: #f5c6cb;
}

.end-session-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.end-session-btn:hover {
  background: #c82333;
}

.no-questions {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* Стили для Markdown контента */
.markdown-content {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #24292e;
}

.markdown-content p {
  margin-bottom: 12px;
}

.markdown-content code {
  background: #f6f8fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 85%;
  line-height: 1.2;
}

.markdown-content pre {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 12px;
  overflow-x: auto;
  margin: 16px 0;
  line-height: 1.2;
  font-size: 13px;
}

.markdown-content pre code {
  background: transparent;
  padding: 0;
  border-radius: 0;
  color: #e6edf3;
  line-height: 1.2;
  font-size: 13px;
}
</style>
