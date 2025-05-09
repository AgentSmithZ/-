<template>
  <div class="content">
    <div class="cards-container">
      <div class="cards-wrapper" ref="cardsWrapper">
        <v-card
          v-for="(card, i) in cards"
          :key="i"
          class="mx-2"
          width="200"
          min-width="200"
        >
          <v-img :src="card.image" height="200px" cover></v-img>
          <v-card-text class="pb-0">{{ card.title }}</v-card-text>
          <v-card-text class="pt-0">{{ card.text }}</v-card-text>
        </v-card>
      </div>

      <v-btn
        v-if="showControls"
        icon
        class="nav-btn prev-btn"
        @click="scroll(-600)"
      >
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-btn
        v-if="showControls"
        icon
        class="nav-btn next-btn"
        @click="scroll(600)"
      >
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cards: [
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 1',
          text: 'Описание карточки 1'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 2',
          text: 'Описание карточки 2'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 3',
          text: 'Описание карточки 4'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 5',
          text: 'Описание карточки 5'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 6',
          text: 'Описание карточки 6'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 7',
          text: 'Описание карточки 7'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 1',
          text: 'Описание карточки 1'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 2',
          text: 'Описание карточки 2'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 3',
          text: 'Описание карточки 4'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 5',
          text: 'Описание карточки 5'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 6',
          text: 'Описание карточки 6'
        },
        {
          image: 'https://via.placeholder.com/300x200?text=Card+1',
          title: 'Карточка 7',
          text: 'Описание карточки 7'
        },
      ],
      showControls: false
    }
  },
  mounted() {
    this.checkOverflow();
    window.addEventListener('resize', this.checkOverflow);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkOverflow);
  },
  methods: {
    scroll(offset) {
      this.$refs.cardsWrapper.scrollBy({
        left: offset,
        behavior: 'smooth'
      });
    },
    checkOverflow() {
      const wrapper = this.$refs.cardsWrapper;
      this.showControls = wrapper.scrollWidth > wrapper.clientWidth;
    }
  }
}
</script>

<style scoped>

.cards-container {
  position: relative;
  width: 100%;
  margin: 20px 0;
}

.cards-wrapper {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  scroll-snap-type: x proximity;
  -webkit-overflow-scrolling: touch;
  padding: 10px 0;
  scroll-padding: 0 50px;
}

.cards-wrapper::-webkit-scrollbar {
  display: none;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  background: rgba(43, 43, 43, 0.7);
}
.prev-btn {
  left: 50px;
}
.next-btn {
  right: 50px;
}

.v-card {
  scroll-snap-align: start;
  flex: 0 0 auto;
  background: #FFFFFF00;
}

</style>