<template>
  <div>
    <div class="my-ground-information-blue">
      王道密函
    </div>
    <div class="my-ground-information-red">
      霸道密函
    </div>
    <div class="my-ground-information-gray">
      黑密函
    </div>
    <HandCard v-for="(item,i) in handCard" :key="i" :cardId="item" :idx="i"
              :num="handCard.length" :bottom="item == selectCardId ? bt6 : bt0"
              @selectback="getSelectback">
    </HandCard>

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

    const updateSelectCardId = inject("updateSelectCardId");
    const selectCardId = inject("selectCardId");
    return {
      selectCardId,
      updateSelectCardId,
      handCard: myStatus.hand_card
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
        console.log(this.handCard);
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