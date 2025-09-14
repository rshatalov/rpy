<template>
<hr/>
TestItemForm Component
<div>
    <h3>Создать Test Item</h3>
    <form @submit.prevent="createItem">
      <div>
        <label>Название:</label>
        <input v-model="form.name" type="text" required />
      </div>
      <div>
        <label>Описание:</label>
        <input v-model="form.description" type="text" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Создание...' : 'Создать' }}
      </button>
    </form>
    <div v-if="message">{{ message }}</div>
</div>
<hr/>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({ name: '', description: '' })
const loading = ref(false)
const message = ref('')

const createItem = async () => {
  loading.value = true
  try {
    const response = await axios.post('http://localhost:8000/test-items/', form.value)
    message.value = `Создан ID: ${response.data.id}`
    form.value = { name: '', description: '' }
  } catch (error) {
    message.value = 'Ошибка'
  }
  loading.value = false
}


</script>