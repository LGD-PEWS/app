<template>
  <div>
    <div class="btn-group">
      <el-button type="primary">新增库</el-button>
    </div>
    <div class="card-group">
      <el-card
        class="card-class"
        shadow="hover"
        v-for="(item, index) in KnowledgeBases"
        :key="index"
      >
        <div>库{{ index }}</div>
        <div>详细信息</div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const KnowledgeBases = ref([{}, {}, {}]);
</script>

<style scoped>
.btn-group {
  margin: 10px 10px 5px 5px;
  width: calc(100vw - 150px - 15px);
}
.card-group {
  display: flex;
  flex-wrap: wrap;
}
.card-class {
  width: calc((100vw - 150px) / 2 - 20px);
  margin: 7px;
}
</style>
