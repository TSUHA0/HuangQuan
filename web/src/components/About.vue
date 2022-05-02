<template>
  <div>
    <input v-model="inMsg"/>
    <span>{{ inMsg }}</span>
    <br>
    <button @click="storeTestMsg">保存</button>
    <button @click="sendMsg">发送</button>
    <ul>
      <li v-for="(msg, i) in msgs" :key="i">
        {{ msg }}
      </li>
    </ul>
  </div>
</template>

<script>
import {Wss} from "@/plugin/http";
import {ref} from "vue";

export default {
  name: "About",
  setup() {
    let msgs = ["first"];
    let inMsg = ref("");
    let ws = new WebSocket(Wss + "wss/multiplayer/");

    function sendMsg() {
      ws.send(inMsg);
    }

    let ses = window.sessionStorage;

    function storeTestMsg() {
      ses.setItem(
          "testmsg", inMsg.value
      );
    }

    return {
      msgs,
      inMsg,
      sendMsg,
      storeTestMsg
    };
  }
};
</script>

<style scoped>

</style>