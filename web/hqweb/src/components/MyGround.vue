<template>
  <div>
    <div class="my-ground-information-blue">
      王道密函
    </div>
    <div class="my-ground-information-red">
      霸道密函
    </div>
    <div class="my-ground-information-gray">
      黑密函
    </div>
    <HandCard v-for="(item,i) in handcardArr" :key="i" :cardId="item.cardId"
              :num="handcardArr.length" :bottom="item.cardId == selectCardId ? bt6 : bt0"
              :isSelect="item.isSelect" @selectback="getSelectback">
    </HandCard>

  </div>
</template>

<script>
import HandCard from "@/components/HandCard";
import {inject} from "vue";

export default {
  name: "MyGround",
  components: {HandCard},
  setup() {
    const updateSelectCardId = inject("updateSelectCardId");
    const selectCardId = inject("selectCardId");
    return {
      selectCardId,
      updateSelectCardId
    };
  },
  props: {
    handcardArr: Array,
  },
  data() {
    return {
      bt0: "bottom:0vh;",
      bt6: "bottom:6vh;"
    };
  },
  methods: {
    getSelectback(cardId) {
      console.log(this.selectCardId);
      for (var i = 0; i < this.handcardArr.length; i++) {
        var item = this.handcardArr[i];
        if (item.cardId == cardId) {
          if (this.selectCardId === -1) {
            this.updateSelectCardId(item.cardId);
          } else {
            this.updateSelectCardId(-1);
          }
          item.isSelect = !item.isSelect;
        } else {
          item.isSelect = false;
        }
      }
    },
  },
};
</script>

<style scoped>

</style>