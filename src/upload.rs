use std::{io::{BufWriter, Write}, fs::File};
use serde_json::{Value, json};
use crate::BOT_TO_SEND;
pub async fn main_upload(channel_id: u64, user: String, input: String) {
    let mut path= std::env::current_dir().unwrap();
    let mut err_str= String::new();
    let mut show_err= true;
    let mut ninput;
    let mut final_buf: Vec<u8>= Vec::new();
    if input.contains("//") {
        ninput= &input[input.find("//").unwrap() + 2..];
        if ninput.contains('/') {
            ninput= &ninput[..ninput.find('/').unwrap()];
            match ninput {
                "gofile.io" => {
                    match reqwest::get("https://api.gofile.io/createAccount").await {
                        Ok(req) => {
                            match req.json::<Value>().await {
                                Ok(json) => {
                                    if json["status"].as_str().unwrap_or("")== "ok" {
                                        if input.contains("/d/") {
                                            let mut pre= &input[input.find("/d/").unwrap() + 3..];
                                            if let Some(index)= pre.find('/') {
                                                pre= &pre[..index];
                                            }
                                            let token= json["data"]["token"].as_str().unwrap_or("");
                                            match reqwest::get(format!("https://api.gofile.io/getContent?contentId={}&token={}&websiteToken=abcde&cache=false", pre, token)).await {
                                                Ok(response) => {
                                                    match response.json::<Value>().await {
                                                        Ok(json) => {
                                                            if json["status"].as_str().unwrap_or("")== "ok" {
                                                                let child= json["data"]["childs"][0].as_str().unwrap_or("");
                                                                match json["data"]["contents"].as_object() {
                                                                    Some(map) => {
                                                                        if map.contains_key(child) {
                                                                            let content= &json["data"]["contents"][child];
                                                                            path.push(content["name"].as_str().unwrap_or("Default.txt"));
                                                                            let client= reqwest::Client::new();
                                                                            match client.execute(reqwest::Client::new()
                                                                                    .get(content["link"].as_str().unwrap())
                                                                                    .header("Cookie", &format!("accountToken= {}", token)).build().unwrap()).await {
                                                                                Ok(response) => {
                                                                                    match response.bytes().await {
                                                                                        Ok(bytes) => {
                                                                                            final_buf.extend(&bytes);
                                                                                            show_err= false;
                                                                                        }
                                                                                        Err(e) => {err_str= e.to_string();}
                                                                                    }
                                                                                }
                                                                                Err(e) => {err_str= e.to_string();}
                                                                            }
                                                                        }else{
                                                                            err_str= "Unable to fetch the child index of the files".to_string();
                                                                        }
                                                                    }
                                                                    None => {err_str= "Unable to fetch the file indexes".to_string();}
                                                                }
                                                            }else{
                                                                err_str= "Unable to fetch the URL file (maybe it doesn't exist?)".to_string();
                                                            }
                                                        }
                                                        Err(e) => {err_str= e.to_string();}
                                                    }
                                                }
                                                Err(e) => {err_str= e.to_string();}
                                            }
                                        }else{
                                            err_str= "Invalid Gofile.io link".to_string();
                                        }
                                    }else{
                                        err_str= "Unable to fetch the token to download the file".to_string();
                                    }
                                }
                                Err(e) => {err_str= e.to_string();}
                            }
                        }
                        Err(e) => {err_str= e.to_string();}
                    }
                }
                "anonfiles.com" => {
                    let mut pre= &input[input.find(".com/").unwrap() + 5..];
                    if let Some(index)= pre.find('/') {
                        pre= &pre[..index];
                    }
                    match reqwest::get(format!("https://api.anonfiles.com/v2/file/{}/info", pre)).await {
                        Ok(response) => {
                            match response.json::<Value>().await {
                                Ok(json) => {
                                    if json["status"].as_bool().unwrap_or(false) {
                                        let response= reqwest::get(json["data"]["file"]["url"]["short"].as_str().unwrap_or("")).await.unwrap();
                                        match response.text().await {
                                            Ok(text) => {
                                                if text.contains("<h1 class=\"text-center text-wordwrap\">") && text.contains("href=\"https://cdn-") {
                                                    let mut name= &text[text.find("<h1 class=\"text-center text-wordwrap\">").unwrap() + 38..];
                                                    name= &name[..name.find("</h1>").unwrap()];
                                                    path.push(name);
                                                    let mut url= &text[text.find("href=\"https://cdn-").unwrap() + 6..];
                                                    url= &url[..url.find('\"').unwrap()];
                                                    match reqwest::get(url).await {
                                                        Ok(reponse) => {
                                                            match reponse.bytes().await {
                                                                Ok(bytes) => {
                                                                    final_buf.extend(&bytes);
                                                                    show_err= false;
                                                                }
                                                                Err(e) => {err_str= e.to_string();}
                                                            }
                                                        }
                                                        Err(e) => {err_str= e.to_string();}
                                                    }
                                                }else{
                                                    err_str= "Invalid Anonfiles.com HTML header".to_string();
                                                }
                                            }
                                            Err(e) => {err_str= e.to_string();}
                                        }
                                    }
                                }
                                Err(e) => {err_str= e.to_string();}
                            }
                        }
                        Err(e) => {err_str= e.to_string();}
                    }
                }
                "pixeldrain.com" => {
                    if input.contains("/u/") {
                        let mut pre= &input[input.find("/u/").unwrap() + 3..];
                        if let Some(index)= pre.find('/') {
                            pre= &pre[..index];
                        }
                        match reqwest::get(format!("https://pixeldrain.com/api/file/{}/info", pre)).await {
                            Ok(response) => {
                                match response.json::<Value>().await {
                                    Ok(json) => {
                                        if json["success"].as_bool().unwrap_or(false) {
                                            path.push(json["name"].as_str().unwrap_or("Default.txt"));
                                            match reqwest::get(format!("https://pixeldrain.com/api/file/{}?download=", pre)).await {
                                                Ok(response) => {
                                                    match response.bytes().await {
                                                        Ok(bytes) => {
                                                            final_buf.extend(&bytes);
                                                            show_err= false;
                                                        }
                                                        Err(e) => {err_str= e.to_string();}
                                                    }
                                                }
                                                Err(e) => {err_str= e.to_string();}
                                            }
                                        }else{
                                            err_str= json["message"].as_str().unwrap_or("Unknown").to_string();
                                        }
                                    }
                                    Err(e) => {err_str= e.to_string();}
                                }
                            }
                            Err(e) => {err_str= e.to_string();}
                        }
                    }else{
                        err_str= "Invalid pixeldrain.com URL".to_string();
                    }
                }
                _ => {
                    match reqwest::get(&input).await {
                        Ok(response) => {
                            let headers= response.headers();
                            let mut raw_get= true;
                            if headers.contains_key("content-disposition") {
                                let header= headers.get("content-disposition").unwrap().to_str().unwrap();
                                if header.contains("filename=\"") {
                                    raw_get= false;
                                    let header= &header[header.find("filename=\"").unwrap() + 10..header.len() - 1];
                                    path.push(header);
                                }
                            }
                            match response.bytes().await {
                                Ok(bytes) => {
                                    if raw_get {
                                        let spath= input.split('/').collect::<Vec<&str>>();
                                        path.push(spath.last().unwrap());
                                    }
                                    final_buf.extend(&bytes);
                                    show_err= false;
                                }
                                Err(e) => {
                                    err_str= format!("Unknown Proxy URL \"{}\", use either \"anonfiles.com\", \"pixeldrain.com\", \"gofile.io\" or an attachment\nError: {:?}", ninput, e);
                                }
                            }
                        }
                        Err(e) => {err_str= e.to_string();}
                    }
                }
            }
        }else{
            err_str= "Input isn't a formal URL link".to_string();
        }
    }else{
        err_str= "Input isn't a formal URL link".to_string();
    }
    if show_err {
        BOT_TO_SEND.lock().await.push(json!({
            "channel": channel_id,
            "content": &format!("```❗ An error occurred: {}```", err_str),
            "react": ["🔴"]
        }));
    }else{
        match File::create(&path) {
            Ok(f) => {
                let mut f= BufWriter::new(f);
                if let Err(e)= f.write_all(&final_buf) {
                    err_str= e.to_string();
                    show_err= true;
                }else if let Err(e)= f.flush() {
                    err_str= e.to_string();
                    show_err= true;
                }
                drop(f);
            }
            Err(e) => {
                err_str= e.to_string();
                show_err= true;
            }
        }
        if show_err {
            BOT_TO_SEND.lock().await.push(json!({
                "channel": channel_id,
                "content": &format!("```❗ An error occurred: {}```", err_str),
                "react": ["🔴"]
            }));
        }else{
            BOT_TO_SEND.lock().await.push(json!({
                "channel": channel_id,
                "content": &format!("```❗ Successfully uploaded to the target PC \"{}\" to \"{}\"\n\nRequested by: {}```", input.trim(), path.to_string_lossy(), user),
                "react": ["🔴"]
            }));
        }
    }
}