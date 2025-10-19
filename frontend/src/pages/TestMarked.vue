<template>
    <div class="markdown-content">
      <div v-html="renderedMarkdown"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { marked } from 'marked'
  
  const markdownText = ref(`
  # Заголовок
  \`\`\`javascript
  function hello() {
    console.log('Hello World!')
  }
  \`\`\`


  \`\`\`python
  def some_f(a: str = "Hey!") -> int:
    print(a)
    return 1

    r = some_f("!!!")
    print(r)
    some_f()

  \`\`\`
  
  **Жирный текст** и *курсив*
  `)
  
  const renderedMarkdown = computed(() => {
    return marked(markdownText.value)
  })
  </script>
  
  <style>
  .markdown-content {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
  }
  
  .markdown-content pre {
    background: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
  }
  
  .markdown-content code {
    background: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  }
  </style>