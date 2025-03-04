<template>
  <div class="theme-toggle">
    <button @click="toggleTheme" class="theme-toggle-btn" :title="isDarkTheme ? '切换到浅色模式' : '切换到深色模式'">
      <svg v-if="isDarkTheme" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  name: 'ThemeToggle',
  data() {
    return {
      isDarkTheme: true
    }
  },
  mounted() {
    // 从本地存储中获取主题设置
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      this.isDarkTheme = savedTheme === 'dark'
      this.applyTheme()
    }
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme
      this.applyTheme()
      // 保存主题设置到本地存储
      localStorage.setItem('theme', this.isDarkTheme ? 'dark' : 'light')
    },
    applyTheme() {
      if (this.isDarkTheme) {
        document.body.classList.remove('light-theme')
      } else {
        document.body.classList.add('light-theme')
      }
    }
  }
}
</script>

<style scoped>
.theme-toggle {
  position: relative;
  z-index: 10;
}

.theme-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: none;
  color: var(--text-color);
  border: none;
  cursor: pointer;
  padding: 0;
  transition: opacity 0.3s ease;
}

.theme-toggle-btn:hover {
  opacity: 0.7;
}

.theme-toggle-btn svg {
  transition: opacity 0.3s ease;
}

.theme-toggle-btn:hover svg {
  opacity: 0.7;
  transform: none;
}
</style>
