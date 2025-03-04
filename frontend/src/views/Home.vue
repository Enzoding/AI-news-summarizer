<template>
  <div class="home">
    <div class="hero-section animate__animated animate__fadeIn glass-effect">
      <div class="hero-content">
        <h1 class="hero-title">AI<span class="accent-text">行业信息</span>助手</h1>
        <p class="hero-subtitle">每日自动收集和总结AI行业最新资讯</p>
        <div class="hero-decoration">
          <div class="tech-line"></div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="tech-circle-container">
          <div class="tech-circle-outer"></div>
          <div class="tech-circle-middle"></div>
          <div class="tech-circle-inner"></div>
          <div class="tech-circle-dot"></div>
        </div>
      </div>
    </div>
    
    <div class="reports-section">
      
      <div v-if="loading" class="loading-container">
        <LoadingSpinner message="正在加载日报..." />
      </div>
      
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="fetchReports" class="retry-button">重试</button>
      </div>
      
      <div v-else-if="reports.length === 0" class="empty-state">
        <p>暂无日报数据</p>
      </div>
      
      <div v-else class="reports-grid">
        <div v-for="(report, index) in reports" :key="report.date" class="report-item animate__animated animate__fadeInUp" :style="{ animationDelay: `${index * 0.1}s` }">
          <ReportCard :report="report" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ReportCard from '@/components/ReportCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  name: 'HomeView',
  components: {
    ReportCard,
    LoadingSpinner
  },
  data() {
    return {
      reports: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchReports()
  },
  methods: {
    async fetchReports() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/reports', {
          params: { limit: 20 }
        })
        
        if (response.data.success) {
          this.reports = response.data.data
        } else {
          this.error = '获取日报数据失败'
        }
      } catch (err) {
        console.error('获取日报失败:', err)
        this.error = '网络错误，请稍后重试'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.home {
  padding-bottom: 2rem;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4rem 2rem;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, rgba(17, 24, 39, 0.8), rgba(10, 14, 23, 0.9));
  border-radius: 16px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.light-theme .hero-section {
  background: linear-gradient(135deg, rgba(240, 242, 245, 0.8), rgba(255, 255, 255, 0.9));
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(0, 163, 255, 0.15), transparent 70%);
  opacity: 0.7;
}

.light-theme .hero-section::before {
  background: radial-gradient(circle at center, rgba(0, 149, 255, 0.15), transparent 70%);
}

.hero-content {
  flex: 1;
  z-index: 2;
}

.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 2;
  height: 200px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  position: relative;
  z-index: 2;
  text-shadow: 0 0 30px rgba(0, 163, 255, 0.5);
  letter-spacing: 1px;
}

.accent-text {
  color: var(--accent-color);
  background: linear-gradient(90deg, var(--secondary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.light-theme .hero-title {
  text-shadow: 0 0 30px rgba(0, 149, 255, 0.5);
}

.hero-subtitle {
  font-size: 1.3rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 2rem 0;
  position: relative;
  z-index: 2;
  letter-spacing: 0.5px;
}

.hero-decoration {
  position: relative;
  height: 40px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  z-index: 2;
  width: 70%;
}

.tech-circle-container {
  position: relative;
  width: 200px;
  height: 200px;
}

.tech-circle-outer {
  position: absolute;
  width: 200px;
  height: 200px;
  border: 1px solid rgba(0, 163, 255, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: rotate 20s linear infinite;
}

.tech-circle-middle {
  position: absolute;
  width: 150px;
  height: 150px;
  border: 1px solid rgba(0, 240, 144, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: rotate 15s linear infinite reverse;
}

.tech-circle-inner {
  position: absolute;
  width: 100px;
  height: 100px;
  border: 1px solid rgba(140, 93, 255, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: rotate 10s linear infinite;
}

.tech-circle-dot {
  position: absolute;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 15px var(--primary-color);
  animation: pulse 2s infinite alternate;
}

@keyframes rotate {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.8;
    box-shadow: 0 0 25px var(--primary-color);
  }
}

.reports-section {
  padding: 2rem 0;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.report-item {
  height: 100%;
}

.loading-container, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  text-align: center;
}

.error-message {
  text-align: center;
  color: #ff5252;
  padding: 2rem;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background-color: var(--accent-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    padding: 3rem 1.5rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
    text-align: center;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
    text-align: center;
    margin: 0 auto 2rem;
  }
  
  .hero-decoration {
    justify-content: center;
    width: 100%;
  }
  
  .hero-visual {
    margin-top: 2rem;
  }
  
  .tech-circle-container {
    transform: scale(0.8);
  }
}
</style>
