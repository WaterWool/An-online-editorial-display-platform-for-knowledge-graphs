<template>
  <div class="app">
    <Editor v-model="jsonData" :config="Config"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Editor } from './packages/editor';
import { Config } from './config' ;
import jsonData from './data2.json'

export default defineComponent({
  name: 'App',
  components: {
    Editor,
  },
  data() {
    return {
      Config,
      jsonData,
    }
  }
});
</script>

<style lang="scss">
  html, body{
    margin: 0;
    padding: 0;
  }
</style>
