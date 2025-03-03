<template>
  <div class="home">
    <div class="hero-section animate__animated animate__fadeIn">
      <h1 class="hero-title">AI行业信息助手</h1>
      <p class="hero-subtitle">每日自动收集和总结AI行业最新资讯</p>
      <div class="hero-decoration">
        <div class="tech-circle"></div>
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
  text-align: center;
  padding: 4rem 1rem;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, rgba(30, 30, 30, 0.8), rgba(18, 18, 18, 0.9));
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(79, 158, 255, 0.15), transparent 70%);
  opacity: 0.7;
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
  text-shadow: 0 0 30px rgba(79, 158, 255, 0.5);
  letter-spacing: 1px;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 2rem;
  position: relative;
  z-index: 2;
}

.hero-decoration {
  position: relative;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.tech-circle {
  width: 150px;
  height: 4px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
  position: relative;
}

.tech-circle::before, .tech-circle::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--primary-color);
  top: 50%;
  transform: translateY(-50%);
  box-shadow: 0 0 10px var(--primary-color);
}

.tech-circle::before {
  left: 0;
}

.tech-circle::after {
  right: 0;
}

.reports-section {
  margin-top: 3rem;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.report-item {
  height: 100%;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: 3rem 0;
}

.error-message {
  text-align: center;
  padding: 3rem 0;
  color: #e74c3c;
  background: rgba(231, 76, 60, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.retry-button {
  margin-top: 1.5rem;
  background-color: #e74c3c;
  padding: 0.7rem 2rem;
  font-weight: 600;
  border-radius: 30px;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background-color: #c0392b;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .reports-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
