<template>
  <div @click="selectUser" :class="selectUsername === username ? 'play-ground-if-select' : ''">
    <div class="play-ground">
      <div class="play-ground-character">
        <div class="play-ground-character-username">{{ username }}</div>
        <img src="@/assets/images/character/张良.png"
             style="height: 100%;width: 100%">
        <div class="play-ground-information-blue">
          {{ blue.length }}
        </div>
        <div class="play-ground-information-red">
          {{ red.length }}
        </div>
        <div class="play-ground-information-gray">
          {{ gray.length }}
        </div>
        <div class="play-ground-card-information">手牌数:{{ hand_card.length }}</div>
      </div>
      <div v-show="deliverCardOwner === username" class="play-ground-deliver-card">
        <img src="@/assets/images/card/权皇.png"
             style="height: 100%;width: 100%">
      </div>
    </div>
  </div>
</template>

<script>
import {inject, toRefs} from "vue";

export default {
  name: "PlayerGround",
  props: ["loc"],
  setup(props) {
    // 一种写法
    // const {loc} = toRefs(props);
    // console.log("loc", loc.value);
    const deliverCardOwner = inject("deliverCardOwner");

    const players = inject("players");
    let myStatus = toRefs(players.arr[props.loc - 1]);
    const selectUsername = inject("selectUsername");

    return {
      ...myStatus,
      selectUsername,
      deliverCardOwner
    };
  },
  methods: {
    selectUser() {
      if (this.selectUsername === this.username)
        this.selectUsername = "";
      else
        this.selectUsername = this.username;
    }
  }

};
</script>

<style scoped>
.play-ground {
  style: "font-size: 2vh"
}
</style>