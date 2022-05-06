<template>
  <div class="action-log">
    <ul style="list-style-type: none;">
      <li v-for="(item, i) in actionLog" :key="i">{{ item }}</li>
    </ul>
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
.action-log {
  font-size: 2vh;
}
</style>