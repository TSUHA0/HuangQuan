import {reactive} from "vue";

const store = {
    state: reactive(
        {
            handCardSeletIdx: -1
        }
    ),
    setHandCardSeletId(idx) {
        this.state.handCardSeletIdx = idx;
    }

};

export {store};