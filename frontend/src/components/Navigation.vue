<template>
    <nav class="navigation">
      <ul>
        <li><router-link to="/" class="nav-link">Главная</router-link></li>
        <li><router-link to="/acts" class="nav-link">Активности</router-link></li>
        <li><router-link to="/plans" class="nav-link">Планы</router-link></li>
    <li><router-link to="/tasks" class="nav-link">Задачи</router-link></li>
    <li><router-link to="/plan-notes" class="nav-link">Заметки планов</router-link></li>
    <li><router-link to="/act-notes" class="nav-link">Заметки активностей</router-link></li>
        <li><router-link to="/tags" class="nav-link">Тэги</router-link></li>
        <li><router-link to="/questions" class="nav-link">Вопросы</router-link></li>
        <li><router-link to="/study" class="nav-link">Учебная сессия</router-link></li>
      </ul>
    </nav>
  </template>
  
  <script setup>
  // Компонент навигации
  </script>
  
  <style scoped>
  .navigation {
    background-color: #f8f9fa;
    padding: 1rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #dee2e6;
  }
  
  .navigation ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 2rem;
  }
  
  .navigation li {
    margin: 0;
  }
  
  .nav-link {
    text-decoration: none;
    color: #495057;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    transition: all 0.2s;
  }
  
  .nav-link:hover {
    background-color: #e9ecef;
    color: #212529;
  }
  
  .nav-link.router-link-active {
    background-color: #007bff;
    color: white;
  }
  </style>