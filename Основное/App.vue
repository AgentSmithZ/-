<template>
  <v-app>
    <v-card width="400" class="mx-auto mt-5">
      <v-card-title>
        <h1 class="display1">Главная</h1>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field 
            label="Username"
            prepend-icon="mdi-account-circle" 
           />
          <v-text-field 
            type = 'password'
            label="Password"
            prepend-icon="mdi-lock" 
            append-icon="mdi-eye-off"
          />
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="success">Регистрация</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="info">Войти</v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
  </v-app>
</template>

<script setup>
  //
</script>
