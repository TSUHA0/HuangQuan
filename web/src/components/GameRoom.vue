<template>
  <button @click="blueChange">asd</button>
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
import {useRouter} from "vue-router";

export default {
  name: "login",
  components: {
    GameGround
  },
  setup() {
    let roomIsShow = ref(true);
    const router = useRouter();
    let playerList = ref([""]);
    let username = window.sessionStorage.getItem("username");
    let roomId = 0;
    let pos = ref(0);
    let playerNum = ref(0);
    let actionLog = ref(["进入房间"]);
    let players = reactive({arr: []});
    let selectCardId = ref(-1);
    let cardUsedId = ref(-1);
    let selectUsername = ref("");
    let floatWindowContent = ref("");

    const updateSelectCardId = (newId) => {
      selectCardId.value = newId;
    };


    if (username == null) {
      alert("请先登陆");
      router.push("/login");
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
      actionLog.value.push(data.username + "抽了" + card_list.length + "张牌");
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
