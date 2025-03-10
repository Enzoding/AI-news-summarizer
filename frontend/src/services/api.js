import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

export default {
  // 获取报告列表
  getReports(limit = 10) {
    return apiClient.get(`/api/reports?limit=${limit}`)
  },
  
  // 获取特定日期的报告
  getReportByDate(date) {
    return apiClient.get(`/api/reports/${date}`)
  },
  
  // 获取最新报告
  getLatestReport() {
    return apiClient.get('/api/reports/latest')
  },
  
  // 获取信息源列表
  getSources() {
    return apiClient.get('/api/sources')
  },
  
  // 手动触发生成报告
  generateReport() {
    return apiClient.post('/api/generate')
  },
  
  // 获取健康状态
  getHealthStatus() {
    return apiClient.get('/api/health')
  },
  
  // 获取RSS订阅链接
  getRssUrl() {
    return '/rss'
  }
}
