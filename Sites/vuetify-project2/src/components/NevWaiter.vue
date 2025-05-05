<template>
  <v-app>
    <v-container fluid>
      <v-row align="center" justify="space-between">
        <v-col cols="12" md="6">
          <h1>Заказы официантов</h1>
        </v-col>
        <v-col cols="12" md="6" class="text-right">
          <v-btn color="primary" @click="dialogCreateOrder = true">Новый заказ</v-btn>
        </v-col>
      </v-row>

      <!-- Таблица заказов -->
      <v-data-table
        :headers="headers"
        :items="orders"
        hide-default-header
        class="my-4 elevation-1"
        :search="search"
        dense
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Поиск..."
              single-line
              hide-details
            ></v-text-field>
          </v-toolbar>
        </template>
      </v-data-table>

      <!-- Диалог создания заказа -->
      <v-dialog v-model="dialogCreateOrder" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Новый заказ</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="newOrder.tableNumber"
                    label="Номер стола"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="newOrder.guestCount"
                    label="Количество гостей"
                    type="number"
                    min="1"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-autocomplete
                    v-model="newOrder.dishIds"
                    :items="menuItems"
                    item-text="title"
                    item-value="id"
                    label="Блюда и напитки"
                    multiple
                    chips
                    deletable-chips
                  ></v-autocomplete>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialogCreateOrder = false">Отмена</v-btn>
            <v-btn color="blue darken-1" text @click="createNewOrder">Создать заказ</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </v-app>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const search = ref('');
    const dialogCreateOrder = ref(false);
    const orders = ref([]); // Массив заказов
    const headers = [
      { text: 'Стол №', value: 'tableNumber' },
      { text: 'Кол-во гостей', value: 'guestCount' },
      { text: 'Дата', value: 'dateCreated' },
      { text: 'Сумма', value: 'totalAmount' },
    ];

    const newOrder = reactive({
      tableNumber: null,
      guestCount: null,
      dishIds: []
    });

    const menuItems = [
      { id: 1, title: 'Борщ', price: 200 },
      { id: 2, title: 'Стейк', price: 1700 },
      { id: 3, title: 'Кофе', price: 100 },
      { id: 4, title: 'Пирожок', price: 50 },
    ];

    onMounted(() => {
      fetchOrders();
    });

    function fetchOrders() {
      axios.get('http://localhost:8000/orders').then(response => {
        orders.value = response.data; // Обновляем массив заказов
      }).catch(error => {
        console.error('Ошибка при получении заказов:', error.response?.data || error.message);
      });
    }

    function createNewOrder() {
      axios.post('http://localhost:8000/orders/', {
        table_number: newOrder.tableNumber,
        guest_count: newOrder.guestCount,
        items: newOrder.dishIds,
        user_id: 1  // Предполагается, что user_id равен 1
      }).then(response => {
        alert('Заказ успешно создан!');
        dialogCreateOrder.value = false;
        fetchOrders();  // Самое важное: обновление списка заказов после создания
      }).catch(error => {
        console.error('Ошибка при создании заказа:', error.response?.data || error.message);
      });
    }

    return {
      search,
      dialogCreateOrder,
      orders,
      headers,
      newOrder,
      menuItems,
      fetchOrders,
      createNewOrder
    };
  }
};
</script>

<style scoped>
.headline {
  font-size: 24px !important;
  font-weight: bold;
}
</style>