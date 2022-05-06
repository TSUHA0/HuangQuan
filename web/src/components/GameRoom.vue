<template>
  <button @click="changeHand">asd</button>
  <div id="gameroom" v-if=gameRoundisShow>
    <span>房间号：</span>
    <input v-model="roomId"/>
    <div style="padding-top:20px;">
      <span style="padding-right:3vh;" @click="joinRoom"><button>加入房间</button></span>
      <span style="padding-right:3vh;" @click="gameStart"><button>开始游戏</button></span>
      <br><br><br>

      <ul style="user-select: none; margin: auto; list-style-type: none;">
        <li v-for="(item, i) in playerList" :key="i"> {{ item }}</li>
      </ul>
    </div>
  </div>
  <GameGround v-else></GameGround>

</template>

<script>
import {store} from "@/plugin/store";
import GameGround from "@/components/GameGround";
import {provide, reactive, ref} from "vue";

export default {
  name: "login",
  components: {
    GameGround
  },
  setup() {
    let roomIsShow = ref(true); //标记游戏是否开始
    let playerList = ref([""]); // 玩家名称列表
    let username = window.sessionStorage.getItem("username"); //本玩家名称
    let roomId = 0; // 房间id
    let pos = ref(0); // 标记位于几号位
    let playerNum = ref(0); //玩家数量
    let actionLog = ref(["进入房间"]); //出牌记录
    let actionNum = 0; //出牌记录计数
    let players = reactive({arr: []}); // 同步server传来的玩家对局信息
    let selectCardId = ref(-1);  //选中卡牌的id
    let selectUsername = ref(""); //选中玩家的名称
    let cardUsedId = ref(0);  //出牌的id
    let cardUsedOwner = ref(""); //出牌玩家的名称
    let floatWindowContent = ref(""); //悬浮窗内容
    let deliverCardOwner = ref("");

    const updateSelectCardId = (newId) => {
      selectCardId.value = newId;
    };

    function updateActionLog(log) {
      actionNum++;
      if (actionLog.value.length >= 10) actionLog.value.splice(0, 1);
      actionLog.value.push(actionNum + ": " + log);
    }

    function delete_player(data) {
      for (let i = 0; i < playerList.value.length; i++)
        if (playerList.value[i] === data.username) playerList.value.splice(i, 1);
    }

    function recover_game(data) {
      let players = data.players;
      for (let i = 0; i < players.length; ++i) {
        if (players[i].username === username) continue;
        playerList.value.push(players[i].username);
      }
    }

    function game_start(data) {
      roomIsShow.value = false;
      players.arr = data.data;
      playerNum.value = data.data.length;
      for (let i = 0; i < data.data.length; i++)
        if (data.data[i].username === username)
          pos.value = data.data[i].pos;
    }

    function draw_card(data) {
      let card_list = data.card_list;
      console.log("抽卡表", card_list);
      updateActionLog(data.username + "抽了" + card_list.length + "张牌");
      console.log("actionLog.arr", actionLog.value);

      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.username) {
          for (let j = 0; j < card_list.length; ++j) players.arr[i].hand_card.push(card_list[j]);
        }
      }
    }

    function wssOnMsg(e) {
      let data = JSON.parse(e.data);
      let event = data.event;
      console.log(data);

      if (event === "draw_card") draw_card(data);  //玩家抽牌

      // 以下为需要忽略username为自身的event
      if (data.username === username) return false;
      if (event === "create_player") playerList.value.push(data.username);  //添加用户进入房间
      else if (event === "recover_game") recover_game(data); //用户恢复房间状态
      else if (event === "delete_player") delete_player(data); //用户退出房间
      else if (event === "game_status") game_start(data);  //对局开始


      return true;
    }

    provide("players", players);
    provide("pos", pos);
    provide("playerNum", playerNum);
    provide("selectCardId", selectCardId);
    provide("updateSelectCardId", updateSelectCardId);
    provide("cardUsedId", cardUsedId);
    provide("selectUsername", selectUsername);
    provide("actionLog", actionLog);
    provide("floatWindowContent", floatWindowContent);
    provide("cardUsedOwner", cardUsedOwner);
    provide("deliverCardOwner", deliverCardOwner);

    store.state.wss.onmessage = wssOnMsg;
    return {
      username, roomId, playerList, gameRoundisShow: roomIsShow, pos, players
    };
  },
  methods: {
    async joinRoom() {
      store.state.wss.send(JSON.stringify(
          {
            "event": "join_room",
            "roomid": this.roomId,
            "username": this.username,
          }
      ));
      this.playerList = [this.username];
    },
    gameStart() {
      store.state.wss.send(JSON.stringify(
          {
            "event": "game_start",
          }
      ));
    },
    changeHand() {
      let myStatus = this.players.arr[this.pos - 1];
      myStatus.hand_card = [1, 2, 3, 4, 6];
      console.log("myStatus", myStatus);
    },
    blueChange() {
      this.players.arr[1].blue.push(1);
      console.log(this.players.arr[1].blue);
    }

  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#gameroom {
  user-select: none;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
