<template>
  <div>
    <div
        style="border-style: inset;width: 5vw;background: gainsboro;text-align: center;margin-bottom: 1vh;
        position: relative;left: 0.5vw">
      牌堆
    </div>
    <button @click="drawCard(1)">抽 1 张牌</button>
    <br>
    <button style="margin-top: 1vh" @click="drawCard(2)">抽 2 张牌</button>
    <PlayerGround id="play-ground-2" :loc="loc[1]"></PlayerGround>
    <PlayerGround id="play-ground-3" :loc="loc[2]"></PlayerGround>
    <PlayerGround id="play-ground-4" :loc="loc[3]"></PlayerGround>
    <PlayerGround id="play-ground-5" :loc="loc[4]"></PlayerGround>
    <PlayerGround id="play-ground-6" :loc="loc[5]"></PlayerGround>

    <UsedCard v-if="cardUsedId !== 0" id="play-ground-used-card"></UsedCard>

    <button v-show="selectCardId > -1"
            style="position: absolute; left: 15vw;bottom: 35vh;width: 7vw"
            @click="playCard('打出了')">
      出牌
    </button>

    <button v-show="selectCardId > -1"
            style="position: absolute; left: 25vw;bottom: 35vh;width: 7vw"
            @click="deliverCard">
      传递
    </button>

    <button v-show="selectCardId > -1"
            style="position: absolute; left: 35vw;bottom: 35vh;width: 7vw"
            @click="playCard('弃置了')">
      弃牌
    </button>

    <button v-show="selectCardId > -1"
            style="position: absolute; left: 45vw;bottom: 35vh;width: 10vw"
            @click="handReplace">
      代替传送密函
    </button>


    <button v-show="selectCardId > -1 && selectUsername !== ''"
            style="position: absolute; left: 57vw;bottom: 35vh;width: 7vw"
            @click="secret_play_card">
      对其打出
    </button>

    <button v-show="selectCardId > -1 && selectUsername !== ''"
            style="position: absolute; left: 67vw;bottom: 35vh;width: 7vw"
            @click="handToReceive">
      密函置于
    </button>


    <div v-show="selectUsername !== '' "
         style="position: absolute; left: 15vw;bottom: 50vh;width: 60vw;">
      <button @click="sendDeliverCard" style="margin-right: 2vw">密函传递</button>
      <button @click="showRoleInfo" style="margin-right: 2vw">查看道牌</button>
      <button @click="handTohand" style="margin-right: 2vw">抽他一张</button>
      <button @click="showReceiveInfo" style="margin-right: 2vw;width: 10vw">查看已接收密函</button>
    </div>

    <MyGround :selectCardId="selectCardId" id="play-ground-1"></MyGround>
  </div>
  <ActionLog></ActionLog>
  <div v-if="receiveInfoIsShow">
    <ReceiveInfo></ReceiveInfo>
  </div>
</template>

<script>
import PlayerGround from "@/components/PlayerGround";
import MyGround from "@/components/MyGround";
import UsedCard from "@/components/UsedCard";
import ActionLog from "@/components/ActionLog";
import ReceiveInfo from "@/components/ReceiveInfo";
import {inject, provide, reactive, ref, toRefs} from "vue";
import {store} from "@/plugin/store";
import g_secretCard from "@/plugin/secretcard";

export default {
  name: "GameGround",
  components: {MyGround, PlayerGround, UsedCard, ActionLog, ReceiveInfo},
  setup() {
    const players = inject("players");
    const playerNum = inject("playerNum");
    const pos = inject("pos");
    const selectCardId = inject("selectCardId");
    const cardUsedId = inject("cardUsedId");
    const deliverStatus = inject("deliverStatus");
    const selectUsername = inject("selectUsername");
    const updateActionLog = inject("updateActionLog");
    const cardUsedOwner = inject("cardUsedOwner");
    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;
    let recInfoArr = reactive({
      blue: [],
      red: [],
      gray: []
    });

    let receiveInfoIsShow = ref(false);

    console.log("playerNum", playerNum.value);
    let loc = [];
    for (let i = pos.value + 1, cnt = 0; cnt < 10; ++i, ++cnt) {
      i = ((i - 1) % playerNum.value) + 1;
      loc.push(i);
    }

    provide("receiveInfoIsShow", receiveInfoIsShow);
    provide("recInfoArr", recInfoArr);
    return {
      recInfoArr,
      receiveInfoIsShow,
      players,
      playerNum,
      pos,
      selectCardId,
      handCard,
      cardUsedId,
      loc,
      deliverStatus,
      selectUsername,
      updateActionLog,
      cardUsedOwner
    };
  },
  methods: {
    handReplace() {
      let id = this.selectCardId;
      for (let i = 0; i < this.handCard.length; i++) {
        if (this.selectCardId === this.handCard[i]) {
          this.handCard.splice(i, 1);
          this.selectCardId = -1;
        }
      }
      let my_name = window.sessionStorage.getItem("username");
      let update_msg = my_name + "使用了一张手牌来代替传送中的密函";
      store.state.wss.send(JSON.stringify(
          {
            "event": "hand_replace_deliver",
            "username": my_name,
            "cardid": id,
            "update_msg": update_msg
          }
      ));
    },
    handTohand() {
      let my_name = window.sessionStorage.getItem("username");
      let update_msg = my_name + "抽了" + this.selectUsername + "一张手牌";
      store.state.wss.send(JSON.stringify(
          {
            "event": "hand_to_hand",
            "username": my_name,
            "target": this.selectUsername,
            "update_msg": update_msg
          }
      ));
    },
    showRoleInfo() {
      let my_name = window.sessionStorage.getItem("username");
      let update_msg = my_name + "查看了" + this.selectUsername + "的道牌(身份)";
      store.state.wss.send(JSON.stringify(
          {
            "event": "show_role_info",
            "username": window.sessionStorage.getItem("username"),
            "target": this.selectUsername,
            "update_msg": update_msg
          }
      ));
    },
    handToReceive() {
      let id = this.selectCardId;
      for (let i = 0; i < this.handCard.length; i++) {
        if (this.selectCardId === this.handCard[i]) {
          this.handCard.splice(i, 1);
          this.selectCardId = -1;
        }
      }
      let update_msg = window.sessionStorage.getItem("username") + "将密函<<" + g_secretCard[id].imgtag + ">>置于" + this.selectUsername;
      store.state.wss.send(JSON.stringify(
          {
            "event": "hand_to_receive",
            "username": window.sessionStorage.getItem("username"),
            "target": this.selectUsername,
            "cardid": id,
            "update_msg": update_msg
          }
      ));
    },
    showReceiveInfo() {
      this.receiveInfoIsShow = true;
      for (let i = 0; i < this.players.arr.length; ++i) {
        if (this.selectUsername === this.players.arr[i].username) {
          this.recInfoArr.blue = this.players.arr[i].blue;
          this.recInfoArr.red = this.players.arr[i].red;
          this.recInfoArr.gray = this.players.arr[i].gray;
        }
      }
    },
    playCard(msg) {
      for (var i = 0; i < this.handCard.length; i++) {
        if (this.selectCardId === this.handCard[i]) {
          this.handCard.splice(i, 1);
          this.cardUsedId = this.selectCardId;
          this.selectCardId = -1;
          //do play card
          this.cardUsedOwner = window.sessionStorage.getItem("username");
        }
      }
      let update_msg = window.sessionStorage.getItem("username") + msg + g_secretCard[this.cardUsedId].name;
      store.state.wss.send(JSON.stringify(
          {
            "event": "play_card",
            "username": window.sessionStorage.getItem("username"),
            "cardid": this.cardUsedId,
            "update_msg": update_msg
          }
      ));
    },
    secret_play_card() {
      for (var i = 0; i < this.handCard.length; i++) {
        if (this.selectCardId === this.handCard[i]) {
          this.handCard.splice(i, 1);
          this.cardUsedId = this.selectCardId;
          this.selectCardId = -1;
          //do play card
          this.cardUsedOwner = window.sessionStorage.getItem("username");
        }
      }
      this.updateActionLog(window.sessionStorage.getItem("username") + "对" + this.selectUsername + "打出了" + g_secretCard[this.cardUsedId].name);
      store.state.wss.send(JSON.stringify(
          {
            "event": "secret_play_card",
            "username": window.sessionStorage.getItem("username"),
            "target": this.selectUsername,
            "cardid": this.cardUsedId,
          }
      ));
    },
    drawCard(num) {
      store.state.wss.send(JSON.stringify(
          {
            "event": "draw_card",
            "cardnum": num,
          }
      ));
    },
    deliverCard() {
      if (this.deliverStatus.deliverCardOwner !== "") {
        alert("场上正在传递密函");
        return;
      }
      for (let i = 0; i < this.handCard.length; i++) {
        if (this.selectCardId === this.handCard[i]) {
          this.handCard.splice(i, 1);
          //do deliver card
          this.deliverStatus.deliverCardId = this.selectCardId;
          this.selectCardId = -1;
          this.deliverStatus.deliverCardOwner = window.sessionStorage.getItem("username");
          this.deliverStatus.deliverVisual = false;
        }
      }
      this.updateActionLog(window.sessionStorage.getItem("username") + "开始传递密函");
      store.state.wss.send(JSON.stringify(
          {
            "event": "deliver_card",
            "username": window.sessionStorage.getItem("username"),
            "cardid": this.deliverStatus.deliverCardId,
            "visual": false
          }
      ));
    },
    sendDeliverCard() {
      this.deliverStatus.deliverCardOwner = this.selectUsername;
      this.updateActionLog(window.sessionStorage.getItem("username") + "将密函传递给了" + this.deliverStatus.deliverCardOwner);
      store.state.wss.send(JSON.stringify(
          {
            "event": "send_deliver_card",
            "username": window.sessionStorage.getItem("username"),
            "delivercardowner": this.selectUsername,
          }
      ));
    }
  },
};
</script>

<style scoped>

</style>