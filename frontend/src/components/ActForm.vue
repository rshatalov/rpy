<template>
    <div class="act-form">
      <h3>Редактировать активность</h3>
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
          <label>
            <input v-model="form.hidden" type="checkbox" />
            Скрыта
          </label>
        </div>
        <div>
          <label>Родительская активность:</label>
          <select v-model="form.parent_id">
            <option :value="null">Нет</option>
            <option v-for="act in availableActs" :key="act.id" :value="act.id">
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
    act: {
      type: Object,
      required: true
    },
    availableActs: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['saved', 'cancelled'])
  
  const form = ref({
    title: '',
    start_date: null,
    end_date: null,
    hidden: false,
    parent_id: null
  })
  
  const initForm = () => {
    if (props.act) {
      form.value = {
        title: props.act.title || '',
        start_date: props.act.start_date || null,
        end_date: props.act.end_date || null,
        hidden: props.act.hidden || false,
        parent_id: props.act.parent_id || null
      }
    }
  }
  
  const handleSubmit = async () => {
    try {
      const payload = {
        title: form.value.title,
        start_date: form.value.start_date || null,
        end_date: form.value.end_date || null,
        hidden: form.value.hidden,
        parent_id: form.value.parent_id
      }
      
      await axios.put(`http://localhost:8000/api/v1/acts/${props.act.id}`, payload)
      emit('saved')
    } catch (error) {
      console.error('Ошибка обновления активности:', error)
      alert('Ошибка обновления активности')
    }
  }
  
  const cancel = () => {
    emit('cancelled')
  }
  
  watch(() => props.act, () => {
    initForm()
  }, { immediate: true })
  
  onMounted(() => {
    initForm()
  })
  </script>
  
  <style scoped>
  .act-form {
    background: #fff3cd;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 2px solid #ffc107;
  }
  
  .act-form div {
    margin-bottom: 15px;
  }
  
  .act-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .act-form input,
  .act-form select {
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