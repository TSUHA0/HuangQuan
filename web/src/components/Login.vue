<template>
  <div id="login">
    <span>账号：</span>
    <input v-model="username"/>
    <br>
    <span>密码：</span>
    <input type="password" v-model="password"/>
    <div style="padding-top:20px;">
      <span style="padding-right:3vh;" @click="login"><button>登陆</button></span>
      <span style="padding-right:3vh;" @click="$router.push('/register')"><button>注册</button></span>
      <span><button @click="getLoginStatus">状态</button></span>
    </div>
  </div>

</template>

<script>
import {apiReq} from "@/plugin/http";
import qs from "qs";

export default {
  name: "login",
  props: {
    msg: String
  },
  data() {
    return {
      username: "",
      password: "",
      ServMsg: "",
    };
  },
  methods: {
    login() {
      let data = qs.stringify({
        username: this.username,
        password: this.password,
      });
      apiReq.post("login/", data).then((res) => {
            if (res.data.result == "success") {
              window.sessionStorage.setItem("username", this.username);
              this.$router.push("/");
            } else {
              alert(res.data.result);
            }
          }
      );
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
#login {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
