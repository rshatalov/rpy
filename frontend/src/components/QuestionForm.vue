<template>
    <div class="question-form">
      <h3 v-if="isEditing">Редактировать вопрос</h3>
      <h3 v-else>Создать новый вопрос</h3>
      
      <form @submit.prevent="handleSubmit">
        <div>
          <label>Вопрос:</label>
          <textarea 
            v-model="form.q" 
            required 
          ></textarea>
        </div>
        
        <div>
          <label>Ответ:</label>
          <textarea 
            v-model="form.a" 
            required 
          ></textarea>
        </div>
        
        <div>
          <label>Сложность:</label>
          <select v-model="form.difficulty">
            <option value="">Выберите сложность</option>
            <option value="easy">Легкая</option>
            <option value="medium">Средняя</option>
            <option value="hard">Сложная</option>
          </select>
        </div>
        
        <div>
          <label>Теги:</label>
          <div class="tags-selection">
            <div v-for="tag in availableTags" :key="tag.slug" class="tag-option">
              <input 
                type="checkbox" 
                :id="`${tag.slug}-${formId}`"
                :value="tag.slug"
                v-model="form.tag_slugs"
              >
              <label :for="`${tag.slug}-${formId}`">{{ tag.title }}</label>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="loading">
            {{ loading ? 'Сохранение...' : (isEditing ? 'Сохранить изменения' : 'Создать вопрос') }}
          </button>
          <button 
            v-if="isEditing" 
            type="button" 
            @click="cancelEdit"
            class="cancel-btn"
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import axios from 'axios'
  
  const props = defineProps({
    question: {
      type: Object,
      default: null
    },
    availableTags: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['saved', 'cancelled'])
  
  const formId = ref(Math.random().toString(36).substr(2, 9))
  const loading = ref(false)
  
  const isEditing = ref(false)
  
  const form = ref({
    q: '',
    a: '',
    difficulty: '',
    tag_slugs: []
  })
  
  // Инициализация формы
  const initForm = () => {
    if (props.question) {
      isEditing.value = true
      form.value = {
        q: props.question.q || '',
        a: props.question.a || '',
        difficulty: props.question.difficulty || '',
        tag_slugs: props.question.tags ? props.question.tags.map(tag => tag.slug) : []
      }
    } else {
      isEditing.value = false
      form.value = {
        q: '',
        a: '',
        difficulty: '',
        tag_slugs: []
      }
    }
  }
  
  const handleSubmit = async () => {
    loading.value = true
    
    try {
      if (isEditing.value) {
        // Обновляем существующий вопрос
        await axios.put(`http://localhost:8000/api/v1/questions/${props.question.id}`, form.value)
        console.log('Вопрос обновлен')
      } else {
        // Создаем новый вопрос
        await axios.post('http://localhost:8000/api/v1/questions/', form.value)
        console.log('Вопрос создан')
      }
      
      emit('saved')
      initForm() // Сброс формы
    } catch (error) {
      console.error('Ошибка сохранения вопроса:', error)
      alert('Ошибка при сохранении вопроса')
    } finally {
      loading.value = false
    }
  }
  
  const cancelEdit = () => {
    emit('cancelled')
    initForm()
  }
  
  // Следим за изменениями question
  watch(() => props.question, () => {
    initForm()
  }, { immediate: true })
  
  onMounted(() => {
    initForm()
  })
  </script>
  
  <style scoped>
  .question-form {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .question-form h3 {
    margin-top: 0;
    margin-bottom: 20px;
    color: #24292e;
  }
  
  .question-form div {
    margin-bottom: 15px;
  }
  
  .question-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .question-form textarea,
  .question-form select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .question-form textarea {
    height: 100px;
    resize: vertical;
    font-family: 'SFMono-Regular', Consolas, monospace;
  }
  
  .tags-selection {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .tag-option {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .form-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
  
  .form-actions button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
  }
  
  .form-actions button[type="submit"] {
    background: #007bff;
    color: white;
  }
  
  .form-actions button[type="submit"]:hover:not(:disabled) {
    background: #0056b3;
  }
  
  .form-actions button[type="submit"]:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }
  
  .cancel-btn {
    background: #6c757d;
    color: white;
  }
  
  .cancel-btn:hover {
    background: #545b62;
  }
  </style>