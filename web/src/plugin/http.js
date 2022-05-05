// let Url = "http://127.0.0.1:8000/api/";
// let Wss = "ws://127.0.0.1:8000/wss/multiplayer/";
let Url = "http://192.168.163.151:8000/api/";
let Wss = "ws://192.168.163.151:8000/wss/multiplayer/";
// let Url = "http://101.43.39.245:8001/api/";
// let Wss = "ws://101.43.39.245:8001/wss/multiplayer/";

import axios from "axios";

const apiReq = axios.create({
    baseURL: Url, withCredentials: true,
});

export {apiReq, Wss};