<template>
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
import g_secretCard from "@/plugin/secretcard";

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
    let deliverStatus = reactive({
      deliverCardId: 0,
      deliverCardOwner: "",
      deliverVisual: false,
    });

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
      for (let i = 0; i < data.data.length; i++) {
        if (data.data[i].username === username)
          pos.value = data.data[i].pos;
        console.log("data.data[i].deliver", i, data.data[i].deliver);
        if (data.data[i].deliver !== 0) {
          deliverStatus.deliverCardOwner = data.data[i].username;
          deliverStatus.deliverCardId = data.data[i].deliver;
        }
      }
    }

    function draw_card(data) {
      let card_list = data.card_list;
      updateActionLog(data.username + "抽了" + card_list.length + "张牌");

      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.username) {
          for (let j = 0; j < card_list.length; ++j) players.arr[i].hand_card.push(card_list[j]);
        }
      }
    }

    function accept_deliver(data) {
      updateActionLog(data.username + "接收了密函，颜色为" + data.color);
      deliverStatus.deliverCardOwner = "";
      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.username) {
          players.arr[i].blue = data.blue;
          players.arr[i].red = data.red;
          players.arr[i].gray = data.gray;
        }
      }
    }

    function play_card(data) {
      cardUsedId.value = data.cardid;
      cardUsedOwner.value = data.username;
      updateActionLog(data.update_msg);
    }

    function secret_play_card(data) {
      cardUsedOwner.value = data.username;
      if (data.target === window.sessionStorage.getItem("username")) {
        cardUsedId.value = data.cardid;
        updateActionLog(cardUsedOwner.value + "单独对" + data.target + "打出了" + g_secretCard[cardUsedId.value].name);
      } else {
        cardUsedId.value = 0;
        updateActionLog(cardUsedOwner.value + "单独对" + data.target + "打出了一张牌");
      }

    }

    function deliver_card(data) {
      deliverStatus.deliverCardOwner = data.username;
      deliverStatus.deliverCardId = data.cardid;
      updateActionLog(data.username + "开始传递密函");
    }

    function behind_come(data) {
      updateActionLog(data.username + "幕后登场！！");
      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.username) {
          players.arr[i].witch_status = "behind";
        }
      }
    }

    function hand_to_receive(data) {
      if (data.update_msg !== "") updateActionLog(data.update_msg);
      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.target) {
          players.arr[i].blue = data.blue;
          players.arr[i].red = data.red;
          players.arr[i].gray = data.gray;
        }
      }
    }

    function show_role_info(data) {
      if (data.username === window.sessionStorage.getItem("username")) {
        updateActionLog(data.target + "的道牌是" + data.role);
      } else {
        updateActionLog(data.username + "查看了" + data.target + "道牌");
      }
    }

    function hand_to_hand(data) {
      updateActionLog(data.update_msg);
      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.target) {
          players.arr[i].hand_card = data.target_card_list;
        } else if (players.arr[i].username === data.username) {
          players.arr[i].hand_card = data.me_card_list;
        }
      }
    }

    function hand_replace_deliver(data) {
      for (let i = 0; i < players.arr.length; i++) {
        if (deliverStatus.deliverCardOwner === players.arr[i].username) {
          players.arr[i].deliver = data.cardid;
          deliverStatus.deliverCardId = data.cardid;
          deliverStatus.deliverVisual = false;
          updateActionLog(data.update_msg);
        }
      }
    }

    function update_action_log(data) {
      updateActionLog(data.update_msg);
    }

    function reverse_deliver(data) {
      updateActionLog(data.update_msg);
      deliverStatus.deliverVisual = true;
    }

    function drop_receive(data) {
      updateActionLog(data.update_msg);
      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.target) {
          players.arr[i].blue = data.blue;
          players.arr[i].red = data.red;
          players.arr[i].gray = data.gray;
        }
      }
    }

    function receive_to_hand(data) {
      updateActionLog(data.update_msg);
      for (let i = 0; i < players.arr.length; i++) {
        if (players.arr[i].username === data.target) {
          players.arr[i].blue = data.blue;
          players.arr[i].red = data.red;
          players.arr[i].gray = data.gray;
        }
        if (players.arr[i].username === data.username) {
          players.arr[i].hand_card.push(data.cardid);
        }
      }
    }


    function wssOnMsg(e) {
      let data = JSON.parse(e.data);
      let event = data.event;
      console.log(data);
      if (data.status === "error") console.log(data.result);

      if (event === "draw_card") draw_card(data);  //玩家抽牌
      else if (event === "hand_to_receive") hand_to_receive(data);  //密函从手牌直接放置到接受区
      else if (event === "show_role_info") show_role_info(data);  //密函从手牌直接放置到接受区
      else if (event === "hand_to_hand") hand_to_hand(data);  //密函从手牌直接放置到接受区
      else if (event === "play_card") play_card(data);  //打出牌
      else if (event === "hand_replace_deliver") hand_replace_deliver(data);  //打出牌
      else if (event === "update_action_log") update_action_log(data);  //打出牌
      else if (event === "reverse_deliver") reverse_deliver(data);  //打出牌
      else if (event === "drop_receive") drop_receive(data);  //打出牌
      else if (event === "receive_to_hand") receive_to_hand(data);  //打出牌

      // 以下为需要忽略username为自身的event
      if (data.username === username) return false;
      if (event === "create_player") playerList.value.push(data.username);  //添加用户进入房间
      else if (event === "recover_game") recover_game(data); //用户恢复房间状态
      else if (event === "delete_player") delete_player(data); //用户退出房间
      else if (event === "game_status") game_start(data);  //对局开始
      else if (event === "deliver_card") deliver_card(data);  //对局开始
      else if (event === "accept_deliver") accept_deliver(data);  //接受密函
      else if (event === "secret_play_card") secret_play_card(data);  //指定打出
      else if (event === "behind_come") behind_come(data);  //幕后登场


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
    provide("deliverStatus", deliverStatus);
    provide("updateActionLog", updateActionLog);

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
