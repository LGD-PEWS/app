// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri_plugin_sql::{Builder, Migration, MigrationKind};

fn main() {
    let migrations = vec![
        // Define your migrations here
        Migration {
            version: 1,
            description: "create_initial_tables",
            sql: "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);",
            kind: MigrationKind::Up,
        },
    ];

    app_lib::run();
    tauri::Builder::default()
        .plugin(
            tauri_plugin_sql::Builder::default()
                .add_migrations("sqlite:test.db", migrations)
                .build(),
        )
        .invoke_handler(tauri::generate_handler![call_python_function])
        .invoke_handler(tauri::generate_handler![my_custom_command])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
    // tauri::Builder::default()
    //     .plugin(tauri_plugin_sql::Builder::default().build())
    //     .run(tauri::generate_context!())
    //     .expect("error while running tauri application");
}

use serde::{Deserialize, Serialize};
use std::process::Command;
use tauri::{command, Manager};

// 输入结构体：包含函数名和参数
#[derive(Serialize, Deserialize)]
struct PythonInput {
    function: String, // 函数名（如 "add"）
    args: Vec<i32>,   // 参数列表（如 [3, 5]）
}

// 输出结构体
#[derive(Serialize, Deserialize)]
struct PythonOutput {
    result: i32,
}

// 统一 Rust 命令处理所有 Python 函数调用
#[command]
async fn call_python_function(input: PythonInput) -> Result<PythonOutput, String> {
    println!("I was invoked from JS!");
    // 获取 Python 脚本路径
    let script_path = std::env::current_dir().unwrap().join("scripts/rust.py");

    // 序列化输入参数为 JSON 字符串
    let input_json = serde_json::to_string(&input).map_err(|e| e.to_string())?;

    // 执行 Python 脚本
    let output = Command::new("python3")
        .arg(script_path.to_str().unwrap())
        .arg(&input_json)
        .output()
        .map_err(|e| e.to_string())?;

    // 检查执行状态
    if !output.status.success() {
        let error_msg = String::from_utf8_lossy(&output.stderr);
        return Err(format!("Python脚本错误: {}", error_msg));
    }

    // 解析 Python 输出
    let output_str = String::from_utf8(output.stdout).map_err(|e| e.to_string())?;
    let result: PythonOutput = serde_json::from_str(&output_str).map_err(|e| e.to_string())?;

    Ok(result)
}

#[tauri::command]
fn my_custom_command() {
    println!("I was invoked from JS!");
}

// use tauri::path::BaseDirectory;
// src-tauri/src/main.rs
// #[tauri::command]
// fn get_app_dir() -> String {
//     tauri::path::resolve_path(
//         "example.db",
//         Some(BaseDirectory::App),
//     )
//     .expect("无法解析路径")
//     .to_str()
//     .unwrap()
//     .to_string()
// }S
// use tauri::Connection;
// #[tauri::command]
// fn create(){
//     let conn: Connection = Connection:open("../../test.db").unwrap();

//     conn.execte("create TABLE person(id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER)",(),).unwrap();
// }
