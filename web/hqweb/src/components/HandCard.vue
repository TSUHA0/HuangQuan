<template>
  <div class="hand-card" :style="cardStyle + bottom" @click="sendSelectIdxback">
    手牌
  </div>
</template>

<script>

let basePos = 4;
export default {
  setup(props, {emit}) {
    function sendSelectIdxback() {
      emit("selectback", props.cardId);
    }

    return {
      sendSelectIdxback
    };
  },
  props: {
    cardId: Number,
    num: Number,
    isSelect: Boolean,
    bottom: String
  },
  name: "HandCard",
  data() {
    return {
      // 牌过多时，将牌进行重叠处理，后期待完善
      cardStyle: "position: absolute; left:" + (basePos + (this.cardId) * (this.num > 2 ? 6 : 8)) + "vw;",
      // cardBottom: "bottom: 0;",
    };
  },
  methods: {},
};
</script>

<style scoped>

</style>