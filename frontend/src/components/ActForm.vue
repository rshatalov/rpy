<template>
    <hr/>
    ActForm Component
    <div>
        <h3>Создать Активность</h3>
        <form @submit.prevent="createAct">
          <div>
            <label>Название:</label>
            <input v-model="form.title" type="text" required />
          </div>
          <div>
            <label>Начальная дата:</label>
            <input v-model="form.start_date" type="text" />
          </div>
          <div>
            <label>Конечная дата:</label>
            <input v-model="form.end_date" type="text" />
          </div>
          <div>
            <label>Родительская активность:</label>
            <select v-model="form.parent_id">
              <option value="">Без родителя</option>
              <option v-for="act in acts" :key="act.id" :value="act.id">
                {{ act.title }} (ID: {{ act.id }})
              </option>
            </select>
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
    import { ref, onMounted } from 'vue'
    import axios from 'axios'
    
    const form = ref({ title: '', start_date: '', end_date: '', parent_id: '' })
    const loading = ref(false)
    const message = ref('')
    const acts = ref([])

    onMounted(async () => {
      try {
        const response = await axios.get('http://localhost:8000/acts/')
        acts.value = response.data
      } catch (error) {
        message.value = 'Ошибка при загрузке активностей'
        console.error('Ошибка при загрузке активностей:', error)
      }
    })

    
    const createAct = async () => {
      loading.value = true
      try {
        const response = await axios.post('http://localhost:8000/acts/', form.value)
        message.value = `Создан ID: ${response.data.id}`
        form.value = { title: '', start_date: '', end_date: '', parent_id: '' }
        const actsResponse = await axios.get('http://localhost:8000/acts/')
        acts.value = actsResponse.data
      } catch (error) {
        message.value = 'Ошибка'
      }
      loading.value = false
    }
    
    
    </script>