<template>
  <div style="position: absolute; top: 32vh;left: 12vw; width: 50vw;height: 60vh;border-style: inset;
      background: white">
    密函信息
    <button style="position: relative;left: 39vw"
            @click="receiveInfoHide">关闭界面
    </button>
    <button style="position: relative;"
            @click="dropReceive">弃置密函
    </button>
    <button style="position: relative;"
            @click="receiveTohand">收到手牌
    </button>
    <button style="position: relative;"
            @click="receiveToReceive">转移自身
    </button>

    <div style="position: relative;left: 40vw;top:7vw;width: 7vw">
      <span>输入卡牌代号</span>
      <input style="width: 4vw" v-model="tagId"/>
      <br>
      你输入的卡牌代号为{{ tagId }}
    </div>
    <div>蓝色密函：</div>
    <div v-for="(item,i) in blue" :key="i" class="recieve-class">
      {{ item }},{{ g_secretCard[item].imgtag }}
    </div>
    <br><br>
    <div>红色密函：</div>
    <div v-for="(item,i) in red" :key="i" class="recieve-class">
      {{ item }},{{ g_secretCard[item].imgtag }}
    </div>
    <br><br>
    <div>黑色密函：</div>
    <div v-for="(item,i) in gray" :key="i" class="recieve-class">
      {{ item }},{{ g_secretCard[item].imgtag }}
    </div>
  </div>
</template>

<script>
import {inject, ref} from "vue";
import g_secretCard from "@/plugin/secretcard";
import {store} from "@/plugin/store";

export default {
  name: "ReceiveInfo",
  setup() {
    const receiveInfoIsShow = inject("receiveInfoIsShow");
    const recInfoArr = inject("recInfoArr");
    const selectUsername = inject("selectUsername");
    let tagId = ref(0);

    return {
      g_secretCard,
      ...recInfoArr,
      receiveInfoIsShow,
      tagId,
      selectUsername
    };
  },
  methods: {
    receiveToReceive() {
      if (parseInt(this.tagId) > g_secretCard.length - 1) {
        alert("卡牌ID非法");
        return;
      }
      let name = g_secretCard[this.tagId].imgtag;
      if (!name) return;
      let update_msg = window.sessionStorage.getItem("username") + "将" + this.selectUsername + "的密函：" + name + "转移到自己身上";
      store.state.wss.send(JSON.stringify(
          {
            "event": "receive_to_receive",
            "update_msg": update_msg,
            "username": window.sessionStorage.getItem("username"),
            "target": this.selectUsername,
            "cardid": this.tagId,
          }
      ));
    },
    receiveTohand() {
      if (parseInt(this.tagId) > g_secretCard.length - 1) {
        alert("卡牌ID非法");
        return;
      }
      let name = g_secretCard[this.tagId].imgtag;
      if (!name) return;
      let update_msg = window.sessionStorage.getItem("username") + "将" + this.selectUsername + "的密函：" + name + "收到了手牌中";
      store.state.wss.send(JSON.stringify(
          {
            "event": "receive_to_hand",
            "update_msg": update_msg,
            "username": window.sessionStorage.getItem("username"),
            "target": this.selectUsername,
            "cardid": this.tagId,
          }
      ));
    },
    dropReceive() {
      if (parseInt(this.tagId) > g_secretCard.length - 1) {
        alert("卡牌ID非法");
        return;
      }
      let name = g_secretCard[this.tagId].imgtag;
      if (!name) return;
      let update_msg = window.sessionStorage.getItem("username") + "弃置了" + this.selectUsername + "的密函：" + name;
      store.state.wss.send(JSON.stringify(
          {
            "event": "drop_receive",
            "update_msg": update_msg,
            "target": this.selectUsername,
            "cardid": this.tagId,
          }
      ));
    },
    receiveInfoHide() {
      this.receiveInfoIsShow = false;
    },
  }
};
</script>

<style scoped>
.recieve-class {
  width: 8vw;
  border-style: inset;
  float: left;
  margin-right: 1vw;
  font-size: 2vh;
}


</style>