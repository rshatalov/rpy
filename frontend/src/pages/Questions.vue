<template>
    <div class="questions-page">
      <h1>Вопросы</h1>

    <QuestionForm 
      :available-tags="availableTags"
      @saved="handleQuestionSaved"
    />
      <hr/>

      <!-- Фильтры по тегам -->
      <div class="filters-section">
        <h2>Фильтры по тегам</h2>
        
        <!-- Включающие фильтры -->
        <div class="filter-group">
          <h3>Показать вопросы с тегами:</h3>
          <div class="tags-filter">
            <div v-for="tag in availableTags" :key="tag.slug" class="tag-filter-item">
              <input 
                type="checkbox" 
                :id="`include-${tag.slug}`"
                :value="tag.slug"
                v-model="includeTags"
              >
              <label :for="`include-${tag.slug}`" class="tag-label include">
                {{ tag.title }}
              </label>
            </div>
          </div>
        </div>
        
        <!-- Исключающие фильтры -->
        <div class="filter-group">
          <h3>Исключить вопросы с тегами:</h3>
          <div class="tags-filter">
            <div v-for="tag in availableTags" :key="tag.slug" class="tag-filter-item">
              <input 
                type="checkbox" 
                :id="`exclude-${tag.slug}`"
                :value="tag.slug"
                v-model="excludeTags"
              >
              <label :for="`exclude-${tag.slug}`" class="tag-label exclude">
                {{ tag.title }}
              </label>
            </div>
          </div>
        </div>
        
        <!-- Кнопки управления фильтрами -->
        <div class="filter-controls">
          <div class="filter-buttons">
            <button @click="clearFilters" class="clear-filters-btn">
              Очистить фильтры
            </button>
            <button @click="toggleRandomSort" class="random-sort-btn" :class="{ active: isRandomSort }">
              {{ isRandomSort ? 'Отключить случайную сортировку' : 'Случайная сортировка' }}
            </button>
          </div>
          <span class="filter-info">
            Показано: {{ filteredQuestions.length }} из {{ questions.length }} вопросов
          </span>
        </div>
      </div>

      <hr/>
  
      <!-- Список вопросов -->
      <div class="questions-list">
        <h2>Список вопросов</h2>
        
        <div v-if="filteredQuestions.length === 0" class="no-questions">
          <div v-if="questions.length === 0">
            Вопросов пока нет
          </div>
          <div v-else>
            Нет вопросов, соответствующих фильтрам
          </div>
        </div>
        
        <div v-else>
          <div v-for="question in filteredQuestions" :key="question.id" class="question-item">
            <div class="question-header">
                <div class="question-tags" v-if="question.tags && question.tags.length > 0">
                <span v-for="tag in question.tags" :key="tag.slug" class="tag">
                  {{ tag.title }}
                </span>
              </div>
            <div class="question-actions">
              <span class="difficulty" :class="question.difficulty">
                {{ getDifficultyText(question.difficulty) }}
              </span>
              <button 
                @click="editQuestion(question)" 
                class="edit-btn"
                title="Редактировать вопрос"
              >
                ✏️
              </button>
              <!-- Кнопка удаления с иконкой -->
              <button 
                @click="deleteQuestion(question.id)" 
                class="delete-btn"
                title="Удалить вопрос"
              >
                🗑️
              </button>
            </div>
            </div>
            
            <div v-if="editingQuestion && editingQuestion.id === question.id" class="edit-form">
            <QuestionForm 
              :question="editingQuestion"
              :available-tags="availableTags"
              @saved="handleQuestionSaved"
              @cancelled="cancelEdit"
            />
          </div>

            <div v-else class="question-content">
              <div class="question-text">
                <div class="markdown-content" v-html="renderMarkdown(question.q)"></div>
              </div>
              <hr/>
              
              <div class="answer-text">
                <div class="markdown-content" v-html="renderMarkdown(question.a)"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import hljs from 'highlight.js'
//import 'highlight.js/styles/github-dark.css'
import QuestionForm from '@/components/QuestionForm.vue'


marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
})

const form = ref({
  q: '',
  a: '',
  difficulty: '',
  tag_slugs: []
})

const availableTags = ref([])
const questions = ref([])
const editingQuestion = ref(null)

// Фильтры
const includeTags = ref([])
const excludeTags = ref([])

// Случайная сортировка
const isRandomSort = ref(false)
const randomOrder = ref([])


const renderMarkdown = (text) => {
  if (!text) return ''
  return marked(text)
}

// Вычисляемое свойство для фильтрации и сортировки вопросов
const filteredQuestions = computed(() => {
  let filtered = questions.value
  
  // Применяем фильтры по тегам
  if (includeTags.value.length > 0 || excludeTags.value.length > 0) {
    filtered = questions.value.filter(question => {
      const questionTagSlugs = question.tags ? question.tags.map(tag => tag.slug) : []
      
      // Проверяем включающие фильтры
      if (includeTags.value.length > 0) {
        const hasIncludeTag = includeTags.value.some(tagSlug => 
          questionTagSlugs.includes(tagSlug)
        )
        if (!hasIncludeTag) return false
      }
      
      // Проверяем исключающие фильтры
      if (excludeTags.value.length > 0) {
        const hasExcludeTag = excludeTags.value.some(tagSlug => 
          questionTagSlugs.includes(tagSlug)
        )
        if (hasExcludeTag) return false
      }
      
      return true
    })
  }
  
  // Применяем случайную сортировку
  if (isRandomSort.value && randomOrder.value.length > 0) {
    // Сортируем отфильтрованные вопросы согласно случайному порядку
    const questionMap = new Map(filtered.map(q => [q.id, q]))
    return randomOrder.value
      .map(id => questionMap.get(id))
      .filter(Boolean) // Убираем undefined (вопросы, которые не прошли фильтр)
  }
  
  return filtered
})

// Функции для управления фильтрами
const clearFilters = () => {
  includeTags.value = []
  excludeTags.value = []
}

// Функция для переключения случайной сортировки
const toggleRandomSort = () => {
  if (isRandomSort.value) {
    // Отключаем случайную сортировку
    isRandomSort.value = false
    randomOrder.value = []
  } else {
    // Включаем случайную сортировку
    isRandomSort.value = true
    generateRandomOrder()
  }
}

// Генерация случайного порядка
const generateRandomOrder = () => {
  const allQuestionIds = questions.value.map(q => q.id)
  // Алгоритм Fisher-Yates для перемешивания
  const shuffled = [...allQuestionIds]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  randomOrder.value = shuffled
}


const editQuestion = (question) => {
  editingQuestion.value = question
}

const cancelEdit = () => {
  editingQuestion.value = null
}

const handleQuestionSaved = () => {
  editingQuestion.value = null
  loadQuestions()
}


const deleteQuestion = async (questionId) => {
  if (!confirm('Вы уверены, что хотите удалить этот вопрос?')) {
    return
  }
  
  try {
    await axios.delete(`http://localhost:8000/api/v1/questions/${questionId}`)
    console.log('Вопрос удален')
    loadQuestions() // Перезагрузить список
  } catch (error) {
    console.error('Ошибка удаления вопроса:', error)
    alert('Ошибка при удалении вопроса')
  }
}

const loadQuestions = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/v1/questions')
        questions.value = response.data
    } catch (error) {
        console.error("Ошибка загрузки вопросов", error)
    }
}

const loadTags = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/tags/')
    availableTags.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки тегов:', error)
  }
}

// Вспомогательные функции
const getDifficultyText = (difficulty) => {
  const difficultyMap = {
    'easy': 'Легкая',
    'medium': 'Средняя', 
    'hard': 'Сложная'
  }
  return difficultyMap[difficulty] || ''
}


onMounted(() => {
    loadQuestions()
    loadTags()
})
</script>


<style scoped>
.questions-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* Стили для фильтров */
.filters-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #495057;
}

.tags-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-filter-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.tag-filter-item input[type="checkbox"] {
  margin: 0;
}

.tag-label {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.tag-label.include {
  background: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

.tag-label.include:hover {
  background: #c3e6cb;
}

.tag-label.exclude {
  background: #f8d7da;
  color: #721c24;
  border-color: #f5c6cb;
}

.tag-label.exclude:hover {
  background: #f5c6cb;
}

.filter-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #dee2e6;
}

.filter-buttons {
  display: flex;
  gap: 8px;
}

.clear-filters-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s;
}

.clear-filters-btn:hover {
  background: #545b62;
}

.random-sort-btn {
  background: #17a2b8;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.random-sort-btn:hover {
  background: #138496;
}

.random-sort-btn.active {
  background: #dc3545;
}

.random-sort-btn.active:hover {
  background: #c82333;
}

.filter-info {
  font-size: 12px;
  color: #6c757d;
}

.question-item {
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background: white;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-header h3 {
  margin: 0;
}

.question-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.difficulty {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.difficulty.easy {
  background: #d4edda;
  color: #155724;
}

.difficulty.medium {
  background: #fff3cd;
  color: #856404;
}

.difficulty.hard {
  background: #f8d7da;
  color: #721c24;
}

.edit-btn {
  background: #28a74600;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.edit-btn:hover {
  background: #21883700;
  transform: scale(1.25);
}


.delete-btn {
  background: #dc354600;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.delete-btn:hover {
  transform: scale(1.25);
}

.edit-form {
  margin-top: 15px;
  border-top: 1px solid #e1e4e8;
  padding-top: 15px;
}

/* .markdown-content {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  margin-top: 8px;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #24292e;
}

.markdown-content h1 {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 8px;
}

.markdown-content h2 {
  font-size: 1.3em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 6px;
}

.markdown-content p {
  margin-bottom: 12px;
}

.markdown-content code {
  background: #f6f8fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 85%;
}

.markdown-content pre {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
}

.markdown-content pre code {
  background: transparent;
  padding: 0;
  border-radius: 0;
  color: #ede6f3;
}

.markdown-content blockquote {
  border-left: 4px solid #dfe2e5;
  padding-left: 16px;
  margin: 16px 0;
  color: #6a737d;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 12px;
  padding-left: 20px;
}

.markdown-content li {
  margin-bottom: 4px;
}

.markdown-content table {
  border-collapse: collapse;
  margin: 16px 0;
  width: 100%;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #dfe2e5;
  padding: 8px 12px;
  text-align: left;
}

.markdown-content th {
  background: #f6f8fa;
  font-weight: 600;
} */




.question-content div {
  margin-bottom: 10px;
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  align-items: center;
}

.tag {
  background: #007bff;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.question-meta {
  color: #666;
  font-size: 12px;
}

.no-questions {
  text-align: center;
  color: #666;
  padding: 40px;
  font-style: italic;
}
</style>