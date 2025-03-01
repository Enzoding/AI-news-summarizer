<template>
  <footer class="footer">
    <div class="container footer-container">
      <div class="footer-content">
        <div class="footer-logo">
          <span class="logo-text">AI行业信息助手</span>
          <p class="footer-description">每日自动收集和总结AI行业最新资讯</p>
        </div>
        <div class="footer-links">
          <router-link to="/" class="footer-link">首页</router-link>
          <router-link to="/about" class="footer-link">关于</router-link>
          <a :href="rssUrl" target="_blank" class="footer-link">RSS订阅</a>
        </div>
      </div>
      <div class="footer-copyright">
        <p>&copy; {{ currentYear }} AI行业信息助手. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      rssUrl: '/rss',
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.footer {
  background-color: #f1f5f9;
  padding: 2rem 0 1rem;
  margin-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.footer-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 2rem;
}

.footer-logo {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.footer-description {
  color: var(--text-secondary);
  max-width: 300px;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-link {
  color: var(--text-secondary);
  transition: color var(--transition-speed) ease;
}

.footer-link:hover {
  color: var(--primary-color);
}

.footer-copyright {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .footer-links {
    margin-top: 1rem;
  }
}
</style>
