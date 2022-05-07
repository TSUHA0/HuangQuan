<template>
  <div :class="selectUsername === username ? 'play-ground-if-select' : ''">
    <div class="play-ground" @click="selectUser">
      <div class="play-ground-character">
        <div class="play-ground-character-username">{{ username }}</div>
        <img :src="getCharacter()"
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
      <div v-show="deliverStatus.deliverCardOwner === username" class="play-ground-deliver-card">
        <img :src="getDeliverUrl(deliverStatus.deliverCardId,deliverStatus.deliverVisual)"
             style="height: 100%;width: 100%">
      </div>
    </div>
    <div style="margin-top: -2vh;font-size: 0.9vmax">
      <p style="float: left">
        <input type="checkbox" id="cbox1" checked="checked">
        <label for="cbox1">王道</label>
      </p>
      <p style="float: left">
        <input type="checkbox" id="cbox2" checked="checked">
        <label for="cbox2">霸道</label>
      </p>
      <p style="float: left">
        <input type="checkbox" id="cbox3" checked="checked">
        <label for="cbox3">心道</label>
      </p>
    </div>
  </div>

</template>

<script>
import {inject, toRefs} from "vue";
import g_front from "@/plugin/front";
import g_secretCard from "@/plugin/secretcard";
import g_behind from "@/plugin/behind";

export default {
  name: "PlayerGround",
  props: ["loc"],
  setup(props) {
    // 一种写法
    // const {loc} = toRefs(props);
    // console.log("loc", loc.value);
    const deliverStatus = inject("deliverStatus");

    const players = inject("players");
    let myStatus = toRefs(players.arr[props.loc - 1]);

    let imagef = require.context("../assets/images/character/front/", false, /\.png$/);
    let imageb = require.context("../assets/images/character/behind/", false, /\.png$/);
    const selectUsername = inject("selectUsername");

    function getCharacter() {
      if (myStatus.witch_status.value === "front") {
        return imagef("./" + g_front[myStatus.front.value].imgtag + ".png");
      } else {
        return imageb("./" + g_behind[myStatus.front.value].imgtag + ".png");
      }
    }

    return {
      ...myStatus,
      myStatus,
      selectUsername,
      deliverStatus,
      getCharacter
    };
  },
  methods: {

    selectUser() {
      if (this.selectUsername === this.username)
        this.selectUsername = "";
      else
        this.selectUsername = this.username;
    },
    getDeliverUrl(id, visual) {
      let images = require.context("../assets/images/card/", false, /\.png$/);
      if (visual === false) return images("./" + "权皇" + ".png");
      else return images("./" + g_secretCard[id].imgtag + ".png");
    }

  }

};
</script>

<style scoped>
.play-ground {
  style: "font-size: 2vh"
}
</style>