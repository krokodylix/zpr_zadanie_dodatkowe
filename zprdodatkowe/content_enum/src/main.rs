use std::env;
use reqwest::StatusCode;
use tokio;

const SPLITT_STRING: &str = "ZPR";

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        eprintln!("Usage: <url> <word> [--verbose | --no-verbose]");
        return;
    }

    let url = &args[1];
    let word = &args[2];
    let verbose = args.contains(&"--verbose".to_string());

    let client = reqwest::Client::new();
    let response = client.get(&url.replace(SPLITT_STRING, word)).send().await;

    match response {
        Ok(resp) => match resp.status() {
            StatusCode::OK => println!("[+] 200 OK: {}", resp.url()),
            StatusCode::FOUND | StatusCode::MOVED_PERMANENTLY => println!("[+] 300 REDIRECT: {}", resp.url()),
            _ => {
                if verbose {
                    println!("[-] Other status: {} - {}", resp.status(), resp.url());
                }
            }
        },
        Err(err) => {
            if verbose {
                eprintln!("[-] Error: {}", err);
            }
        },
    }
}
