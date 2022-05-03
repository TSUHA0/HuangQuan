<template>
  <div>
    <div class="my-ground-information-blue">
    </div>
    <div class="my-ground-information-red">
    </div>
    <div class="my-ground-information-gray">
    </div>
    <HandCard v-for="(item,i) in handCard" :key="i" :cardId="item" :idx="i"
              :bottom="item == selectCardId ? bt6 : bt0"
              @selectback="getSelectback">
    </HandCard>

    <div class="my-ground-behind-character">
      <img src="https://img.win3000.com/m00/06/ac/9e46cfd309a8aa2c7ef0b16ed50296be_c_345_458.jpg"
           style="height: 100%;width: 100%">
    </div>
    <div class="my-ground-front-character">
      傀儡
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
    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;

    const updateSelectCardId = inject("updateSelectCardId");
    const selectCardId = inject("selectCardId");
    return {
      selectCardId,
      updateSelectCardId,
      handCard
    };
  },
  data() {
    return {
      bt0: "bottom:0vh;",
      bt6: "bottom:6vh;"
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
  },
};
</script>

<style scoped>

</style>