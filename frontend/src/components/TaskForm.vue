<template>
    <div class="task-form">
      <h3>Редактировать задачу</h3>
      <form @submit.prevent="handleSubmit">
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
        <div class="form-actions">
          <button type="submit">Сохранить</button>
          <button type="button" @click="cancel">Отмена</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import axios from 'axios'
  
  const props = defineProps({
    task: {
      type: Object,
      required: true
    },
    plans: {
      type: Array,
      default: () => []
    },
    acts: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['saved', 'cancelled'])
  
  const form = ref({
    title: '',
    description: '',
    start_date: null,
    end_date: null,
    plan_id: null,
    act_id: null
  })
  
  const formatDateForInput = (dateStr) => {
    if (!dateStr) return null
    const date = new Date(dateStr)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day}T${hours}:${minutes}`
  }
  
  const initForm = () => {
    if (props.task) {
      form.value = {
        title: props.task.title || '',
        description: props.task.description || '',
        start_date: formatDateForInput(props.task.start_date),
        end_date: formatDateForInput(props.task.end_date),
        plan_id: props.task.plan_id || null,
        act_id: props.task.act_id || null
      }
    }
  }
  
  const handleSubmit = async () => {
    try {
      const payload = {
        title: form.value.title,
        description: form.value.description,
        start_date: form.value.start_date ? new Date(form.value.start_date).toISOString() : null,
        end_date: form.value.end_date ? new Date(form.value.end_date).toISOString() : null,
        plan_id: form.value.plan_id,
        act_id: form.value.act_id
      }
      await axios.put(`/api/v1/tasks/${props.task.id}`, payload)
      emit('saved')
    } catch (error) {
      console.error('Ошибка обновления задачи:', error)
      alert('Ошибка обновления задачи')
    }
  }
  
  const cancel = () => {
    emit('cancelled')
  }
  
  watch(() => props.task, () => {
    initForm()
  }, { immediate: true })
  
  onMounted(() => {
    initForm()
  })
  </script>
  
  <style scoped>
  .task-form {
    background: #fff3cd;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 2px solid #ffc107;
  }
  
  .task-form div {
    margin-bottom: 15px;
  }
  
  .task-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .task-form input,
  .task-form select,
  .task-form textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .task-form textarea {
    height: 80px;
    resize: vertical;
  }
  
  .form-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
  
  .form-actions button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .form-actions button[type="submit"] {
    background: #007bff;
    color: white;
  }
  
  .form-actions button[type="button"] {
    background: #6c757d;
    color: white;
  }
  </style>