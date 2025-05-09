<template>
    <v-card class="mx-auto content" elevation="24" max-width="1100">
      <v-carousel
        :continuous="false"
        show-arrows="hover"
        delimiter-icon="mdi-square"
        height="300"
        hide-delimiter-background
      >
        <v-carousel-item v-for="(slide, i) in slides" :key="i">
          <v-sheet :color="colors[i]" height="100%" tile>
            <div class="d-flex fill-height justify-center align-center">
              <div class="text-h2">{{ slide }} Slide</div>
            </div>
          </v-sheet>
        </v-carousel-item>
      </v-carousel>
    </v-card>
  </template>
  
  <script setup>
    const colors = [
      'gray-darken-1',
      'gray-darken-1',
      'gray-darken-1',
      'gray-darken-1',
      'gray-darken-1',
    ]
    const slides = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
  </script>

<style scoped>
.content{
    margin-bottom: 30px;
}
</style>