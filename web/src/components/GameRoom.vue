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
  <GameGround v-else :players="players"></GameGround>
  <button @click="changeHand">改变手牌</button>

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
    let actionLog = reactive({arr: ["进入房间"]});
    let players = reactive({arr: []});
    let selectCardId = ref(-1);
    let cardUsedId = ref(-1);
    let selectUsername = ref("");

    const updateSelectCardId = (newId) => {
      selectCardId.value = newId;
    };


    if (username == null) {
      alert("请先登陆");
      router.push("/login");
    }

    function wssOnMsg(e) {
      let data = JSON.parse(e.data);
      let event = data.event;
      console.log(data);
      if (data.username === username) return false;
      if (event === "create_player") {  //添加用户进入房间
        playerList.value.push(data.username);
      } else if (event === "recover_game") { //用户恢复房间状态
        let players = data.players;
        for (let i = 0; i < players.length; ++i) {
          if (players[i].username === username) continue;
          playerList.value.push(players[i].username);
        }
      } else if (event === "delete_player") { //用户退出房间
        for (let i = 0; i < playerList.value.length; i++)
          if (playerList.value[i] === data.username) playerList.value.splice(i, 1);
      } else if (event === "game_status") {  //对局开始
        roomIsShow.value = false;
        players.arr = data.data;
        playerNum.value = data.data.length;
        for (let i = 0; i < data.data.length; i++) {
          if (data.data[i].username === username) {
            pos.value = data.data[i].pos;
          }
        }

      }
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

    store.state.wss.onmessage = wssOnMsg;
    return {
      username, roomId, playerList, gameRoundisShow: roomIsShow, pos, players
    };
  },
  methods: {
    async joinRoom() {
      store.state.wss.send(JSON.stringify(
          {
            "event": "joinroom",
            "roomid": this.roomId,
            "username": this.username,
          }
      ));
      this.playerList = [this.username];
    },
    gameStart() {
      store.state.wss.send(JSON.stringify(
          {
            "event": "gamestart",
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
