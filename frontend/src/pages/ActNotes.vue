<template>
    <div class="act-notes-page">
      <h1>Заметки активностей</h1>
      
      <ActNoteForm
        v-if="editingNote"
        :note="editingNote"
        :acts="acts"
        @saved="handleNoteSaved"
        @cancelled="cancelEdit"
      />
      
      <div v-else class="create-form">
        <h2>Создать заметку</h2>
        <form @submit.prevent="createNote">
          <div>
            <label>Активность:</label>
            <select v-model="form.act_id">
              <option :value="null">Нет</option>
              <option v-for="act in acts" :key="act.id" :value="act.id">
                {{ act.title }}
              </option>
            </select>
          </div>
          <div>
              <label>Время создания:</label>
              <input v-model="form.created_at" type="datetime-local" />
              <small class="hint">Оставьте пустым для текущего времени</small>
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
        <select v-model="filterActId" @change="loadNotes">
          <option :value="null">Все активности</option>
          <option v-for="act in acts" :key="act.id" :value="act.id">
            {{ act.title }}
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
                <p v-if="note.act_id" class="act-name">
                  Активность: {{ getActName(note.act_id) }}
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
  import ActNoteForm from '@/components/ActNoteForm.vue'
  
  const notes = ref([])
  const acts = ref([])
  const editingNote = ref(null)
  const filterActId = ref(null)
  
  const form = ref({
    content: '',
    act_id: null,
    created_at: null
  })
  
  const renderMarkdown = (text) => {
    if (!text) return ''
    return marked(text)
  }
  
  const createNote = async () => {
    try {
      await axios.post('/api/v1/act-notes/', form.value)
      form.value = { content: '', act_id: null }
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
      await axios.delete(`/api/v1/act-notes/${id}`)
      loadNotes()
    } catch (error) {
      console.error('Ошибка удаления:', error)
      alert('Ошибка удаления заметки')
    }
  }
  
  const loadNotes = async () => {
    try {
      let url = '/api/v1/act-notes/'
      if (filterActId.value) {
        url += `?act_id=${filterActId.value}`
      }
      const response = await axios.get(url)
      notes.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки заметок:', error)
    }
  }
  
  const loadActs = async () => {
    try {
      const response = await axios.get('/api/v1/acts/')
      acts.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки активностей:', error)
    }
  }
  
  const getActName = (id) => {
    const act = acts.value.find(a => a.id === id)
    return act ? act.title : ''
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
    loadActs()
  })
  </script>
  
  <style scoped>
  .act-notes-page {
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
  
  .act-name {
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