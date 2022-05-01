import {createRouter, createWebHashHistory} from "vue-router";
import Home from "../components/GameGround";
import login from "../components/Login";
import About from "@/components/About";

const routes = [
    {path: "/", component: Home},
    {path: "/login", component: login},
    {path: "/test", component: About},
];

const router = createRouter({
    history: createWebHashHistory(),
    routes, // `routes: routes` 的缩写
});

// router.beforeEach((to, from, next) => {
//   // to and from are both route objects. must call `next`.
//   if (to.path == '/') {
//     next('/login')
//   }
//   if (to.path == '/login') {
//     return next()
//   }
// })

export default router;