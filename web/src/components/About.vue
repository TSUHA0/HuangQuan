<template>
  <div>
    <input v-model="inMsg"/>
    <br>
    <!--    <button @click="connWss">连接</button>-->
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

export default {
  name: "About",
  setup() {
    let msgs = ["first"];
    let inMsg = "";
    let ws = new WebSocket(Wss + "wss/multiplayer/");

    function sendMsg() {
      ws.send(inMsg);
    }

    return {
      msgs,
      inMsg,
      sendMsg,
    };
  }
};
</script>

<style scoped>

</style>