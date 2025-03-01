<template>
  <div class="about-page animate__animated animate__fadeIn">
    <h1 class="page-title">关于 AI行业信息助手</h1>
    
    <div class="about-content">
      <div class="about-section card">
        <h2 class="section-subtitle">项目介绍</h2>
        <p class="about-text">
          AI行业信息助手是一个基于人工智能的行业资讯聚合平台，旨在帮助AI从业者和爱好者快速获取行业最新动态。
          我们每天自动收集来自各大科技媒体和学术平台的AI相关新闻和研究论文，通过大语言模型进行智能总结和分析，
          为用户提供高质量、易于理解的AI行业信息摘要。
        </p>
      </div>
      
      <div class="about-section card">
        <h2 class="section-subtitle">核心功能</h2>
        <ul class="features-list">
          <li class="feature-item">
            <div class="feature-icon">🔍</div>
            <div class="feature-content">
              <h3 class="feature-title">智能聚合</h3>
              <p class="feature-description">自动收集AI行业相关新闻和研究论文，覆盖主流科技媒体和学术平台</p>
            </div>
          </li>
          <li class="feature-item">
            <div class="feature-icon">🤖</div>
            <div class="feature-content">
              <h3 class="feature-title">AI总结</h3>
              <p class="feature-description">使用大语言模型生成高质量中文摘要，提取关键信息</p>
            </div>
          </li>
          <li class="feature-item">
            <div class="feature-icon">📱</div>
            <div class="feature-content">
              <h3 class="feature-title">便捷阅读</h3>
              <p class="feature-description">简洁现代的界面设计，支持多端访问，提供良好的阅读体验</p>
            </div>
          </li>
          <li class="feature-item">
            <div class="feature-icon">🔄</div>
            <div class="feature-content">
              <h3 class="feature-title">定期更新</h3>
              <p class="feature-description">每日自动更新，确保您获取最新的行业动态</p>
            </div>
          </li>
          <li class="feature-item">
            <div class="feature-icon">📡</div>
            <div class="feature-content">
              <h3 class="feature-title">RSS订阅</h3>
              <p class="feature-description">支持RSS订阅，方便用户通过阅读器获取更新</p>
            </div>
          </li>
        </ul>
      </div>
      
      <div class="about-section card">
        <h2 class="section-subtitle">技术实现</h2>
        <p class="about-text">
          本项目前端基于Vue.js构建，采用轻量级设计，确保快速加载和流畅体验。后端使用Python Flask框架，
          结合先进的自然语言处理技术，实现内容的自动收集、处理和生成。整个系统采用模块化设计，具有良好的可扩展性。
        </p>
      </div>
      
      <div class="about-section card">
        <h2 class="section-subtitle">联系我们</h2>
        <p class="about-text">
          如果您有任何问题、建议或合作意向，欢迎通过以下方式与我们联系：
        </p>
        <div class="contact-info">
          <div class="contact-item">
            <span class="contact-icon">📧</span>
            <span class="contact-text">邮箱：contact@aiassistant.example.com</span>
          </div>
          <div class="contact-item">
            <span class="contact-icon">🌐</span>
            <span class="contact-text">网站：www.aiassistant.example.com</span>
          </div>
          <div class="contact-item">
            <span class="contact-icon">📱</span>
            <span class="contact-text">社交媒体：@AIIndustryAssistant</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="subscription-section">
      <h2 class="subscription-title">订阅我们的更新</h2>
      <p class="subscription-text">通过RSS订阅，随时获取AI行业最新动态</p>
      <a :href="rssUrl" target="_blank" class="subscription-button tech-glow">
        <span>RSS订阅</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 11a9 9 0 0 1 9 9"></path>
          <path d="M4 4a16 16 0 0 1 16 16"></path>
          <circle cx="5" cy="19" r="1"></circle>
        </svg>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      rssUrl: '/rss'
    }
  }
}
</script>

<style scoped>
.about-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.about-section {
  padding: 2rem;
}

.section-subtitle {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
  position: relative;
  display: inline-block;
}

.section-subtitle::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -5px;
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 3px;
}

.about-text {
  line-height: 1.8;
  font-size: 1.1rem;
}

.features-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.feature-icon {
  font-size: 2rem;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.feature-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

.contact-info {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.contact-icon {
  font-size: 1.5rem;
}

.contact-text {
  color: var(--text-secondary);
}

.subscription-section {
  margin-top: 3rem;
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(155, 89, 182, 0.1));
  border-radius: 12px;
}

.subscription-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.subscription-text {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.subscription-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 2rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  color: white;
  border-radius: 30px;
  font-weight: 600;
  transition: all var(--transition-speed) ease;
}

.subscription-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.subscription-button svg {
  transition: transform var(--transition-speed) ease;
}

.subscription-button:hover svg {
  transform: translateX(3px);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .about-section {
    padding: 1.5rem;
  }
  
  .section-subtitle {
    font-size: 1.3rem;
  }
  
  .about-text {
    font-size: 1rem;
  }
  
  .subscription-section {
    padding: 2rem 1rem;
  }
  
  .subscription-title {
    font-size: 1.5rem;
  }
}
</style>
