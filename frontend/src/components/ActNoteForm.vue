<template>
    <div class="act-note-form">
      <h3>Редактировать заметку</h3>
      <form @submit.prevent="handleSubmit">
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
    acts: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['saved', 'cancelled'])
  
  const form = ref({
    content: '',
    act_id: null,
    created_at: null
  })
  
  const initForm = () => {
    if (props.note) {
      form.value = {
        content: props.note.content || '',
        act_id: props.note.act_id || null,
        created_at: formatDateTime(props.note.created_at)
      }
    }
  }

  const formatDateTime = (dateStr) => {
    if (!dateStr) return ''
    // console.log(dateStr)
    // const d = new Date(dateStr).toLocaleDateString('ru-RU', {
    //     day: '2-digit',
    //     month: '2-digit',
    //     year: 'numeric'
    //   })
    // console.log(d)
    const date = new Date(dateStr)

    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const d = `${year}-${month}-${day}T${hours}:${minutes}`
    return d
  }
  
  const handleSubmit = async () => {
    try {
      await axios.put(`/api/v1/act-notes/${props.note.id}`, form.value)
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
  .act-note-form {
    background: #fff3cd;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border: 2px solid #ffc107;
  }
  
  .act-note-form div {
    margin-bottom: 15px;
  }
  
  .act-note-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .act-note-form select,
  .act-note-form textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .act-note-form textarea {
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