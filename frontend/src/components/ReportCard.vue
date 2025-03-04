<template>
  <router-link :to="`/report/${report.date}`" class="report-card card tech-glow">
    <div class="card-content">
      <div class="card-header">
        <div class="date-chip">
          <div class="date-dot"></div>
          <span>{{ formatSimpleDate(report.date) }}</span>
        </div>
        <h3 class="report-title">AI行业日报</h3>
      </div>
      <div class="card-decoration">
        <div class="tech-line"></div>
      </div>
      <div class="card-footer">
        <div class="tech-stats">
          <div class="stat-item">
            <div class="stat-icon"></div>
            <span>AI资讯</span>
          </div>
        </div>
      </div>
    </div>
    <div class="card-overlay">
      <span class="read-more">阅读详情</span>
    </div>
    <div class="card-bg-decoration">
      <div class="bg-circle"></div>
      <div class="bg-line"></div>
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
    formatSimpleDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric'
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
  min-height: 180px;
  justify-content: space-between;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: linear-gradient(135deg, rgba(17, 24, 39, 0.8), rgba(10, 14, 23, 0.9));
  transition: all var(--transition-speed) ease, background 0.3s ease, border-color 0.3s ease;
  z-index: 1;
}

.light-theme .report-card {
  border: 1px solid rgba(0, 0, 0, 0.05);
  background: linear-gradient(135deg, rgba(240, 242, 245, 0.8), rgba(255, 255, 255, 0.9));
}

.card-content {
  position: relative;
  z-index: 2;
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.date-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.8rem;
  background: rgba(0, 163, 255, 0.1);
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--primary-color);
  width: fit-content;
  border: 1px solid rgba(0, 163, 255, 0.2);
}

.date-dot {
  width: 8px;
  height: 8px;
  background-color: var(--primary-color);
  border-radius: 50%;
  animation: pulse 2s infinite alternate;
}

.report-title {
  font-size: 1.5rem;
  font-weight: 700;
  text-align: left;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px rgba(0, 163, 255, 0.3);
  letter-spacing: 0.5px;
}

.light-theme .report-title {
  text-shadow: 0 0 10px rgba(0, 149, 255, 0.3);
}

.card-decoration {
  position: relative;
  width: 100%;
  height: 20px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin: auto 0;
}

.tech-line {
  height: 2px;
  width: 70%;
  background: linear-gradient(90deg, var(--primary-color), transparent);
  position: relative;
}

.tech-line::before, .tech-line::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--primary-color);
  top: 50%;
  transform: translateY(-50%);
}

.tech-line::before {
  left: 0;
  box-shadow: 0 0 10px var(--primary-color);
}

.card-footer {
  margin-top: auto;
}

.tech-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.stat-icon {
  width: 12px;
  height: 12px;
  border: 1px solid var(--primary-color);
  border-radius: 50%;
  position: relative;
}

.stat-icon::before {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  background-color: var(--primary-color);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 1.5rem;
  opacity: 0;
  transition: opacity var(--transition-speed) ease;
  z-index: 3;
}

.light-theme .card-overlay {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.5), transparent);
}

.read-more {
  color: white;
  font-weight: 500;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  transform: translateY(20px);
  transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

.read-more::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.7s ease;
}

.card-bg-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  opacity: 0.1;
  transition: opacity var(--transition-speed) ease;
}

.bg-circle {
  position: absolute;
  top: -50px;
  right: -50px;
  width: 150px;
  height: 150px;
  border: 1px dashed var(--primary-color);
  border-radius: 50%;
}

.bg-line {
  position: absolute;
  bottom: 30px;
  left: 0;
  width: 50%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
}

.report-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px var(--shadow-color), 0 0 20px var(--glow-color);
  border-color: rgba(0, 163, 255, 0.3);
}

.light-theme .report-card:hover {
  border-color: rgba(0, 149, 255, 0.3);
}

.report-card:hover .card-overlay {
  opacity: 1;
}

.report-card:hover .read-more {
  transform: translateY(0);
  box-shadow: 0 5px 15px var(--shadow-color);
}

.report-card:hover .read-more::before {
  left: 100%;
}

.report-card:hover .card-bg-decoration {
  opacity: 0.2;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.2);
    opacity: 0.7;
    box-shadow: 0 0 10px var(--primary-color);
  }
}
</style>
