<template>
  <div class="search-input">
    <el-input
      class="el-input"
      v-model="input"
      style="width: 240px"
      placeholder="请输入关键词"
    />
    <el-button type="primary" :icon="Search" circle />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Search } from "@element-plus/icons-vue";
const input = ref("");
</script>

<style scoped>
.search-input {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

:deep .el-input__wrapper {
  border-radius: 200px 0 0 200px !important;
  height: 50px;
}

.el-button.is-circle{
  border-radius:  0 200px 200px 0 !important;
  height: 52px;
  width: 50px;
}
</style>
