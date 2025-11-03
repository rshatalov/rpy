<template>
  <div class="tasks-page">
    <h1>Задачи</h1>
    
    <TaskForm
      v-if="editingTask"
      :task="editingTask"
      :plans="plans"
      :acts="acts"
      @saved="handleTaskSaved"
      @cancelled="cancelEdit"
    />
    
    <div v-else class="create-form">
      <h2>Создать задачу</h2>
      <form @submit.prevent="createTask">
        <div>
          <label>Название:</label>
          <input v-model="form.title" required />
        </div>
        <div>
          <label>Описание:</label>
          <textarea v-model="form.description"></textarea>
        </div>
        <div>
          <label>Дата начала:</label>
          <input v-model="form.start_date" type="datetime-local" />
        </div>
        <div>
          <label>Дата окончания:</label>
          <input v-model="form.end_date" type="datetime-local" />
        </div>
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
          <label>Активность:</label>
          <select v-model="form.act_id">
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

    <!-- Фильтры -->
    <div class="filters">
      <select v-model="filterPlanId" @change="loadTasks">
        <option :value="null">Все планы</option>
        <option v-for="plan in plans" :key="plan.id" :value="plan.id">
          {{ plan.title }}
        </option>
      </select>
      <select v-model="filterActId" @change="loadTasks">
        <option :value="null">Все активности</option>
        <option v-for="act in acts" :key="act.id" :value="act.id">
          {{ act.title }}
        </option>
      </select>
    </div>

    <div class="tasks-list">
      <h2>Список задач</h2>
      <div v-if="tasks.length === 0" class="no-items">
        Задач пока нет
      </div>
      <div v-else>
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-header">
            <h3>{{ task.title }}</h3>
            <div class="task-actions">
              <button @click="editTask(task)" class="edit-btn">✏️</button>
              <button @click="deleteTask(task.id)" class="delete-btn">🗑️</button>
            </div>
          </div>
          <div class="task-content">
            <p v-if="task.description">{{ task.description }}</p>
            <p v-if="task.start_date">Начало: {{ formatDateTime(task.start_date) }}</p>
            <p v-if="task.end_date">Окончание: {{ formatDateTime(task.end_date) }}</p>
            <p v-if="task.plan_id">План: {{ getPlanName(task.plan_id) }}</p>
            <p v-if="task.act_id">Активность: {{ getActName(task.act_id) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import TaskForm from '@/components/TaskForm.vue'

const tasks = ref([])
const plans = ref([])
const acts = ref([])
const editingTask = ref(null)
const filterPlanId = ref(null)
const filterActId = ref(null)

const form = ref({
  title: '',
  description: '',
  start_date: null,
  end_date: null,
  plan_id: null,
  act_id: null
})

const createTask = async () => {
  try {
    const payload = {
      ...form.value,
      start_date: form.value.start_date ? new Date(form.value.start_date).toISOString() : null,
      end_date: form.value.end_date ? new Date(form.value.end_date).toISOString() : null
    }
    await axios.post('/api/v1/tasks/', payload)
    form.value = { title: '', description: '', start_date: null, end_date: null, plan_id: null, act_id: null }
    loadTasks()
  } catch (error) {
    console.error('Ошибка создания задачи:', error)
    alert('Ошибка создания задачи')
  }
}

const editTask = (task) => {
  editingTask.value = task
}

const cancelEdit = () => {
  editingTask.value = null
}

const handleTaskSaved = () => {
  editingTask.value = null
  loadTasks()
}

const deleteTask = async (id) => {
  if (!confirm('Удалить задачу?')) return
  try {
    await axios.delete(`/api/v1/tasks/${id}`)
    loadTasks()
  } catch (error) {
    console.error('Ошибка удаления:', error)
    alert('Ошибка удаления задачи')
  }
}

const loadTasks = async () => {
  try {
    let url = '/api/v1/tasks/'
    const params = []
    if (filterPlanId.value) params.push(`plan_id=${filterPlanId.value}`)
    if (filterActId.value) params.push(`act_id=${filterActId.value}`)
    if (params.length > 0) url += '?' + params.join('&')
    
    const response = await axios.get(url)
    tasks.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки задач:', error)
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

const loadActs = async () => {
  try {
    const response = await axios.get('/api/v1/acts/')
    acts.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки активностей:', error)
  }
}

const getPlanName = (id) => {
  const plan = plans.value.find(p => p.id === id)
  return plan ? plan.title : ''
}

const getActName = (id) => {
  const act = acts.value.find(a => a.id === id)
  return act ? act.title : ''
}

const formatDateTime = (dateStr) => {
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
  loadTasks()
  loadPlans()
  loadActs()
})
</script>

<style scoped>
.tasks-page {
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
.create-form select,
.create-form textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.create-form textarea {
  height: 80px;
  resize: vertical;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filters select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.task-item {
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  background: white;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.task-actions {
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