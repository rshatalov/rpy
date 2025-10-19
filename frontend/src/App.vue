<template>
  <div id="app">
    <Navigation />
    <router-view />
  </div>
</template>


<script setup>
import Navigation from './components/Navigation.vue'


</script>


<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
