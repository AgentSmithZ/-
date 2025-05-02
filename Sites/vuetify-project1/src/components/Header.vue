<!-- Шаблон Vue -->
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
        <div v-if="isAuthenticated">
          <v-btn class="text-none" variant="text" @click="logout">Выйти</v-btn>
        </div>
        <div v-else>
          <v-btn href="/auth" class="text-none" append-icon="mdi-login" variant="text">
            Войти
          </v-btn>
        </div>
      </div>
    </v-app-bar>
  </v-container>
</template>

<!-- Стили -->
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

<!-- Скрипт -->
<script>
import logossite from '@/assets/yin-yang.png';

export default {
  data() {
    return {
      logosite: logossite,
      isAuthenticated: false, // флаг авторизации
    };
  },

  methods: {
    // Выход из аккаунта
    logout() {
      localStorage.removeItem('token'); // удаляем токен
      this.isAuthenticated = false; // меняем флаг авторизации
      window.location.href = '/'; // переходим на главную страницу
    },

    // Проверка наличия токена при загрузке страницы
    checkAuth() {
      const token = localStorage.getItem('token');
      this.isAuthenticated = !!token; // если есть токен, считаем пользователя авторизированным
    },
  },

  // Выполняем проверку при создании компонента
  created() {
    this.checkAuth();
  },
};
</script>