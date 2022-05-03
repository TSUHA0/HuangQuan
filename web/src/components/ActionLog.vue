<template>
  <div class="action-log">
    <ol>
      <li v-for="(item, i) in actLogArr" :key="i">{{ item }}</li>
    </ol>
  </div>
</template>

<script>
import {inject, toRefs} from "vue";

export default {
  name: "ActionLog",
  setup() {
    const actionLog = inject("actionLog");
    let actLogArr = toRefs(actionLog.arr);
    return {
      actLogArr
    };
  }
};
</script>

<style scoped>

</style>