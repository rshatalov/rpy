<template>
    <div class="plan-form">
      <h3>Редактировать план</h3>
      <form @submit.prevent="handleSubmit">
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
            <option v-for="plan in availablePlans.filter(p => p.id !== props.plan.id)" :key="plan.id" :value="plan.id">
              {{ plan.title }}
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
    plan: {
      type: Object,
      required: true
    },
    availablePlans: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['saved', 'cancelled'])
  
  const form = ref({
    title: '',
    start_date: null,
    end_date: null,
    parent_id: null
  })
  
  const initForm = () => {
    if (props.plan) {
      form.value = {
        title: props.plan.title || '',
        start_date: props.plan.start_date || null,
        end_date: props.plan.end_date || null,
        parent_id: props.plan.parent_id || null
      }
    }
  }
  
  const handleSubmit = async () => {
    try {
      const payload = {
        title: form.value.title,
        start_date: form.value.start_date || null,
        end_date: form.value.end_date || null,
        parent_id: form.value.parent_id
      }
      await axios.put(`/api/v1/plans/${props.plan.id}`, payload)
      emit('saved')
    } catch (error) {
      console.error('Ошибка обновления плана:', error)
      alert('Ошибка обновления плана')
    }
  }
  
  const cancel = () => {
    emit('cancelled')
  }
  
  watch(() => props.plan, () => {
    initForm()
  }, { immediate: true })
  
  onMounted(() => {
    initForm()
  })
  </script>
  
  <style scoped>
  .plan-form {
    background: #fff3cd;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 2px solid #ffc107;
  }
  
  .plan-form div {
    margin-bottom: 15px;
  }
  
  .plan-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .plan-form input,
  .plan-form select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
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