<template>
  <div class="action-log">
    <ol>
      <li v-for="(item, i) in actionLog" :key="i">{{ item }}</li>
    </ol>
  </div>
</template>

<script>
import {inject} from "vue";

export default {
  name: "ActionLog",
  setup() {
    const actionLog = inject("actionLog");
    return {
      actionLog
    };
  }
};
</script>

<style scoped>

</style>