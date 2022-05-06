<template>
  <div>
    <div class="my-ground-information-blue">
      {{ blue.length }}
    </div>
    <div class="my-ground-information-red">
      {{ red.length }}
    </div>
    <div class="my-ground-information-gray">
      {{ gray.length }}
    </div>
    <HandCard v-for="(item,i) in handCard" :key="i" :cardId="item" :idx="i"
              :bottom="item === selectCardId ? bt6 : bt0"
              @selectback="getSelectback">
    </HandCard>

    <div :class="selectUsername === username ? 'my-ground-if-select' : '' ">
    </div>
    <div @click="selectUser" class="my-ground-behind-character">
      <img src="@/assets/images/character/张良.png"
           style="height: 100%;width: 100%">
    </div>
    <div @click="selectUser" class="my-ground-front-character">
      <img src="@/assets/images/character/刺客.png"
           style="height: 100%;width: 100%">
    </div>
    <div class="my-ground-deliver-card">
      <img src="@/assets/images/card/权皇.png"
           style="height: 100%;width: 100%">
    </div>
  </div>
</template>

<script>
import HandCard from "@/components/HandCard";
import {inject, toRefs} from "vue";

export default {
  name: "MyGround",
  components: {HandCard},
  setup() {
    const players = inject("players");
    const pos = inject("pos");
    const selectUsername = inject("selectUsername");

    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;

    const updateSelectCardId = inject("updateSelectCardId");
    const selectCardId = inject("selectCardId");
    return {
      selectCardId,
      updateSelectCardId,
      handCard,
      selectUsername,
      ...myStatus
    };
  },
  data() {
    return {
      bt0: "bottom:0vh;",
      bt6: "bottom:10vh;"
    };
  },
  methods: {
    getSelectback(cardId) {
      for (var i = 0; i < this.handCard.length; i++) {
        var item = this.handCard[i];
        if (item == cardId) {
          if (this.selectCardId == cardId) {
            this.updateSelectCardId(-1);
          } else {
            this.updateSelectCardId(item);
          }
        }
      }
    },
    selectUser() {
      if (this.selectUsername === this.username)
        this.selectUsername = "";
      else
        this.selectUsername = this.username;
    }
  },
};
</script>

<style scoped>

</style>