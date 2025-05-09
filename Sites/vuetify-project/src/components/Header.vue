<template>
  <v-container class="pa-0" fluid>
    <v-app-bar elevation="0" flat class="custom-app-bar no-shadow">
    <div class="content">
        <v-btn href="/" icon>
          <v-img
            :src="logosite"
            width="35"
            height="35"
          ></v-img>
        </v-btn>
        <div class="btn-group">
          <v-btn
            class="text-none"
            prepend-icon="mdi-check"
            variant="text"
            href="/"
          >
            Главная
          </v-btn>
        </div>
        <v-btn
          class="text-none"
          append-icon="mdi-login"
          variant="text"
          >Войти</v-btn>
    </div>
    </v-app-bar>
  </v-container>
</template>

<style scoped>
.content {
  max-width: 1100px; 
  margin: 0 auto;  
  padding: 0 16px;
  display: flex;
  align-items: center; 
  justify-content: space-between;  
  width: 100%;
}

span {
  color:aqua;
}

.btn-group {
  display: flex;
  gap: 16px; 
  justify-content: center;  
  flex-grow: 1; 
}
</style>

<script>
  import logossite from '@/assets/yin-yang.png';

export default {
  data() {
    return {
      logosite: logossite,  // Передаём импортированный URL
    };
  },
};

</script>