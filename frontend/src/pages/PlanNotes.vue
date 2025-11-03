<template>
    <div class="plan-notes-page">
      <h1>Заметки планов</h1>
      
      <PlanNoteForm
        v-if="editingNote"
        :note="editingNote"
        :plans="plans"
        @saved="handleNoteSaved"
        @cancelled="cancelEdit"
      />
      
      <div v-else class="create-form">
        <h2>Создать заметку</h2>
        <form @submit.prevent="createNote">
          <div>
            <label>План:</label>
            <select v-model="form.plan_id">
              <option :value="null">Нет</option>
              <option v-for="plan in plans" :key="plan.id" :value="plan.id">
                {{ plan.title }}
              </option>
            </select>
          </div>
          <div>
            <label>Содержимое:</label>
            <textarea v-model="form.content" required></textarea>
          </div>
          <button type="submit">Создать</button>
        </form>
      </div>
  
      <hr/>
  
      <!-- Фильтр -->
      <div class="filters">
        <select v-model="filterPlanId" @change="loadNotes">
          <option :value="null">Все планы</option>
          <option v-for="plan in plans" :key="plan.id" :value="plan.id">
            {{ plan.title }}
          </option>
        </select>
      </div>
  
      <div class="notes-list">
        <h2>Список заметок</h2>
        <div v-if="notes.length === 0" class="no-items">
          Заметок пока нет
        </div>
        <div v-else>
          <div v-for="note in notes" :key="note.id" class="note-item">
            <div class="note-header">
              <div>
                <p v-if="note.plan_id" class="plan-name">
                  План: {{ getPlanName(note.plan_id) }}
                </p>
                <small class="note-date">{{ formatDate(note.created_at) }}</small>
              </div>
              <div class="note-actions">
                <button @click="editNote(note)" class="edit-btn">✏️</button>
                <button @click="deleteNote(note.id)" class="delete-btn">🗑️</button>
              </div>
            </div>
            <div class="note-content">
              <div class="markdown-content" v-html="renderMarkdown(note.content)"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { marked } from 'marked'
  import PlanNoteForm from '@/components/PlanNoteForm.vue'
  
  const notes = ref([])
  const plans = ref([])
  const editingNote = ref(null)
  const filterPlanId = ref(null)
  
  const form = ref({
    content: '',
    plan_id: null,
    created_at: null
  })
  
  const renderMarkdown = (text) => {
    if (!text) return ''
    return marked(text)
  }
  
  const createNote = async () => {
    try {
      await axios.post('/api/v1/plan-notes/', form.value)
      form.value = { content: '', plan_id: null }
      loadNotes()
    } catch (error) {
      console.error('Ошибка создания заметки:', error)
      alert('Ошибка создания заметки')
    }
  }
  
  const editNote = (note) => {
    editingNote.value = note
  }
  
  const cancelEdit = () => {
    editingNote.value = null
  }
  
  const handleNoteSaved = () => {
    editingNote.value = null
    loadNotes()
  }
  
  const deleteNote = async (id) => {
    if (!confirm('Удалить заметку?')) return
    try {
      await axios.delete(`/api/v1/plan-notes/${id}`)
      loadNotes()
    } catch (error) {
      console.error('Ошибка удаления:', error)
      alert('Ошибка удаления заметки')
    }
  }
  
  const loadNotes = async () => {
    try {
      let url = '/api/v1/plan-notes/'
      if (filterPlanId.value) {
        url += `?plan_id=${filterPlanId.value}`
      }
      const response = await axios.get(url)
      notes.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки заметок:', error)
    }
  }
  
  const loadPlans = async () => {
    try {
      const response = await axios.get('/api/v1/plans/')
      plans.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки планов:', error)
    }
  }
  
  const getPlanName = (id) => {
    const plan = plans.value.find(p => p.id === id)
    return plan ? plan.title : ''
  }
  
  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  onMounted(() => {
    loadNotes()
    loadPlans()
  })
  </script>
  
  <style scoped>
  .plan-notes-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .create-form {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .create-form div {
    margin-bottom: 15px;
  }
  
  .create-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .create-form select,
  .create-form textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .create-form textarea {
    height: 150px;
    resize: vertical;
  }
  
  .filters {
    margin-bottom: 20px;
  }
  
  .filters select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .note-item {
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    background: white;
  }
  
  .note-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 10px;
  }
  
  .plan-name {
    font-weight: bold;
    color: #007bff;
    margin: 0 0 5px 0;
  }
  
  .note-date {
    color: #666;
    font-size: 12px;
  }
  
  .note-actions {
    display: flex;
    gap: 8px;
  }
  
  .edit-btn, .delete-btn {
    padding: 6px 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .edit-btn {
    background: #28a745;
    color: white;
  }
  
  .delete-btn {
    background: #dc3545;
    color: white;
  }
  
  .note-content {
    margin-top: 10px;
  }
  
  .markdown-content {
    line-height: 1.6;
  }
  
  .no-items {
    text-align: center;
    padding: 40px;
    color: #666;
  }
  </style>