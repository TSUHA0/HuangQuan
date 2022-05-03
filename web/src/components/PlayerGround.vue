<template>
  <div @click="log" :class="selectUsername == username ? 'play-ground-if-select' : ''">
    <div class="play-ground">
      <div>{{ username }}</div>
      <div class="play-ground-behind-character">
        <img src="https://img.win3000.com/m00/06/ac/9e46cfd309a8aa2c7ef0b16ed50296be_c_345_458.jpg"
             style="height: 100%;width: 100%">
      </div>
      <div class="play-ground-front-character">
      </div>
      <div>手牌数:{{ hand_card.length }}</div>
      <div class="play-ground-information-blue">
        {{ blue.length }}
      </div>
      <div class="play-ground-information-red">
        {{ red.length }}
      </div>
      <div class="play-ground-information-gray">
        {{ gray.length }}
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
    const players = inject("players");
    let myStatus = toRefs(players.arr[props.loc - 1]);
    const selectUsername = inject("selectUsername");

    return {
      ...myStatus,
      selectUsername
    };
  },
  methods: {
    log() {
      if (this.selectUsername === this.username)
        this.selectUsername = "";
      else
        this.selectUsername = this.username;
    }
  }

};
</script>

<style scoped>

</style>