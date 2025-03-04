<template>
  <nav class="navbar glass-effect">
    <div class="container navbar-container">
      <router-link to="/" class="navbar-logo">
        <div class="logo-icon">
          <div class="logo-circle"></div>
          <div class="logo-pulse"></div>
        </div>
        <span class="logo-text neon-text">AI行业信息助手</span>
      </router-link>
      
      <div class="navbar-links" :class="{ 'active': isMenuOpen }">
        <router-link to="/" class="navbar-link" @click="closeMenu">首页</router-link>
        <a :href="rssUrl" target="_blank" class="navbar-link rss-link" @click="closeMenu">
          <span>RSS订阅</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 11a9 9 0 0 1 9 9"></path>
            <path d="M4 4a16 16 0 0 1 16 16"></path>
            <circle cx="5" cy="19" r="1"></circle>
          </svg>
        </a>
        <div class="theme-toggle-container">
          <ThemeToggle />
        </div>
      </div>
      
      <div class="navbar-actions">
        <ThemeToggle class="desktop-theme-toggle" />
        <button class="menu-toggle" @click="toggleMenu" :class="{ 'active': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import ThemeToggle from '@/components/ThemeToggle.vue'

export default {
  name: 'Navbar',
  components: {
    ThemeToggle
  },
  data() {
    return {
      isMenuOpen: false,
      rssUrl: '/rss'
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
      document.body.style.overflow = this.isMenuOpen ? 'hidden' : ''
    },
    closeMenu() {
      this.isMenuOpen = false
      document.body.style.overflow = ''
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px var(--shadow-color);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.light-theme .navbar {
  background-color: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-color);
  font-weight: 700;
  font-size: 1.5rem;
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

.navbar-logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  position: relative;
  width: 24px;
  height: 24px;
}

.logo-circle {
  position: absolute;
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px var(--primary-color);
  animation: pulse 2s infinite alternate;
}

.logo-pulse {
  position: absolute;
  width: 24px;
  height: 24px;
  border: 2px solid var(--primary-color);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  animation: ripple 2s infinite;
}

@keyframes ripple {
  0% {
    width: 0px;
    height: 0px;
    opacity: 0.8;
  }
  100% {
    width: 24px;
    height: 24px;
    opacity: 0;
  }
}

.logo-text {
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 800;
  position: relative;
  letter-spacing: 0.5px;
}

.logo-text::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.navbar-logo:hover .logo-text::after {
  transform: scaleX(1);
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.navbar-link {
  color: var(--text-color);
  font-weight: 500;
  position: relative;
  padding: 0.5rem 0;
  transition: color var(--transition-speed) ease;
  letter-spacing: 0.5px;
}

.navbar-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  transition: width var(--transition-speed) ease;
}

.navbar-link:hover {
  color: var(--primary-color);
}

.navbar-link:hover::after {
  width: 100%;
}

.router-link-active {
  color: var(--primary-color);
}

.router-link-active::after {
  width: 100%;
}

.rss-link {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.rss-link svg {
  transition: transform var(--transition-speed) ease;
}

.rss-link:hover svg {
  transform: translateX(3px);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.desktop-theme-toggle {
  display: block;
}

.theme-toggle-container {
  display: none;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
  box-shadow: none;
}

.menu-toggle:hover {
  transform: none;
  box-shadow: none;
}

.menu-toggle span {
  display: block;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  border-radius: 3px;
  transition: all 0.3s ease;
}

.menu-toggle.active span:nth-child(1) {
  transform: translateY(9px) rotate(45deg);
}

.menu-toggle.active span:nth-child(2) {
  opacity: 0;
}

.menu-toggle.active span:nth-child(3) {
  transform: translateY(-9px) rotate(-45deg);
}

@media (max-width: 768px) {
  .menu-toggle {
    display: flex;
  }
  
  .navbar-links {
    position: fixed;
    top: 0;
    right: -100%;
    width: 70%;
    height: 100vh;
    background-color: var(--card-bg-color);
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: right 0.3s ease;
    box-shadow: -5px 0 15px var(--shadow-color);
    z-index: 99;
  }
  
  .navbar-links.active {
    right: 0;
  }
  
  .desktop-theme-toggle {
    display: none;
  }
  
  .theme-toggle-container {
    display: block;
    margin-top: 1rem;
  }
}
</style>
