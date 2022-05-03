import {reactive} from "vue";
import {Wss} from "@/plugin/http";

const store = {
    state: reactive(
        {
            wss: new WebSocket(Wss),
            handCardSeletIdx: -1
        }
    ),
    setHandCardSeletId(idx) {
        this.state.handCardSeletIdx = idx;
    }
};

export {store};