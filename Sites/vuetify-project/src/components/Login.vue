<template>
    <v-card
      class="mx-auto"
      prepend-icon="mdi-login"
      width="450"
      height="270"
    >
      <template v-slot:title>
        <span class="font-weight-black">Авторизация</span>
      </template>
  
      <v-sheet class="mx-auto" width="300">
      <v-form fast-fail @submit.prevent="submit">
        <v-text-field
          v-model="nickName"
          :rules="nickNameRules"
          label="Nickname"
        ></v-text-field>
  
        <v-text-field
          v-model="passWord"
          :rules="passWordRules"
          label="Password"
          type="password"
        ></v-text-field>
  
        <v-btn class="mt-2" type="submit" block>Войти</v-btn>
      </v-form>
    </v-sheet>
    </v-card>
  </template>

  <script setup>
import { ref } from 'vue'
import axios from 'axios'

axios.post('http://localhost:8000/auth', {
  nickName: this.nickName,
  passWord: this.passWord
}, {
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true  // Если используете куки
}).then(response => {
  console.log('Успех:', response.data)
}).catch(error => {
  console.error('Ошибка:', error)
})

const nickName = ref('')
const passWord = ref('')

const submit = async () => {
  try {
    // Проверяем, что поля заполнены
    if (!nickName.value || !passWord.value) {
      alert('Пожалуйста, заполните все поля');
      return;
    }

    const response = await axios.post('http://localhost:8000/auth', {
      nickName: nickName.value,
      passWord: passWord.value
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    localStorage.setItem('user', response.data.user);
    localStorage.setItem('role', response.data.role);
    
    switch(response.data.role) {
      case 'Admin':
        window.location.href = '/admin';
        break;
      case 'Waiter':
        window.location.href = '/waiter';
        break;
      case 'Cook':
        window.location.href = '/cook';
        break;
      default:
        window.location.href = '/';
    }
    if (response.data && response.data.token) {
      localStorage.setItem('token', response.data.token);
      alert('Авторизация успешна!');
      // Перенаправление или другие действия
    } else {
      throw new Error('Неверный ответ сервера');
    }
  } catch (error) {
    console.error('Ошибка авторизации:', error);
    alert(error.response?.data?.message || 'Ошибка авторизации');
  }
}
  </script>