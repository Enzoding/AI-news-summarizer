<template>
  <div class="report-detail-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <LoadingSpinner message="正在加载报告内容..." />
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <div class="error-actions">
        <button @click="fetchReport" class="btn">重试</button>
        <router-link to="/" class="btn">返回首页</router-link>
      </div>
    </div>
    
    <!-- 报告内容 -->
    <div v-else-if="report" class="report-content-container">
      <!-- 返回链接 -->
      <div class="back-link-container">
        <router-link to="/" class="back-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          返回
        </router-link>
      </div>
      
      <!-- 主要内容 -->
      <div class="main-content">
        <!-- 标题 -->
        <div class="report-header">
          <h1 class="report-title">AI行业日报 {{ formatDate(report.date) }}</h1>
        </div>
        
        <!-- 概述部分 -->
        <div id="summary" class="content-section">
          <h2 class="section-title">行业概述</h2>
          <div class="markdown-content" v-html="renderMarkdown(report.summary)"></div>
        </div>
        
        <!-- 新闻部分 -->
        <div v-if="report.news && report.news.length > 0" id="news" class="content-section">
          <h2 class="section-title">重要新闻</h2>
          <div 
            v-for="(item, index) in report.news" 
            :key="index" 
            :id="`news-${index}`"
            class="content-item"
          >
            <h3 class="item-title">{{ item.title }}</h3>
            <div class="markdown-content" v-html="renderMarkdown(item.summary)"></div>
            <div class="item-meta">
              <span class="item-source">{{ item.source }}</span>
              <a v-if="item.url" :href="item.url" target="_blank" class="item-link">
                原文链接
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </div>
        
        <!-- 论文部分 -->
        <div v-if="report.papers && report.papers.length > 0" id="papers" class="content-section">
          <h2 class="section-title">研究论文</h2>
          <div 
            v-for="(paper, index) in report.papers" 
            :key="index" 
            :id="`paper-${index}`"
            class="content-item"
          >
            <h3 class="item-title">{{ paper.title }}</h3>
            <p class="item-authors">{{ formatAuthors(paper.authors) }}</p>
            <div class="markdown-content" v-html="renderMarkdown(paper.summary)"></div>
            <div class="item-meta">
              <span class="item-date">{{ formatDate(paper.published_date) }}</span>
              <a v-if="paper.url" :href="paper.url" target="_blank" class="item-link">
                论文链接
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
    
    <!-- 空状态 -->
    <div v-else class="empty-container">
      <p>未找到报告数据</p>
      <router-link to="/" class="btn">返回首页</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { marked } from 'marked'

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
    formatAuthors(authors) {
      if (!authors) return ''
      if (typeof authors === 'string') return authors
      return authors.join(', ')
    },
    renderMarkdown(content) {
      if (!content) return ''
      return marked(content)
    }
  }
}
</script>

<style scoped>
/* 基础布局 */
.report-detail-container {
  min-height: 100vh;
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

/* 加载和错误状态 */
.loading-container,
.error-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 2rem;
  text-align: center;
}

.error-message {
  color: #e53e3e;
  margin-bottom: 1rem;
}

.error-actions {
  display: flex;
  gap: 1rem;
}

/* 按钮样式 */
.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #4299e1;
  color: white;
  border-radius: 0.25rem;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn:hover {
  background-color: #3182ce;
}

/* 返回链接 */
.back-link-container {
  margin-bottom: 1rem;
  padding: 0.5rem 0;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
  text-decoration: none;
  transition: color 0.2s;
}

.back-link:hover {
  color: #4299e1;
}

/* 主要内容布局 */
.report-content-container {
  display: flex;
  flex-direction: column;
}

/* 主内容区 */
.main-content {
  padding: 1rem 0;
}

.report-header {
  margin-bottom: 2rem;
}

.report-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
}

/* 内容部分 */
.content-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #4299e1;
}

.content-item {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.content-item:last-child {
  border-bottom: none;
}

.item-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 0.75rem;
}

.item-authors {
  font-size: 0.875rem;
  color: #718096;
  font-style: italic;
  margin: 0 0 0.75rem;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #718096;
}

.item-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: #4299e1;
  text-decoration: none;
  transition: color 0.2s;
}

.item-link:hover {
  color: #3182ce;
}

/* Markdown 内容样式 */
.markdown-content {
  line-height: 1.7;
  color: #4a5568;
}

.markdown-content :deep(h2) {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin: 1.5rem 0 0.75rem;
}

.markdown-content :deep(h3) {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin: 1.25rem 0 0.75rem;
}

.markdown-content :deep(h4) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 1rem 0 0.75rem;
}

.markdown-content :deep(p) {
  margin: 0 0 1rem;
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: #2d3748;
}

.markdown-content :deep(em) {
  font-style: italic;
  color: #4a5568;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .report-title {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
}
</style>
