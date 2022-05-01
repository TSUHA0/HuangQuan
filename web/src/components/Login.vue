<template>
  <div id="app">
    <h1>{{ msg }}</h1>
    <a @click="getMsg">click me!!!</a>
    <br>
    <a :data="ServMsg">Server Msg is {{ ServMsg }}</a>
    <br>
    <span>账号：</span>
    <input v-model="username"/>
    <br>
    <span>密码：</span>
    <input type="password" v-model="password"/>
    <div style="padding-top:20px;">
      <span style="padding-right:3vh;"><button>登陆</button></span>
      <span><button>注册</button></span>
    </div>

    <p>
      <!--使用 router-link 组件进行导航 -->
      <!--通过传递 `to` 来指定链接 -->
      <!--`<router-link>` 将呈现一个带有正确 `href` 属性的 `<a>` 标签-->
      <router-link to="/">Go to Home</router-link>
      <router-link to="/login">Go to Logint</router-link>
    </p>
    <!-- 路由出口 -->
    <!-- 路由匹配到的组件将渲染在这里 -->
    <router-view></router-view>
  </div>

</template>

<script>
import axios from 'axios'
import {Url} from "@/plugin/http"

export default {
  name: 'login',
  props: {
    msg: String
  },
  data() {
    return {
      username: '',
      password: '',
      ServMsg: '',
    }
  },
  methods: {
    getMsg() {
      axios.get(Url + 'login')
          .then((res) => {
                console.log(res.data.msg)
                this.ServMsg = res.data.msg
              }
          )
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

a {
  color: #42b983;
}
</style>
