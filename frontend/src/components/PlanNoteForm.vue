<template>
    <div class="plan-note-form">
      <h3>Редактировать заметку</h3>
      <form @submit.prevent="handleSubmit">
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
          <label>Время создания:</label>
          <input v-model="form.created_at" type="datetime-local" />  <!-- ✅ Добавьте это поле -->
        </div>
        <div>
          <label>Содержимое:</label>
          <textarea v-model="form.content" required></textarea>
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
    note: {
      type: Object,
      required: true
    },
    plans: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['saved', 'cancelled'])
  
  const form = ref({
    content: '',
    plan_id: null,
    created_at: null
  })
  
  const initForm = () => {
    if (props.note) {
      form.value = {
        content: props.note.content || '',
        plan_id: props.note.plan_id || null,
        created_at: formatDate(props.note.created_at) 
      }
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

  const handleSubmit = async () => {
    try {
      await axios.put(`/api/v1/plan-notes/${props.note.id}`, form.value)
      emit('saved')
    } catch (error) {
      console.error('Ошибка обновления заметки:', error)
      alert('Ошибка обновления заметки')
    }
  }
  
  const cancel = () => {
    emit('cancelled')
  }
  
  watch(() => props.note, () => {
    initForm()
  }, { immediate: true })
  
  onMounted(() => {
    initForm()
  })
  </script>
  
  <style scoped>
  .plan-note-form {
    background: #fff3cd;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 2px solid #ffc107;
  }
  
  .plan-note-form div {
    margin-bottom: 15px;
  }
  
  .plan-note-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .plan-note-form select,
  .plan-note-form textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .plan-note-form textarea {
    height: 150px;
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