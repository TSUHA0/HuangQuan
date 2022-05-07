<template>
  <div class="hand-card">
    {{ cardUsedOwner }}使用牌
    <div id="focus_toolTip_used_card" class="special_focus_toolTip">
      <div style='color: #fec443;font-weight: bold;font-family: MicrosoftYaHei;'>
        {{ floatWindowContent }}
      </div>
    </div>
    <div class="hand-card">
      <img :src="getImgUrl(cardUsedId)" style="height: 100%;width: 100%"
           @mousemove="itemMousemove"
           @mouseover="itemMouseover"
           @mouseout="itemMouseout">
    </div>
  </div>
</template>

<script>
import {inject, ref} from "vue";
import g_secretCard from "@/plugin/secretcard";
import $ from "jquery";

export default {
  name: "UsedCard",
  setup() {
    const cardUsedId = inject("cardUsedId");
    const cardUsedOwner = inject("cardUsedOwner");
    const floatWindowContent = inject("floatWindowContent");

    let cardContent = ref(g_secretCard[cardUsedId.value].content);
    let t = Function;

    return {
      floatWindowContent,
      t,
      cardContent,
      cardUsedId,
      cardUsedOwner
    };
  },
  methods: {
    getImgUrl: function (id) {
      let images = require.context("../assets/images/card/", false, /\.png$/);
      return images("./" + g_secretCard[id].imgtag + ".png");
    },
    itemMouseover: function () {
      var focusTooltip = $("#focus_toolTip_used_card");
      this.t = setTimeout(function () {
        focusTooltip.css("display", "block");
      }, 1500);
      this.floatWindowContent = this.cardContent;
    },
    itemMouseout: function () {
      var focusTooltip = $("#focus_toolTip_used_card");
      clearTimeout(this.t);
      focusTooltip.css("display", "none");
    },
    itemMousemove: function () {
      let focusTooltip = $("#focus_toolTip_used_card");
      focusTooltip.css("top", 22 + "vh");
      focusTooltip.css("left", -5 + "vw");
    },
  }
};
</script>

<style scoped>
</style>