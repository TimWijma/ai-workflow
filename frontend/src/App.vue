<template>
  <div id="app">
    <FlowEditor />
  </div>
</template>

<script setup lang="ts">
import FlowEditor from './components/FlowEditor.vue'
</script>

<style scoped>
#app {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}
</style>
