<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-copyright">
        <p>&copy; {{ currentYear }} AI行业信息助手</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.footer {
  background-color: rgba(18, 18, 18, 0.8);
  padding: 1rem 0;
  margin-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.light-theme .footer {
  background-color: rgba(248, 249, 250, 0.8);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-copyright {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
  position: relative;
}

.footer-copyright p {
  position: relative;
  display: inline-block;
  transition: all var(--transition-speed) ease;
}

.footer-copyright p:hover {
  color: var(--text-color);
  transform: translateY(-2px);
}
</style>
