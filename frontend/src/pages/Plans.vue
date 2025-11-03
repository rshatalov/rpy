<template>
    <div class="plans-page">
      <h1>Планы</h1>
      
      <PlanForm
        v-if="editingPlan"
        :plan="editingPlan"
        :available-plans="plans"
        @saved="handlePlanSaved"
        @cancelled="cancelEdit"
      />
      
      <div v-else class="create-form">
        <h2>Создать план</h2>
        <form @submit.prevent="createPlan">
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
            <label>Родительский план:</label>
            <select v-model="form.parent_id">
              <option :value="null">Нет</option>
              <option v-for="plan in plans" :key="plan.id" :value="plan.id">
                {{ plan.title }}
              </option>
            </select>
          </div>
          <button type="submit">Создать</button>
        </form>
      </div>
  
      <hr/>
  
      <div class="plans-list">
        <h2>Список планов</h2>
        <div v-if="plans.length === 0" class="no-items">
          Планов пока нет
        </div>
        <div v-else>
          <div v-for="plan in plans" :key="plan.id" class="plan-item">
            <div class="plan-header">
              <h3>{{ plan.title }}</h3>
              <div class="plan-actions">
                <button @click="editPlan(plan)" class="edit-btn">✏️</button>
                <button @click="deletePlan(plan.id)" class="delete-btn">🗑️</button>
              </div>
            </div>
            <div class="plan-content">
              <p v-if="plan.start_date">Начало: {{ formatDate(plan.start_date) }}</p>
              <p v-if="plan.end_date">Окончание: {{ formatDate(plan.end_date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import PlanForm from '@/components/PlanForm.vue'
  
  const plans = ref([])
  const editingPlan = ref(null)
  const form = ref({
    title: '',
    start_date: null,
    end_date: null,
    parent_id: null
  })
  
  const createPlan = async () => {
    try {
      const payload = {
        title: form.value.title,
        start_date: form.value.start_date || null,
        end_date: form.value.end_date || null,
        parent_id: form.value.parent_id
      }
      await axios.post('/api/v1/plans/', payload)
      form.value = { title: '', start_date: null, end_date: null, parent_id: null }
      loadPlans()
    } catch (error) {
      console.error('Ошибка создания плана:', error)
      alert('Ошибка создания плана')
    }
  }
  
  const editPlan = (plan) => {
    editingPlan.value = plan
  }
  
  const cancelEdit = () => {
    editingPlan.value = null
  }
  
  const handlePlanSaved = () => {
    editingPlan.value = null
    loadPlans()
  }
  
  const deletePlan = async (id) => {
    if (!confirm('Удалить план?')) return
    try {
      await axios.delete(`/api/v1/plans/${id}`)
      loadPlans()
    } catch (error) {
      console.error('Ошибка удаления:', error)
      alert('Ошибка удаления плана')
    }
  }
  
  const loadPlans = async () => {
    try {
      const response = await axios.get('/api/v1/plans/')
      plans.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки планов:', error)
      alert('Ошибка загрузки планов')
    }
  }
  
  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr + 'T00:00:00')
    return date.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }
  
  onMounted(() => {
    loadPlans()
  })
  </script>
  
  <style scoped>
  .plans-page {
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
  
  .plan-item {
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    background: white;
  }
  
  .plan-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .plan-actions {
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