<template>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container>
        <h2 class="registeradmin">Регистрация пользователя</h2>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="login"
              :counter="10"
              :rules="loginRules"
              label="Логин"
              required
              variant="underlined"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="password"
              :counter="10"
              :rules="passwordRules"
              label="Пароль"
              required
              variant="underlined"
              type="password"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              v-model="selectedRoles"
              :rules="selectRules"
              :items="['Администратор', 'Официант', 'Повар']"
              label="Роль"
              multiple
              chips
              close-on-click
              variant="underlined"
            />
          </v-col>
        </v-row>
        <v-btn
          :disabled="!valid"
          class="mt-2"
          text="Создать"
          type="submit"
          block
          @click.prevent="onRegisterClick"
        />
      </v-container>
    </v-form>
  
    <v-container class="mt-4 bg-surface-variant">
      <v-data-table
        :headers="headers"
        :items="users"
        density="compact"
        hover
      >
        <template #[`item.actions`]="{ item }">
          <v-icon size="small" class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
          <v-icon size="small" @click="deleteItem(item)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        valid: false,
        login: "",
        password: "",
        selectedRoles: [],
        headers: [
          { title: "ID", key: "id" },
          { title: "Логин", key: "login" },
          { title: "Роли", key: "roles" },
          { title: "Действия", key: "actions", sortable: false },
        ],
        users: [], // Массив для хранения зарегистрированных пользователей
        loginRules: [
          (v) => !!v || "Логин обязателен!",
          (v) =>
            /^[\w\d]{3,}$/.test(v) ||
            "Логин должен состоять минимум из трех символов.",
        ],
        passwordRules: [
          (v) => !!v || "Пароль обязателен!",
          (v) =>
            /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$/.test(v) ||
            "Пароль должен содержать минимум 6 символов, цифру, строчную и заглавную буквы.",
        ],
        selectRules: [
          (v) => v.length >= 1 || "Минимум одна роль обязательна!",
        ],
      };
    },
  
    methods: {
      onRegisterClick() {
        if (this.$refs.form.validate()) {
          const body = {
            login: this.login,
            password: this.password,
            roles: this.selectedRoles.join(","), // Преобразуем выбранные роли в строку
          };
  
          fetch("/users/register", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
          })
            .then((res) => res.json())
            .then((data) => {
              alert("Пользователь успешно зарегистрирован!");
              this.loadUsers(); // Загружаем список пользователей заново
            })
            .catch((err) => {
              console.error("Ошибка при регистрации:", err);
              alert("Ошибка при регистрации пользователя.");
            });
        }
      },
  
      loadUsers() {
        fetch("/users/list")
          .then((res) => res.json())
          .then((data) => {
            this.users = data.map((u) => ({
              id: u.id,
              login: u.login,
              roles: u.roles,
            }));
          })
          .catch((err) => {
            console.error("Ошибка при загрузке пользователей:", err);
          });
      },
  
      editItem(item) {}, // Пока оставим заглушку
      deleteItem(item) {}, // Оставим заглушку
    },
  
    created() {
      this.loadUsers(); // Сразу при загрузке страницы подгружаем пользователей
    },
  };
  </script>
  
  <style scoped>
  .registeradmin {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  </style>