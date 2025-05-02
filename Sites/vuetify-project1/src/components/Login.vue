<template>
  <v-card class="mx-auto" prepend-icon="mdi-login" width="450" height="270">
    <template v-slot:title>
      <span class="font-weight-black">Авторизация</span>
    </template>

    <v-sheet class="mx-auto" width="300">
      <v-form fast-fail @submit.prevent="submit">
        <v-text-field
          v-model="nickname"
          :rules="nicknameRules"
          label="Nickname"
          type="text"
        ></v-text-field>

        <v-text-field
          v-model="password"
          :rules="passwordRules"
          label="Password"
          type="password"
        ></v-text-field>

        <v-btn class="mt-2" type="submit" block>Войти</v-btn>
      </v-form>
    </v-sheet>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// Данные для полей формы
const nickname = ref('');
const password = ref('');

// Правила для валидации никнейма и пароля
const nicknameRules = [
  (val) => !!val || 'Необходимо ввести ник',
];
const passwordRules = [
  (val) => !!val || 'Необходимо ввести пароль',
];

// Функция отправки формы авторизации
const submit = async () => {
  try {
    if (!nickname.value.trim() || !password.value.trim()) {
      alert('Пожалуйста, заполните все поля.');
      return;
    }

    const response = await axios.post(
      'http://localhost:8000/auth',
      {
        nickname: nickname.value,
        password: password.value,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (response.status === 200 && response.data.token) {
      localStorage.setItem('token', response.data.token); // Сохраняем токен в Local Storage

      // Переходим на нужную страницу в зависимости от никнейма
      switch(nickname.value.toLowerCase().trim()) {
        case 'admin':
          window.location.href = '/admin';
          break;
        case 'waiter':
          window.location.href = '/waiter';
          break;
        case 'cook':
          window.location.href = '/cook';
          break;
        default:
          alert('Ваш никнейм не соответствует ни одной роли');
      }
    } else {
      throw new Error('Ошибка авторизации');
    }
  } catch (error) {
    console.error('Ошибка авторизации:', error);
    alert(error.response ? error.response.data.message || 'Ошибка авторизации' : 'Ошибка сети');
  }
};
</script>