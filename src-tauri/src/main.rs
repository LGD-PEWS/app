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
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
    // tauri::Builder::default()
    //     .plugin(tauri_plugin_sql::Builder::default().build())
    //     .run(tauri::generate_context!())
    //     .expect("error while running tauri application");
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
