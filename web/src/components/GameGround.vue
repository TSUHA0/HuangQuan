<template>

  <PlayerGround id="play-ground-2"></PlayerGround>
  <PlayerGround id="play-ground-3"></PlayerGround>
  <PlayerGround id="play-ground-4"></PlayerGround>
  <div style="position: absolute; left: 50vw;bottom: 55vh;width: 10vw"
  >{{ selectCardId }}
  </div>
  <button v-show="selectCardId > -1"
          style="position: absolute; left: 20vw;bottom: 25vh;width: 10vw"
          @click="playCard">
    出牌
  </button>

  <button v-show="selectCardId > -1"
          style="position: absolute; left: 40vw;bottom: 25vh;width: 10vw"
          @click="playCard">
    弃牌
  </button>
  <MyGround :handcardArr="handcardArr" :selectCardId="selectCardId"
            id="play-ground-1"></MyGround>
</template>

<script>
import PlayerGround from "@/components/PlayerGround";
import MyGround from "@/components/MyGround";
import {ref, provide} from "vue";

export default {
  name: "GameGround",
  components: {MyGround, PlayerGround},
  setup() {
    let selectCardId = ref(-1);
    const updateSelectCardId = (newId) => {
      selectCardId.value = newId;
    };
    provide("updateSelectCardId", updateSelectCardId);
    provide("selectCardId", selectCardId);
    return {
      selectCardId,
      updateSelectCardId
    };
  },
  data() {
    return {
      handcardArr: [1, 2, 3],
    };
  },
  methods: {
    // playCard() {
    //   let item = this.handcardArr;
    //   for (var i = 0; i < item.length; i++) {
    //     if (item[i].isSelect) {
    //       item.splice(i, 1);
    //       this.selectCardId = -1;
    //       //do play card
    //     }
    //   }
    // },
  },
};
</script>

<style scoped>

</style>