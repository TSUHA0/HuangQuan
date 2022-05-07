import {createRouter, createWebHashHistory} from "vue-router";


const routes = [{
    path: "/gameround", name: "game", component: () => import("../components/GameGround"),
}, {
    path: "/login", name: "login", component: () => import("../components/Login")
}, {
    path: "/register", name: "register", component: () => import("../components/Register")
}, {
    path: "/", name: "gameroom", component: () => import("../components/GameRoom")
}, {
    path: "/test", name: "test", component: () => import("@/components/About")
},];

const router = createRouter({
    history: createWebHashHistory(), routes, // `routes: routes` 的缩写
});

router.beforeEach((to, from, next) => {
    if (window.sessionStorage.getItem("username") || to.path === "/login" || to.path === "/register") next();
    else {
        alert("请先登陆");
        next("/login");
    }
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