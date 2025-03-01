<template>
  <div class="report-detail">
    <div v-if="loading" class="loading-container">
      <LoadingSpinner message="正在加载报告内容..." />
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="fetchReport" class="retry-button">重试</button>
      <router-link to="/" class="back-button">返回首页</router-link>
    </div>
    
    <div v-else-if="report" class="report-content animate__animated animate__fadeIn">
      <div class="report-header">
        <router-link to="/" class="back-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          返回
        </router-link>
        <h1 class="report-title">AI行业日报 {{ formatDate(report.date) }}</h1>
        <p class="report-date">发布于 {{ formatDateTime(report.generated_at) }}</p>
      </div>
      
      <div class="summary-section card">
        <h2 class="section-subtitle">今日概述</h2>
        <p class="summary-text">{{ report.summary }}</p>
      </div>
      
      <div v-if="report.news && report.news.length > 0" class="news-section card">
        <h2 class="section-subtitle">行业新闻</h2>
        <div class="news-list">
          <div v-for="(item, index) in report.news" :key="index" class="news-item animate__animated animate__fadeInUp" :style="{ animationDelay: `${index * 0.05}s` }">
            <h3 class="news-title">{{ item.title }}</h3>
            <p class="news-summary">{{ item.summary }}</p>
            <div class="news-meta">
              <span class="news-source">{{ item.source }}</span>
              <a v-if="item.url" :href="item.url" target="_blank" class="news-link">
                原文链接
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="report.papers && report.papers.length > 0" class="papers-section card">
        <h2 class="section-subtitle">研究论文</h2>
        <div class="papers-list">
          <div v-for="(paper, index) in report.papers" :key="index" class="paper-item animate__animated animate__fadeInUp" :style="{ animationDelay: `${index * 0.05}s` }">
            <h3 class="paper-title">{{ paper.title }}</h3>
            <p class="paper-authors">{{ formatAuthors(paper.authors) }}</p>
            <p class="paper-summary">{{ paper.summary }}</p>
            <div class="paper-meta">
              <span class="paper-date">{{ formatDate(paper.published_date) }}</span>
              <a v-if="paper.url" :href="paper.url" target="_blank" class="paper-link">
                论文链接
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <p>未找到报告数据</p>
      <router-link to="/" class="back-button">返回首页</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  name: 'ReportDetail',
  components: {
    LoadingSpinner
  },
  data() {
    return {
      report: null,
      loading: true,
      error: null
    }
  },
  computed: {
    reportDate() {
      return this.$route.params.date
    }
  },
  watch: {
    reportDate() {
      this.fetchReport()
    }
  },
  mounted() {
    this.fetchReport()
  },
  methods: {
    async fetchReport() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`/api/reports/${this.reportDate}`)
        
        if (response.data.success) {
          this.report = response.data.data
        } else {
          this.error = '获取报告数据失败'
        }
      } catch (err) {
        console.error('获取报告失败:', err)
        this.error = '网络错误，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return ''
      const date = new Date(dateTimeString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    formatAuthors(authors) {
      if (!authors) return ''
      if (typeof authors === 'string') return authors
      return authors.join(', ')
    }
  }
}
</script>

<style scoped>
.report-detail {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

.loading-container,
.error-message,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  text-align: center;
}

.error-message {
  color: #e74c3c;
}

.retry-button,
.back-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
}

.retry-button {
  background-color: #e74c3c;
  margin-right: 1rem;
}

.back-button {
  background-color: var(--text-secondary);
}

.report-header {
  margin-bottom: 2rem;
  position: relative;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  transition: color var(--transition-speed) ease;
}

.back-link:hover {
  color: var(--primary-color);
}

.report-title {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.report-date {
  color: var(--text-secondary);
  font-size: 1rem;
}

.card {
  padding: 2rem;
  margin-bottom: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px var(--shadow-color);
  background-color: var(--card-bg-color);
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

.summary-text {
  line-height: 1.8;
  font-size: 1.1rem;
}

.news-list,
.papers-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.news-item,
.paper-item {
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

.news-item:last-child,
.paper-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.news-title,
.paper-title {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.news-summary,
.paper-summary {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.news-meta,
.paper-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.news-link,
.paper-link {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--primary-color);
  transition: all var(--transition-speed) ease;
}

.news-link:hover,
.paper-link:hover {
  color: var(--accent-color);
}

.news-link svg,
.paper-link svg {
  transition: transform var(--transition-speed) ease;
}

.news-link:hover svg,
.paper-link:hover svg {
  transform: translateX(3px);
}

.paper-authors {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  font-style: italic;
}

@media (max-width: 768px) {
  .report-title {
    font-size: 1.8rem;
  }
  
  .card {
    padding: 1.5rem;
  }
  
  .section-subtitle {
    font-size: 1.3rem;
  }
  
  .summary-text {
    font-size: 1rem;
  }
}
</style>
