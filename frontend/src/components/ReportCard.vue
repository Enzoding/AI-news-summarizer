<template>
  <router-link :to="`/report/${report.date}`" class="report-card card tech-glow">
    <div class="card-content">
      <h3 class="report-title">AI行业日报 {{ formatSimpleDate(report.date) }}</h3>
      <div class="card-decoration">
        <div class="tech-line"></div>
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
  min-height: 120px;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: linear-gradient(135deg, rgba(30, 30, 30, 0.8), rgba(18, 18, 18, 0.9));
  transition: all var(--transition-speed) ease, background 0.3s ease, border-color 0.3s ease;
}

.light-theme .report-card {
  border: 1px solid rgba(0, 0, 0, 0.05);
  background: linear-gradient(135deg, rgba(240, 240, 240, 0.8), rgba(255, 255, 255, 0.9));
}

.card-content {
  position: relative;
  z-index: 2;
  width: 100%;
}

.report-title {
  font-size: 1.5rem;
  color: var(--primary-color);
  font-weight: 700;
  text-align: center;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 10px rgba(79, 158, 255, 0.3);
}

.light-theme .report-title {
  text-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
}

.card-decoration {
  position: relative;
  width: 100%;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tech-line {
  height: 2px;
  width: 50%;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
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
}

.tech-line::after {
  right: 0;
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

.report-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px var(--shadow-color), 0 0 20px var(--glow-color);
  border-color: rgba(79, 158, 255, 0.3);
}

.light-theme .report-card:hover {
  border-color: rgba(52, 152, 219, 0.3);
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
</style>
