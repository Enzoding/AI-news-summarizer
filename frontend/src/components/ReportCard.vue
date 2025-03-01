<template>
  <router-link :to="`/report/${report.date}`" class="report-card card tech-glow">
    <div class="report-date">{{ formatDate(report.date) }}</div>
    <h3 class="report-title">AI行业日报</h3>
    <p class="report-summary">{{ truncateSummary(report.summary) }}</p>
    <div class="report-stats">
      <div class="stat">
        <span class="stat-icon">📰</span>
        <span class="stat-value">{{ report.news_count || 0 }}条新闻</span>
      </div>
      <div class="stat">
        <span class="stat-icon">📄</span>
        <span class="stat-value">{{ report.paper_count || 0 }}篇论文</span>
      </div>
    </div>
    <div class="card-overlay">
      <span class="read-more">阅读详情</span>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'ReportCard',
  props: {
    report: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      });
    },
    truncateSummary(summary) {
      if (!summary) return '';
      return summary.length > 100 ? summary.substring(0, 100) + '...' : summary;
    }
  }
}
</script>

<style scoped>
.report-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.report-date {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.report-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
  font-weight: 700;
}

.report-summary {
  flex-grow: 1;
  margin-bottom: 1rem;
  line-height: 1.6;
  color: var(--text-color);
}

.report-stats {
  display: flex;
  gap: 1rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.stat-icon {
  font-size: 1.1rem;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 1.5rem;
  opacity: 0;
  transition: opacity var(--transition-speed) ease;
}

.read-more {
  color: white;
  font-weight: 500;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  transform: translateY(20px);
  transition: transform var(--transition-speed) ease;
}

.report-card:hover .card-overlay {
  opacity: 1;
}

.report-card:hover .read-more {
  transform: translateY(0);
}
</style>
