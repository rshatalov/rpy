<template>
    <div class="code-display">
      <div class="code-header">
        <span class="language">{{ language }}</span>
        <button @click="copyCode" class="copy-btn">Копировать</button>
      </div>
      <pre><code :class="`language-${language}`" v-html="highlightedCode"></code></pre>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import hljs from 'highlight.js'
  import 'highlight.js/styles/github.css'
  
  const props = defineProps({
    code: String,
    language: {
      type: String,
      default: 'javascript'
    }
  })
  
  const highlightedCode = computed(() => {
    return hljs.highlight(props.code, { language: props.language }).value
  })
  
  const copyCode = async () => {
    await navigator.clipboard.writeText(props.code)
    // Показать уведомление о копировании
  }
  </script>
  
  <style scoped>
  .code-display {
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    overflow: hidden;
    margin: 16px 0;
  }
  
  .code-header {
    background: #f6f8fa;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e1e4e8;
  }
  
  .language {
    font-size: 12px;
    color: #586069;
    text-transform: uppercase;
  }
  
  .copy-btn {
    background: #0366d6;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
  }
  
  pre {
    margin: 0;
    padding: 16px;
    overflow-x: auto;
    background: #f6f8fa;
  }
  </style>