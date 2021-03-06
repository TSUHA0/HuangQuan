import {createApp} from "vue";
import VueCookies from "vue-cookies";
import App from "./App.vue";
import router from "@/router/router";
import "./assets/css/style.css";
import "@/plugin/secretcard";
import "@/plugin/front";


// 5. 创建并挂载根实例
const app = createApp(App);
//确保 _use_ 路由实例使
//整个应用支持路由。
app.use(router);
app.use(VueCookies);
app.mount("#app");

