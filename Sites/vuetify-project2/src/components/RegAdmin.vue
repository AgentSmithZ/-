<template>
    <v-container class="mt-4 bg-surface-variant">
      <div class="d-flex justify-center">
        <v-btn style="margin-bottom: 10px;">
          Новый пользователь

          <v-overlay
            activator="parent"
            location-strategy="connected"
            scroll-strategy="block"
          >
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-container>
              <v-card style="padding:50px;">
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
                    single
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
            </v-card>
            </v-container>
          </v-form>
          </v-overlay>
        </v-btn>
      </div>
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
      login: "",               // Поле ввода логина
      password: "",            // Поле ввода пароля
      selectedRoles: [],       // Выбранные роли пользователя
      headers: [               // Колонки таблицы с пользователями
        { title: "ID", key: "id" },
        { title: "Логин", key: "login" },
        { title: "Роли", key: "roles" },
        { title: "Действия", key: "actions", sortable: false },
      ],
      users: [],               // Список загруженных пользователей
      
      // Правила валидации формы
      loginRules: [
        (v) => !!v || "Логин обязателен!",
        (v) => (/^[\w\d]{3,}$/.test(v)) || "Логин должен состоять минимум из трёх символов."
      ],
      passwordRules: [
        (v) => !!v || "Пароль обязателен!",
        (v) => (/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$/.test(v)) || "Пароль должен содержать минимум 6 символов, цифру, строчную и заглавную буквы."
      ],
      selectRules: [
        (v) => v.length >= 1 || "Выберите хотя бы одну роль!"
      ]
    };
  },

  methods: {
  async onRegisterClick() {
    if (this.$refs.form.validate()) {
      const body = {
        login: this.login,
        password: this.password,
        roles: this.selectedRoles, // НЕОБХОДИМО оставить массивом, а не строкой
      };

      try {
        const response = await fetch("/users/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const data = await response.json();
        alert("Пользователь успешно зарегистрирован!");
        this.loadUsers(); // Перезагрузка списка пользователей
      } catch (error) {
        console.error("Ошибка при регистрации:", error);
        alert("Ошибка при регистрации пользователя. Попробуйте снова позже.");
      }
    }
  },
  // Другие методы остаются прежними

    /**
     * Загружает список всех пользователей с сервера.
     */
    async loadUsers() {
      try {
        const response = await fetch("/users/list");
        if (!response.ok) {
          throw new Error(`Ошибка сервера: ${response.statusText}`);
        }
        
        const data = await response.json();
        this.users = data.map(u => ({ 
          id: u.id, 
          login: u.login, 
          roles: u.roles 
        }));
      } catch (error) {
        console.error("Ошибка при загрузке пользователей:", error);
      }
    },

    /**
     * Методы для редактирования и удаления пока заглушены.
     */
    editItem(item) {},
    deleteItem(item) {}
  },

  /**
   * Загружаем пользователей сразу при монтировании компонента.
   */
  created() {
    this.loadUsers();
  }
};
</script>
  
  <style scoped>
  .registeradmin {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  </style>