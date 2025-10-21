<template>

Вопросы

<form @submit.prevent="createQuestion">
    <div>
      <label>Вопрос:</label>
      <textarea v-model="form.q" required></textarea>
    </div>
    
    <div>
      <label>Ответ:</label>
      <textarea v-model="form.a" required></textarea>
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
            :id="tag.slug"
            :value="tag.slug"
            v-model="form.tag_slugs"
          >
          <label :for="tag.slug">{{ tag.title }}</label>
        </div>
      </div>
    </div>
    
    <button type="submit">Создать вопрос</button>
  </form>



</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const form = ref({
  q: '',
  a: '',
  difficulty: '',
  tag_slugs: []
})

const availableTags = ref([])

const createQuestion = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/questions/', form.value)
    console.log('Вопрос создан:', response.data)
    // Очистить форму
    form.value = { q: '', a: '', difficulty: '', tag_slugs: [] }
  } catch (error) {
    console.error('Ошибка создания вопроса:', error)
  }
}

const loadTags = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/tags/')
    availableTags.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки тегов:', error)
  }
}

onMounted(() => {
  loadTags()
})


</script>