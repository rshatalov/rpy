<template>
    <div class="acts-page">
      <h1>Активности</h1>
      
      <!-- Форма создания/редактирования -->
      <ActForm
        v-if="editingAct"
        :act="editingAct"
        :available-acts="acts"
        @saved="handleActSaved"
        @cancelled="cancelEdit"
      />
      
      <div v-else class="create-form">
        <h2>Создать активность</h2>
        <form @submit.prevent="createAct">
          <div>
            <label>Название:</label>
            <input v-model="form.title" required />
          </div>
          <div>
            <label>Дата начала:</label>
            <input v-model="form.start_date" type="date" />
          </div>
          <div>
            <label>Дата окончания:</label>
            <input v-model="form.end_date" type="date" />
          </div>
          <div>
            <label>
              <input v-model="form.hidden" type="checkbox" />
              Скрыта
            </label>
          </div>
          <div>
            <label>Родительская активность:</label>
            <select v-model="form.parent_id">
              <option :value="null">Нет</option>
              <option v-for="act in acts" :key="act.id" :value="act.id">
                {{ act.title }}
              </option>
            </select>
          </div>
          <button type="submit">Создать</button>
        </form>
      </div>
  
      <hr/>
  
      <!-- Список активностей -->
      <div class="acts-list">
        <h2>Список активностей</h2>
        <div v-if="acts.length === 0" class="no-items">
          Активностей пока нет
        </div>
        <div v-else>
          <div v-for="act in acts" :key="act.id" class="act-item">
            <div class="act-header">
              <h3>{{ act.title }}</h3>
              <div class="act-actions">
                <button @click="editAct(act)" class="edit-btn">✏️</button>
                <button @click="deleteAct(act.id)" class="delete-btn">🗑️</button>
              </div>
            </div>
            <div class="act-content">
              <p v-if="act.start_date">Начало: {{ formatDate(act.start_date) }}</p>
              <p v-if="act.end_date">Окончание: {{ formatDate(act.end_date) }}</p>
              <p v-if="act.hidden" class="hidden-badge">Скрыта</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import ActForm from '@/components/ActForm.vue'
  import axios from 'axios'
  
  const acts = ref([])
  const editingAct = ref(null)
  const form = ref({
    title: '',
    start_date: null,
    end_date: null,
    hidden: false,
    parent_id: null
  })
  
  const createAct = async () => {
    try {
      await axios.post('http://localhost:8000/api/v1/acts/', form.value)
      form.value = { title: '', start_date: null, end_date: null, hidden: false, parent_id: null }
      loadActs()
    } catch (error) {
      console.error('Ошибка создания активности:', error)
    }
  }
  
  const editAct = (act) => {
    editingAct.value = act
  }
  
  const cancelEdit = () => {
    editingAct.value = null
  }
  
  const handleActSaved = () => {
    editingAct.value = null
    loadActs()
  }
  
  const deleteAct = async (id) => {
    if (!confirm('Удалить активность?')) return
    try {
          await axios.delete(`http://localhost:8000/api/v1/acts/${id}`)
          loadActs()
    } catch (error) {
      console.error('Ошибка удаления:', error)
    }
  }
  
  const loadActs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/acts/')
      acts.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки активностей:', error)
    }
  }
  
  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
  }
  
  onMounted(() => {
    loadActs()
  })
  </script>
  
  <style scoped>
  .acts-page {
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
  
  .create-form input,
  .create-form select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .act-item {
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    background: white;
  }
  
  .act-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .act-actions {
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
  
  .no-items {
    text-align: center;
    padding: 40px;
    color: #666;
  }
  </style>