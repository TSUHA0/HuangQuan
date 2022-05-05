<template>
  <div class="hello">
    <div id="focus_toolTip" class="special_focus_toolTip" v-html="toolTopbody"></div>
    <button
        class="buttonStyle"
        @mousemove="itemMousemove($event)"
        @mouseover="itemMouseover"
        @mouseout="itemMouseout"
    >悬浮框测试
    </button>
  </div>
</template>
<script>
import $ from "jquery";

export default {
  name: "FloatWindow",
  data() {
    return {
      toolTopbody: ""
    };
  },
  methods: {
    itemMouseover: function () {
      var focusTooltip = $("#focus_toolTip");
      focusTooltip.css("display", "block");
    },

    itemMouseout: function () {
      var focusTooltip = $("#focus_toolTip");
      focusTooltip.css("display", "none");
    },

    itemMousemove: function (e) {
      var self = this;
      var focusTooltip = $("#focus_toolTip");
      focusTooltip.css("top", e.clientY - 8 + "px");
      focusTooltip.css("left", e.clientX + 10 + "px");
      var headerHtml =
          "<div style='font-size:12px;color: #fec443;font-weight: bold;font-family: MicrosoftYaHei;'>" +
          "我的悬浮框参考：" +
          "</div>";
      var effectHtml =
          "<div style='font-size:12px;margin-top:5px;'>" + "</div>";
      self.toolTopbody = headerHtml + effectHtml;
    }
  }
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.buttonStyle {
  margin-left: 150px;
}

.special_focus_toolTip {
  z-index: 7;
  position: absolute;
  display: none;
  width: 400px;
  height: 130px;
  border-style: solid;
  transition: left 0.4s cubic-bezier(0.23, 1, 0.32, 1),
  top 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  background-color: rgba(50, 50, 50, 0.701961);
  border-width: 0px;
  border-color: #333333;
  border-radius: 4px;
  color: #ffffff;
  font-style: normal;
  font-variant: normal;
  font-weight: normal;
  font-stretch: normal;
  font-size: 14px;
  font-family: "Microsoft YaHei";
  line-height: 21px;
  padding: 10px 10px;
}
</style>