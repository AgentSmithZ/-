<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>

</script>

<style>
canvas, iframe, video, img, hr {
  border: none !important;
  box-shadow: none !important;
  margin: 0 !important;
  padding: 0 !important;
}
html::before, html::after,
body::before, body::after,
#app::before, #app::after {
  content: none !important;
  display: none !important;
}
html, body {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  box-shadow: none !important;
  background: #f2f2f2 !important; /* или нужный тебе цвет */
}
.v-main {
  background: var(--v-theme-background) !important;
}
</style>
