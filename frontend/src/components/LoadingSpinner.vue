<template>
  <div class="loading-container">
    <div class="loading-spinner">
      <div class="spinner-ring"></div>
      <div class="spinner-core"></div>
    </div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    message: {
      type: String,
      default: '加载中...'
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1.5rem;
}

.loading-spinner {
  position: relative;
  width: 60px;
  height: 60px;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.spinner-ring::before, .spinner-ring::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  border: 3px solid transparent;
}

.spinner-ring::before {
  top: 5px;
  left: 5px;
  right: 5px;
  bottom: 5px;
  border-top-color: var(--secondary-color);
  animation: spin 3s linear infinite;
}

.spinner-ring::after {
  top: 15px;
  left: 15px;
  right: 15px;
  bottom: 15px;
  border-top-color: var(--accent-color);
  animation: spin 1.5s linear infinite;
}

.spinner-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 15px;
  height: 15px;
  background-color: var(--primary-color);
  border-radius: 50%;
  box-shadow: 0 0 15px var(--primary-color);
  animation: pulse 1.5s ease-in-out infinite alternate;
}

.loading-message {
  color: var(--text-secondary);
  font-size: 1rem;
  animation: pulse 1.5s infinite alternate;
  text-shadow: 0 0 10px rgba(79, 158, 255, 0.3);
  letter-spacing: 1px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0% {
    opacity: 0.6;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1.05);
  }
}
</style>
