<template>
    <hr/>
    <div>
      <h3>Управление тэгами</h3>
      
      <!-- Форма создания тэга -->
      <div>
        <h4>Создать тэг</h4>
        <form @submit.prevent="createTag">
          <div>
            <label>Slug:</label>
            <input v-model="form.slug" type="text" required placeholder="python" />
          </div>
          <div>
            <label>Название:</label>
            <input v-model="form.title" type="text" required placeholder="Python Programming" />
          </div>
          <button type="submit" :disabled="loading">
            {{ loading ? 'Создание...' : 'Создать тэг' }}
          </button>
        </form>
      </div>
  
      <!-- Список тэгов -->
      <div>
        <h4>Список тэгов</h4>
        <button @click="loadTags" :disabled="loadingTags">
          {{ loadingTags ? 'Загрузка...' : 'Обновить список' }}
        </button>
        
        <div v-if="tags.length > 0">
          <div v-for="tag in tags" :key="tag.slug" class="tag-item">
            <strong>{{ tag.slug }}</strong>: {{ tag.title }}
            <button @click="deleteTag(tag.slug)" class="delete-btn">Удалить</button>
          </div>
        </div>
        <div v-else-if="!loadingTags">
          Тэгов пока нет
        </div>
      </div>
  
      <!-- Сообщения -->
      <div v-if="message" class="message">{{ message }}</div>
    </div>
    <hr/>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const form = ref({ slug: '', title: '' })
  const tags = ref([])
  const loading = ref(false)
  const loadingTags = ref(false)
  const message = ref('')
  
  // Создание тэга
  const createTag = async () => {
    loading.value = true
    try {
      const response = await axios.post('http://localhost:8000/api/v1/tags/', form.value)
      message.value = `Тэг "${response.data.slug}" создан успешно!`
      form.value = { slug: '', title: '' }
      loadTags() // Обновляем список
    } catch (error) {
      if (error.response?.data?.detail) {
        message.value = `Ошибка: ${error.response.data.detail}`
      } else {
        message.value = 'Ошибка создания тэга'
      }
    }
    loading.value = false
  }
  
  // Загрузка списка тэгов
  const loadTags = async () => {
    loadingTags.value = true
    try {
      const response = await axios.get('http://localhost:8000/api/v1/tags')
      tags.value = response.data
    } catch (error) {
      message.value = 'Ошибка загрузки тэгов'
    }
    loadingTags.value = false
  }
  
  // Удаление тэга
  const deleteTag = async (slug) => {
    if (!confirm(`Удалить тэг "${slug}"?`)) return
    
    try {
      await axios.delete(`http://localhost:8000/api/v1/tags/${slug}`)
      message.value = `Тэг "${slug}" удален`
      loadTags() // Обновляем список
    } catch (error) {
      message.value = 'Ошибка удаления тэга'
    }
  }
  
  // Загружаем тэги при монтировании компонента
  onMounted(() => {
    loadTags()
  })
  </script>
  
  <style scoped>
  .tag-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    margin: 4px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .delete-btn {
    background-color: #ff4444;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .delete-btn:hover {
    background-color: #cc0000;
  }
  
  .message {
    margin-top: 10px;
    padding: 8px;
    background-color: #f0f0f0;
    border-radius: 4px;
  }
  
  form div {
    margin: 8px 0;
  }
  
  form label {
    display: inline-block;
    width: 80px;
  }
  
  form input {
    padding: 4px;
    margin-left: 8px;
  }
  
  button {
    padding: 6px 12px;
    margin: 4px;
    cursor: pointer;
  }
  </style>