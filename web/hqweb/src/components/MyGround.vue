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
    <HandCard v-for="(item,i) in handcardArr" :key="i" :cardId="item"
              :num="handcardArr.length" :bottom="item == selectCardId ? bt6 : bt0"
              @selectback="getSelectback">
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
      for (var i = 0; i < this.handcardArr.length; i++) {
        var item = this.handcardArr[i];
        if (item == cardId) {
          if (this.selectCardId == cardId) {
            this.updateSelectCardId(-1);
          } else {
            this.updateSelectCardId(item);
          }
        }
      }
    },
  },
};
</script>

<style scoped>

</style>