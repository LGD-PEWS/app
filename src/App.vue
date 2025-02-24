<template>
  <div class="common-layout">
    <el-container>
      <el-container>
        <el-aside width="150px">
          <el-menu
            default-active="HomeView"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
            :router="true"
          >
            <el-menu-item index="HomeView">
              <el-icon><icon-menu /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="KnowledgeBase">
              <el-icon><icon-menu /></el-icon>
              <span>知识库</span>
            </el-menu-item>
            <el-menu-item index="Setting" disabled>
              <el-icon><setting /></el-icon>
              <span>设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main><RouterView /></el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";

import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from "@element-plus/icons-vue";
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style scoped>
.el-aside {
  background-color: white;
}
.el-main {
  padding: 0;
  width: calc(100vw - 150px);
  height: calc(100vh);
}
.el-menu {
  height: calc(100vh);
}
</style>
