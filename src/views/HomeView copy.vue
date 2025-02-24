<template>
  <el-button-group>
    <el-button type="primary" @click="callAdd()">测试按钮</el-button>s
    <el-button type="primary" @click="initTable()">初始化表</el-button>
    <el-button type="primary" @click="insertData()">添加数据</el-button>
    <el-button type="primary" @click="deleteData()">删除数据</el-button>
    <el-button type="primary" @click="updateData()">修改数据</el-button>
    <el-button type="primary" @click="queryData()">查询数据</el-button>
  </el-button-group>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
    <el-form-item label="id:">
      <el-input v-model="formInline.userId" placeholder="" clearable />
    </el-form-item>
    <el-form-item label="name:">
      <el-input v-model="formInline.name" placeholder="" clearable />
    </el-form-item>
  </el-form>
  <div>{{ tableData }}</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import Database from "@tauri-apps/plugin-sql";

// import { invoke } from "@tauri-apps/api";
import { invoke } from "@tauri-apps/api/core";

const formInline = ref({
  userId: null,
  name: "",
});

const tableData = ref();
onMounted(async () => {
  // tableData.value = await queryAuth();
});

const result = ref();
// 调用加法
const callAdd = async () => {
  console.log("?", invoke);
  // invoke('call_python_function');
  invoke('my_custom_command');
  // try {
  //   const response: any = await invoke("call_python_function", {
  //     input: { function: "add", args: [3, 5] },
  //   });
  //   result.value = response.result; // 8
  // } catch (error) {
  //   console.error("调用失败:", error);
  //   result.value = "错误: " + error;
  // }
};

// const test = async () => {
//   try {
//     const command = await exec("_create_tables", [
//       "../../python/rust.py",
//     ]);
//     console.log(command.stdout); // 获取 Python 输出
//   } catch (error) {
//     console.error("Error:", error);
//   }
// };
//
const insertData = async () => {
  console.log("增");
  await insertAuth(formInline.value.userId, formInline.value.name);
  await queryData();
};
const deleteData = async () => {
  console.log("删");
  await deleteAuth(formInline.value.userId);
  await queryData();
};
const updateData = async () => {
  console.log("改");
  await updateAuth(formInline.value.userId, formInline.value.name);
  await queryData();
};
const queryData = async () => {
  console.log("查");
  tableData.value = await queryAuth();
};

// 创建表
async function initTable() {
  const db = await initDb();
  await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);");
}
// 初始化数据库连接
async function initDb() {
  // sqlite数据库，路径相对于tauri::api::path::BaseDirectory::App
  const db = await Database.load("sqlite:test.db");
  return db;
}

// 插入数据
async function insertAuth(id: number, name: string) {
  const db = await initDb();
  await db.execute("INSERT into users (id, name) VALUES ($1, $2)", [id, name]);
}

// 更新数据
async function updateAuth(id: number, name: string) {
  const db = await initDb();
  await db.execute("UPDATE users SET name = $2 WHERE id = $1", [id, name]);
}

// 删除数据
async function deleteAuth(id: number) {
  const db = await initDb();
  await db.execute("DELETE FROM users WHERE id = $1", [id]);
}

// 查询数据
async function queryAuth() {
  const db = await initDb();
  return await db.select("SELECT * FROM users");
}
</script>

<style scoped>
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}
</style>
