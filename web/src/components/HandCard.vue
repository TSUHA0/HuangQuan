<template>
  <div>
    <div id="focus_toolTip" class="special_focus_toolTip">
      <div style='color: #fec443;font-weight: bold;font-family: MicrosoftYaHei;'>
        {{ floatWindowContent }}
      </div>
    </div>
    <div class="hand-card" :style=" 'position: absolute; left:' +
      (this.basePos + (this.idx) * (this.handCard.length > 8 ? (70 / this.handCard.length) : 8))
      + 'vw;' + this.bottom "
         @click="sendSelectIdxback">
      <img :src="getImgUrl(cardId)" style="height: 100%;width: 100%"
           @mousemove="itemMousemove($event)"
           @mouseover="itemMouseover"
           @mouseout="itemMouseout">
    </div>

  </div>
</template>

<script>
import {inject, ref, toRefs} from "vue";
import $ from "jquery";
import g_secretCard from "@/plugin/secretcard";

export default {
  name: "HandCard",
  setup(props, {emit}) {
    let cardContent = ref(g_secretCard[props.cardId].content);

    let basePos = 5;
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
      basePos,
      sendSelectIdxback,
      handCard,
      floatWindowContent,
      t,
      cardContent
    };
  },
  props: {
    idx: Number,
    cardId: Number,
    bottom: String
  },
  methods: {
    getImgUrl(id) {
      let images = require.context("../assets/images/card/", false, /\.png$/);
      return images("./" + g_secretCard[id].imgtag + ".png");
    },
    itemMouseover: function () {
      var focusTooltip = $("#focus_toolTip");
      this.t = setTimeout(function () {
        focusTooltip.css("display", "block");
      }, 1500);
      this.floatWindowContent = this.cardContent;
    },
    itemMouseout: function () {
      var focusTooltip = $("#focus_toolTip");
      clearTimeout(this.t);
      focusTooltip.css("display", "none");
    },
    itemMousemove: function (e) {
      let focusTooltip = $("#focus_toolTip");
      focusTooltip.css("bottom", parseInt(100 - e.clientY / window.innerHeight * 100) + "vh");
      let x = parseInt(e.clientX / window.innerWidth * 100 + 2);
      if (x > 78) {
        focusTooltip.css("left", "78vw");
      } else {
        focusTooltip.css("left", x + "vw");
      }
    },
  }
};
</script>

<style scoped>

</style>