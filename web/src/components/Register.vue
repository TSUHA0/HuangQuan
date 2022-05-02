<template>
  <div>
    <span>账号：</span>
    <input v-model="username"/>
    <br>
    <span>密码：</span>
    <input type="password" v-model="password"/>
    <br>
    <span>再次输入密码：</span>
    <input type="password" v-model="password_confirm"/>
    <div style="padding-top:20px;">
      <span style="padding-right:3vh;" @click="register"><button>注册</button></span>
      <span @click="this.$router.push('/login')"><button>返回登陆界面</button></span>
    </div>
  </div>

</template>

<script>
import {apiReq} from "@/plugin/http";
import qs from "qs";

export default {
  name: "register",
  props: {
    msg: String
  },
  data() {
    return {
      username: "",
      password: "",
      password_confirm: "",
    };
  },
  methods: {
    register() {
      let data = qs.stringify({
        username: this.username,
        password: this.password,
        password_confirm: this.password_confirm
      });
      apiReq.post("register/", data).then((res) => {
            console.log(res);
            if (res.data.result == "success") {
              alert("注册成功，即将返回主页");
              this.$router.push("/login");
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

</style>
