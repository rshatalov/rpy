<template>
    <div class="code-example-page">
      <h1>Примеры кода</h1>
      
      <!-- Markdown контент -->
      <div class="markdown-content" v-html="renderedMarkdown"></div>
      
      <!-- Отдельные блоки кода -->
      <CodeDisplay 
        :code="javascriptCode" 
        language="javascript" 
      />
      
      <CodeDisplay 
        :code="pythonCode" 
        language="python" 
      />
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { marked } from 'marked'
  import hljs from 'highlight.js'
  //import 'highlight.js/styles/github.css'
  //import 'highlight.js/styles/vs.css'
  import 'highlight.js/styles/github-dark.css'

  import CodeDisplay from '../components/CodeDisplay.vue'
  
  onMounted(async () => {
    hljs.registerLanguage('python', require('highlight.js/lib/languages/python'));

    })


  // Настройка marked
  marked.setOptions({
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    }
  })
  
  const markdownContent = ref(`
  # Добро пожаловать!
  
  Это **Markdown** с подсветкой кода:
  
  \`\`\`javascript
  const greeting = 'Hello World!'
  console.log(greeting)
  \`\`\`
  
  \`\`\`python
  def hello():
      print("Hello from Python!")
  \`\`\`
  `)
  
  const renderedMarkdown = computed(() => {
    return marked(markdownContent.value)
  })
  
  const javascriptCode = `function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
  }`
  
  const pythonCode = `def fibonacci(n):
      if n <= 1:
          return n
      return fibonacci(n - 1) + fibonacci(n - 2)`
  </script>