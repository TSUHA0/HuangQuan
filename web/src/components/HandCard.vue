<template>
  <div class="hand-card" :style=" 'position: absolute; left:' +
      (this.basePos + (this.idx + 1) * (this.handCard.length > 13 ? (75 / this.handCard.length) : 6))
      + 'vw;' + this.bottom "
       @click="sendSelectIdxback">
    手牌{{ cardId }}
  </div>
</template>

<script>

import {inject, toRefs} from "vue";


export default {
  setup(props, {emit}) {
    let basePos = 4;
    const players = inject("players");
    const pos = inject("pos");
    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;

    function sendSelectIdxback() {
      emit("selectback", props.cardId);
    }

    return {
      basePos,
      sendSelectIdxback,
      handCard
    };
  },
  props: {
    idx: Number,
    cardId: Number,
    bottom: String
  },
  name: "HandCard",
};
</script>

<style scoped>

</style>