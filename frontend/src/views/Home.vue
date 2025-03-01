<template>
  <div class="home">
    <div class="hero-section animate__animated animate__fadeIn">
      <h1 class="hero-title">AI行业信息助手</h1>
      <p class="hero-subtitle">每日自动收集和总结AI行业最新资讯</p>
    </div>
    
    <div class="reports-section">
      <h2 class="section-title">最新日报</h2>
      
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
  padding: 3rem 1rem;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(155, 89, 182, 0.1));
  border-radius: 12px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
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
}

.retry-button {
  margin-top: 1rem;
  background-color: #e74c3c;
}

.retry-button:hover {
  background-color: #c0392b;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .reports-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
