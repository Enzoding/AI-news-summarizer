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
  background-color: #f1f5f9;
  padding: 1rem 0;
  margin-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.footer-copyright {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
}
</style>
