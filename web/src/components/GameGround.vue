<template>
  <div>
    <div> 牌堆</div>
    <button @click="drawCard(1)">抽 1 张牌</button>
    <br>
    <button style="margin-top: 1vh" @click="drawCard(2)">抽 2 张牌</button>
    <PlayerGround id="play-ground-2" :loc="loc[1]"></PlayerGround>
    <PlayerGround id="play-ground-3" :loc="loc[2]"></PlayerGround>
    <PlayerGround id="play-ground-4" :loc="loc[3]"></PlayerGround>
    <PlayerGround id="play-ground-5" :loc="loc[4]"></PlayerGround>
    <PlayerGround id="play-ground-6" :loc="loc[5]"></PlayerGround>

    <UsedCard id="play-ground-used-card"></UsedCard>

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
    <MyGround :selectCardId="selectCardId" id="play-ground-1"></MyGround>
  </div>
  <ActionLog></ActionLog>

</template>

<script>
import PlayerGround from "@/components/PlayerGround";
import MyGround from "@/components/MyGround";
import UsedCard from "@/components/UsedCard";
import ActionLog from "@/components/ActionLog";
import {inject, toRefs} from "vue";
import {store} from "@/plugin/store";

export default {
  name: "GameGround",
  components: {MyGround, PlayerGround, UsedCard, ActionLog},
  setup() {
    const players = inject("players");
    const playerNum = inject("playerNum");
    const pos = inject("pos");
    const selectCardId = inject("selectCardId");
    const cardUsedId = inject("cardUsedId");
    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;

    console.log("playerNum", playerNum.value);
    let loc = [];
    for (let i = pos.value + 1, cnt = 0; cnt < 10; ++i, ++cnt) {
      i = ((i - 1) % playerNum.value) + 1;
      loc.push(i);
    }
    console.log(loc);
    return {
      players,
      playerNum,
      pos,
      selectCardId,
      handCard,
      cardUsedId,
      loc
    };
  },
  methods: {
    playCard() {
      for (var i = 0; i < this.handCard.length; i++) {
        if (this.selectCardId === this.handCard[i]) {
          this.handCard.splice(i, 1);
          this.cardUsedId = this.selectCardId;
          this.selectCardId = -1;
          //do play card
        }
      }
    },
    drawCard(num) {
      store.state.wss.send(JSON.stringify(
          {
            "event": "draw_card",
            "cardnum": num,
          }
      ));
    }
  },
};
</script>

<style scoped>

</style>