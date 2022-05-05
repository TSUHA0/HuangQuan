<template>
  <div>
    <div id="focus_toolTip" class="special_focus_toolTip">
      <div style='font-size:12px;color: #fec443;font-weight: bold;font-family: MicrosoftYaHei;'>
        {{ floatWindowContent }}
      </div>
    </div>
    <div class="hand-card" :style=" 'position: absolute; left:' +
      (this.basePos + (this.idx + 1) * (this.handCard.length > 13 ? (75 / this.handCard.length) : 6))
      + 'vw;' + this.bottom "
         @click="sendSelectIdxback">
      <img :src="test" style="height: 100%;width: 100%"
           @mousemove="itemMousemove($event)"
           @mouseover="itemMouseover"
           @mouseout="itemMouseout">
    </div>

  </div>
</template>

<script>
import {inject, toRefs} from "vue";
import $ from "jquery";

export default {
  name: "HandCard",
  setup(props, {emit}) {
    let test = require("@/assets/test.png");
    let basePos = 4;
    const players = inject("players");
    const pos = inject("pos");
    const floatWindowContent = inject("floatWindowContent");
    let myStatus = toRefs(players.arr[pos.value - 1]);
    const handCard = myStatus.hand_card;
    let t = Function;

    function sendSelectIdxback() {
      emit("selectback", props.cardId);
    }

    return {
      test,
      basePos,
      sendSelectIdxback,
      handCard,
      floatWindowContent,
      t
    };
  },
  props: {
    idx: Number,
    cardId: Number,
    bottom: String
  },
  methods: {
    itemMouseover: function () {
      var focusTooltip = $("#focus_toolTip");
      this.t = setTimeout(function () {
        focusTooltip.css("display", "block");
      }, 1500);
      this.floatWindowContent = "选中手牌" + this.cardId;
    },
    itemMouseout: function () {
      var focusTooltip = $("#focus_toolTip");
      clearTimeout(this.t);
      focusTooltip.css("display", "none");
    },
    itemMousemove: function (e) {
      let focusTooltip = $("#focus_toolTip");
      focusTooltip.css("bottom", parseInt(100 - e.clientY / window.innerHeight * 100) + "vh");
      focusTooltip.css("left", parseInt(e.clientX / window.innerWidth * 100 + 2) + "vw");
    },
  }
};
</script>

<style scoped>

</style>