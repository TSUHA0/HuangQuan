import {reactive} from "vue";

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

export {store};