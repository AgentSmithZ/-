<template>
  <v-container>
    <!-- Форма добавления -->
    <v-card class="pa-4 mb-4">
      <v-form @submit.prevent="addUser">
        <v-text-field v-model="newUser.nickname" label="Логин"></v-text-field>
        <v-text-field v-model="newUser.password" label="Пароль" type="password"></v-text-field>
        <v-select
          v-model="newUser.role_id"
          :items="roles"
          item-text="role"
          item-value="id"
          label="Роль"
        ></v-select>
        <v-btn type="submit" color="primary">Добавить</v-btn>
      </v-form>
    </v-card>

    <!-- Таблица пользователей -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="formattedUsers"
        hide-default-footer
        disable-pagination
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="changeActivation(item.id)"
          >
            {{
              item.is_active === 1
                ? 'mdi-toggle-switch-off-outline'
                : 'mdi-toggle-switch-on-outline'
            }}
          </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      newUser: {
        nickname: '',
        password: '',
        role_id: ''
      },
      users: [], // Массив пользователей
      roles: [], // Список ролей
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Логин', value: 'nickname' },
        { text: 'Роль', value: 'role' },
        { text: 'Статус', value: 'status' },
        { text: 'Действия', value: 'actions', sortable: false }
      ],
      nextId: 1 // Начальное значение ID
    };
  },
  computed: {
    formattedUsers() {
      return this.users.map((u) => ({
        ...u,
        role: this.getRoleById(u.role_id) || 'Без роли',
        status: u.is_active === 1 ? 'Активен' : 'Уволен'
      }));
    }
  },
  created() {
    this.initializeData();
  },
  methods: {
    initializeData() {
      this.roles = [
        { id: 1, role: 'Admin' },
        { id: 2, role: 'Waiter' },
        { id: 3, role: 'Cook' }
      ];

      this.users = [
        { id: 1, nickname: 'admin', password: '123456', role_id: 1, is_active: 1 },
        { id: 2, nickname: 'waiter1', password: 'password', role_id: 2, is_active: 1 },
        { id: 3, nickname: 'cook1', password: 'anotherpass', role_id: 3, is_active: 1 }
      ];
    },
    getRoleById(roleId) {
      return this.roles.find(r => r.id === roleId)?.role;
    },
    changeActivation(userId) {
      const index = this.users.findIndex(u => u.id === userId);
      if (index !== -1) {
        this.users[index].is_active = +(!this.users[index].is_active);
      }
    },
    addUser() {
      if (!this.newUser.nickname || !this.newUser.password || !this.newUser.role_id) {
        alert('Все поля обязательны!');
        return;
      }
      const newId = ++this.nextId;

      this.users.push({
        id: newId,
        nickname: this.newUser.nickname,
        password: this.newUser.password,
        role_id: parseInt(this.newUser.role_id),
        is_active: 1
      });

      this.newUser = {};
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

td, th {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.green--text {
  color: green;
}

.red--text {
  color: red;
}
</style>