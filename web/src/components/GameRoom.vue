<template>
  <div id="gameroom">
    <span>房间号：</span>
    <input v-model="roomId"/>
    <div style="padding-top:20px;">
      <span style="padding-right:3vh;" @click="joinRoom"><button>加入房间</button></span>
      <span style="padding-right:3vh;" @click="joinRoom"><button>开始游戏</button></span>
      <br><br><br>

      <ul style="user-select: none; margin: auto; list-style-type: none;">
        <li v-for="(item, i) in playerList" :key="i"> {{ item }}</li>
      </ul>
    </div>
  </div>

</template>

<script>
import {apiReq} from "@/plugin/http";
import {store} from "@/plugin/store";
import {ref} from "vue";
import {useRouter} from "vue-router";

export default {
  name: "login",
  props: {
    msg: String
  },
  setup() {
    const router = useRouter();
    let playerList = ref(["1"]);
    let username = window.sessionStorage.getItem("username");
    let roomId = 0;
    if (username == null) {
      alert("请先登陆");
      router.push("/login");
    }

    function wssOnMsg(e) {
      let data = JSON.parse(e.data);
      let event = data.event;
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
          if (playerList.value[i] == data.username) playerList.value.splice(i, 1);
      }

    }

    store.state.wss.onmessage = wssOnMsg;

    return {
      username, roomId, playerList
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
    getLoginStatus() {
      apiReq.get("getinfo/").then((res) => {
            console.log(res);
          }
      );
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
