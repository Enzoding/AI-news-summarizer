<template>
  <div class="report-detail-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <LoadingSpinner message="正在加载报告内容..." />
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container">
      <div class="error-message">{{ error }}</div>
      <button @click="fetchReport" class="back-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M1 4v6h6"></path>
          <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
        </svg>
        重试
      </button>
    </div>

    <!-- 内容展示 -->
    <div v-else-if="report" class="container">
      <button @click="goBack" class="back-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <path d="M12 19l-7-7 7-7"></path>
        </svg>
        返回
      </button>

      <div class="report-content">
        <div class="tech-decoration"></div>
        
        <header class="report-header">
          <h1 class="report-title">AI行业日报 {{ formatDate(report.date) }}</h1>
          <div class="report-meta">
            <div class="meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <span>{{ formatDate(report.date) }}</span>
            </div>
            <div v-if="report.created_at" class="meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
              </svg>
              <span>生成于: {{ new Date(report.created_at).toLocaleString('zh-CN') }}</span>
            </div>
            <div v-if="report.model" class="meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 1 0 10 10H12V2z"></path>
                <path d="M20 2a10 10 0 0 1 0 20 10 10 0 0 1-20 0"></path>
                <path d="M2 12h10"></path>
                <path d="M12 2v10"></path>
              </svg>
              <span>使用模型: {{ formatModelName(report.model) }}</span>
            </div>
          </div>
        </header>

        <!-- 摘要部分 -->
        <section v-if="report.summary" class="section">
          <h2 class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            摘要
          </h2>
          <div class="content-text" v-html="report.summary"></div>
        </section>

        <!-- 主要内容部分 -->
        <section v-if="report.content" class="section">
          <h2 class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            详细内容
          </h2>
          <div class="content-text" v-html="report.content"></div>
        </section>

        <!-- 关键点部分 -->
        <section v-if="report.key_points && report.key_points.length" class="section">
          <h2 class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 11 12 14 22 4"></polyline>
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
            </svg>
            关键点
          </h2>
          <div class="section-content">
            <ul>
              <li v-for="(point, index) in report.key_points" :key="index" v-html="point"></li>
            </ul>
          </div>
        </section>

        <!-- 相关链接部分 -->
        <section v-if="report.links && report.links.length" class="section">
          <h2 class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
            </svg>
            相关链接
          </h2>
          <div class="section-content">
            <ul>
              <li v-for="(link, index) in report.links" :key="index">
                <a :href="link.url" target="_blank" rel="noopener noreferrer">{{ link.title || link.url }}</a>
              </li>
            </ul>
          </div>
        </section>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="error-container">
      <div class="error-message">未找到报告内容</div>
      <button @click="goBack" class="back-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <path d="M12 19l-7-7 7-7"></path>
        </svg>
        返回
      </button>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'

// 配置 marked 选项
marked.setOptions({
  breaks: true,  // 允许换行符转换为 <br>
  gfm: true,     // 启用 GitHub 风格的 Markdown
  headerIds: true, // 为标题生成 ID
  mangle: false,   // 不转义标题文本
  sanitize: false, // 不清理 HTML 标签
  smartLists: true, // 使用更智能的列表行为
  smartypants: true, // 使用更智能的标点符号
  xhtml: false      // 不使用 XHTML 自闭合标签
})

export default {
  name: 'ReportDetail',
  components: {
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const report = ref(null)
    const loading = ref(true)
    const error = ref(null)

    const fetchReport = async () => {
      loading.value = true
      error.value = null
      
      try {
        // 确保路由参数存在
        if (!route.params.date || route.params.date === 'undefined') {
          throw new Error('无效的报告日期')
        }
        
        const response = await fetch(`/api/reports/${route.params.date}`)
        
        if (!response.ok) {
          throw new Error(`获取报告失败: ${response.statusText}`)
        }
        
        const data = await response.json()
        if (data.success && data.data) {
          report.value = data.data
          
          // 将 Markdown 内容转换为 HTML
          if (report.value.summary) {
            report.value.summary = marked(report.value.summary)
          }
          
          // 处理其他可能包含 Markdown 的字段
          if (report.value.content) {
            report.value.content = marked(report.value.content)
          }
          
          // 处理关键点列表（如果是 Markdown 格式）
          if (report.value.key_points && Array.isArray(report.value.key_points)) {
            report.value.key_points = report.value.key_points.map(point => {
              return typeof point === 'string' ? marked(point) : point
            })
          }
        } else {
          throw new Error('获取报告数据失败')
        }
      } catch (err) {
        console.error('Error fetching report:', err)
        error.value = `获取报告失败: ${err.message}`
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      router.back()
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatModelName = (modelName) => {
      // 根据模型名称返回一个更友好的显示名称
      if (!modelName) return '未知模型';
      
      const modelMap = {
        'Grok': 'Grok AI',
        'DeepSeek': 'DeepSeek AI',
        'None': '未知模型'
      };
      
      return modelMap[modelName] || modelName;
    }

    onMounted(() => {
      fetchReport()
    })

    return {
      report,
      loading,
      error,
      fetchReport,
      goBack,
      formatDate,
      formatModelName
    }
  }
}
</script>

<style scoped>
.report-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  color: var(--text-color);
}

.back-button {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  margin-bottom: 2rem;
}

.back-button:hover {
  background-color: var(--primary-color-dark);
}

.back-button svg {
  margin-right: 0.5rem;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

.error-message {
  color: var(--error-color);
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.report-content {
  background-color: var(--card-bg-color);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.tech-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, var(--primary-color-light) 0%, transparent 70%);
  opacity: 0.3;
  border-radius: 0 0 0 100%;
  z-index: 0;
}

.report-header {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.report-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.report-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  font-size: 0.9rem;
  color: var(--text-color-light);
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item svg {
  width: 18px;
  height: 18px;
  margin-right: 0.5rem;
}

.section {
  margin-bottom: 2.5rem;
  position: relative;
  z-index: 1;
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.section-title svg {
  width: 24px;
  height: 24px;
  margin-right: 0.5rem;
}

.content-text, .section-content {
  line-height: 1.6;
  color: var(--text-color);
}

/* Markdown 样式 */
:deep(.content-text), :deep(.section-content) {
  /* 标题样式 */
  h1, h2, h3, h4, h5, h6 {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
    line-height: 1.25;
    color: var(--heading-color);
  }
  
  /* 统一标题字体大小 */
  h1 { font-size: 1.8rem; }
  h2 { font-size: 1.6rem; }
  h3 { font-size: 1.4rem; }
  h4 { font-size: 1.2rem; }
  h5 { font-size: 1.1rem; }
  h6 { font-size: 1rem; }
  
  /* 段落样式 */
  p {
    margin-bottom: 1rem;
    font-size: 1rem;
    line-height: 1.6;
  }
  
  /* 列表样式 */
  ul, ol {
    margin-bottom: 1rem;
    padding-left: 2rem;
  }
  
  li {
    margin-bottom: 0.5rem;
    font-size: 1rem;
    line-height: 1.6;
  }
  
  /* 链接样式 */
  a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.2s;
  }
  
  a:hover {
    text-decoration: underline;
    color: var(--primary-color-dark);
  }
  
  /* 引用样式 */
  blockquote {
    border-left: 4px solid var(--primary-color-light);
    padding-left: 1rem;
    margin-left: 0;
    margin-right: 0;
    font-style: italic;
    color: var(--text-color-light);
  }
  
  /* 代码样式 */
  code {
    background-color: var(--code-bg-color);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: monospace;
    font-size: 0.9em;
  }
  
  pre {
    background-color: var(--code-bg-color);
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
    margin-bottom: 1rem;
  }
  
  pre code {
    background-color: transparent;
    padding: 0;
  }
  
  /* 表格样式 */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
  }
  
  th, td {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
  }
  
  th {
    background-color: var(--table-header-bg);
    font-weight: 600;
  }
  
  /* 水平线样式 */
  hr {
    border: 0;
    height: 1px;
    background-color: var(--border-color);
    margin: 2rem 0;
  }
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.news-item {
  background-color: var(--card-bg-color-light);
  border-radius: 6px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.news-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.news-link {
  display: block;
  padding: 1.25rem;
  color: var(--text-color);
  text-decoration: none;
}

.news-title {
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
  color: var(--heading-color);
}

.news-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: var(--text-color-light);
}

.papers-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.paper-item {
  background-color: var(--card-bg-color-light);
  border-radius: 6px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.paper-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.paper-link {
  display: block;
  padding: 1.5rem;
  color: var(--text-color);
  text-decoration: none;
}

.paper-title {
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
  color: var(--heading-color);
}

.paper-authors {
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  color: var(--text-color-light);
  font-style: italic;
}

.paper-summary {
  font-size: 0.95rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.paper-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--text-color-light);
}

@media (max-width: 768px) {
  .report-title {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .news-grid {
    grid-template-columns: 1fr;
  }
  
  .report-content {
    padding: 1.5rem;
  }
}
</style>
