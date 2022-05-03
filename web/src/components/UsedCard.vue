<template>
  <div class="hand-card">
    使用牌{{ cardUsedId }}
  </div>
</template>

<script>

import {inject} from "vue";

export default {
  setup() {
    const cardUsedId = inject("cardUsedId");

    return {
      cardUsedId
    };
  },
  name: "UsedCard",
};
</script>

<style scoped>

</style>