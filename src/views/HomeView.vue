<template>
  <div class="search-input">
    <el-input
      class="el-input"
      v-model="input"
      style="width: 240px"
      placeholder="请输入关键词"
    />
    <el-button type="primary" :icon="Search" circle @click="a()" />
    <el-button type="primary" :icon="Search" circle @click="b()" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Search } from "@element-plus/icons-vue";
const input = ref("");
import { openPath } from "@tauri-apps/plugin-opener";
import axios from "axios";

onMounted(async () => {
  console.log("111");
});

const a = async () => {
  // await openPath("../../public/rust.exe");
  axios
    .post("/api/get_all", {
      table_name: "knowledge_base",
    })
    .then((res) => {
      console.log("res", res.data);
    });
};
const b = async () => {
  // await openPath("../../public/rust.exe");
  axios
    .post("/api/add_knowledge_base", {
      name: "1",
      description: "1",
      encoding_model: "1",
      is_multimodal: "1",
      bind_path: "1",
    })
    .then((res) => {
      console.log("res", res.data);
    });
};
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

.el-button.is-circle {
  border-radius: 0 200px 200px 0 !important;
  height: 52px;
  width: 50px;
}
</style>
