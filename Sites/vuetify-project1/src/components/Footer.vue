<template>
    <v-footer class="text-center d-flex flex-column ga-2 py-4" color="gray-darken-1">
      <div class="content">
        <div class="d-flex ga-3">
            <v-btn
            v-for="icon in icons"
            :key="icon"
            :icon="icon"
            density="comfortable"
            variant="text"
            ></v-btn>
        </div>
    
        <v-divider class="my-2" thickness="2" width="50"></v-divider>
    
        <div class="text-caption font-weight-regular opacity-60">
            Ваши прав защищены.
        </div>
    
        <v-divider></v-divider>
    
        <div>
            {{ new Date().getFullYear() }} — <strong>MangaGate</strong>
        </div>
      </div>
    </v-footer>
  </template>
  <script setup>
    const icons = [
      'mdi-facebook',
      'mdi-twitter',
      'mdi-linkedin',
      'mdi-instagram',
    ]
  </script>

<style scoped>
.content {
  max-width: 1100px;  /* Максимальная ширина содержимого */
  margin: 0 auto;
  padding: 0 16px;  /* Отступы слева и справа */
  width: 100%;
}
</style>