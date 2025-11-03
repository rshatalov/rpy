import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Timer from './Timer.vue'
import DBTest from './DBTest.vue'

import Dashboard from './pages/Dashboard.vue'
import Tags from './pages/Tags.vue'
import TestMarked from './pages/TestMarked.vue'
import TestHighlight from './pages/TestHighlight.vue'
import Questions from '@/pages/Questions.vue'
import StudySession from './pages/StudySession.vue'
import Acts from './pages/Acts.vue'
import Plans from './pages/Plans.vue'
import Tasks from './pages/Tasks.vue'
import PlanNotes from './pages/PlanNotes.vue'
import ActNotes from './pages/ActNotes.vue'

const routes = [
    { path: '/', component: Dashboard },
    { path: '/acts', component: Acts },
    { path: '/plans', component: Plans },
    { path: '/tasks', component: Tasks },
    { path: '/plan-notes', component: PlanNotes },
    { path: '/act-notes', component: ActNotes },
    { path: '/tags', component: Tags },
    { path: '/questions', component: Questions },
    { path: '/study', component: StudySession },
  ]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')