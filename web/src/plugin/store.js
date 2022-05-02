import {reactive} from "vue";
import {Wss} from "@/plugin/http";

const store = {
    state: reactive(
        {
            wss: undefined,
            handCardSeletIdx: -1
        }
    ),
    setHandCardSeletId(idx) {
        this.state.handCardSeletIdx = idx;
    }
};

store.state.wss = new WebSocket(Wss);

export {store};