<template>
  <div>
    <div
        style="position: absolute; bottom: 18vh;left: 1vw; width: 3vw;border-style: inset; background: gainsboro;text-align: center">
      {{ role }}
    </div>
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
      <img :src="behindReq"
           style="height: 100%;width: 100%">
    </div>
    <div @click="selectUser" class="my-ground-front-character">
      <img :src="frontReq"
           style="height: 100%;width: 100%">
    </div>
    <div v-show="deliverStatus.deliverCardOwner === username" class="my-ground-deliver-card">
      <img :src="getDeliverUrl(deliverStatus.deliverCardId,deliverStatus.deliverVisual)"
           style="height: 100%;width: 100%">
      <button @click="acceptDeliver"
              style="position: absolute;left: 5vw;bottom: 2vh">接收密函
      </button>
    </div>
    <button v-show="witch_status === 'front'" @click="behindCome"
            style="position: absolute;left: 92vw;bottom: 32vh">幕后登场
    </button>
    <button @click="showDeliver" style="position: absolute;left: 89vw;bottom: 38vh;width: 10vw;height: 4vh">
      看传递密函
    </button>
    <button @click="reverseDeliver" style="position: absolute;left: 89vw;bottom: 44vh;width: 10vw;height: 4vh;">
      传递密函翻面
    </button>
  </div>
</template>

<script>
import HandCard from "@/components/HandCard";
import {inject, toRefs} from "vue";
import g_secretCard from "@/plugin/secretcard";
import g_behind from "@/plugin/behind";
import g_front from "@/plugin/front";
import {store} from "@/plugin/store";

export default {
  name: "MyGround",
  components: {HandCard},
  setup() {
    const players = inject("players");
    const pos = inject("pos");
    const selectUsername = inject("selectUsername");
    const deliverStatus = inject("deliverStatus");
    const updateActionLog = inject("updateActionLog");

    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;
    let behindReq = require("@/assets/images/character/behind/" + g_behind[myStatus.behind.value].imgtag + ".png");
    let frontReq = require("@/assets/images/character/front/" + g_front[myStatus.front.value].imgtag + ".png");

    const updateSelectCardId = inject("updateSelectCardId");
    const selectCardId = inject("selectCardId");
    return {
      updateActionLog,
      selectCardId,
      updateSelectCardId,
      handCard,
      selectUsername,
      ...myStatus,
      deliverStatus,
      behindReq,
      frontReq
    };
  },
  data() {
    return {
      bt0: "bottom:0vh;",
      bt6: "bottom:10vh;"
    };
  },
  methods: {
    showDeliver() {
      this.deliverStatus.deliverVisual = true;
      store.state.wss.send(JSON.stringify(
          {
            "event": "update_action_log",
            "update_msg": window.sessionStorage.getItem("username") + "查看了传送中的密函"
          }
      ));
    },
    reverseDeliver() {
      this.deliverStatus.deliverVisual = true;
      store.state.wss.send(JSON.stringify(
          {
            "event": "reverse_deliver",
            "update_msg": window.sessionStorage.getItem("username") + "翻开了传送中的密函"
          }
      ));
    },
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
    },
    getDeliverUrl(id, visual) {
      let images = require.context("../assets/images/card/", false, /\.png$/);
      if (visual === false) return images("./" + "权皇" + ".png");
      else return images("./" + g_secretCard[id].imgtag + ".png");
    },
    acceptDeliver() {
      let color = g_secretCard[this.deliverStatus.deliverCardId].color;
      if (color === "黑") {
        this.gray.push(this.deliverStatus.deliverCardId);
      } else if (color === "蓝") {
        this.blue.push(this.deliverStatus.deliverCardId);
      } else if (color === "红") {
        this.red.push(this.deliverStatus.deliverCardId);
      }
      this.deliverStatus.deliverCardOwner = "";
      store.state.wss.send(JSON.stringify(
          {
            "event": "accept_deliver",
            "cardid": this.deliverStatus.deliverCardId
          }
      ));
    },
    behindCome() {
      this.witch_status = "behind";
      store.state.wss.send(JSON.stringify(
          {
            "event": "behind_come",
          }
      ));
    }
  },
};
</script>

<style scoped>

</style>