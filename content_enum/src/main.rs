use std::env;
use reqwest::StatusCode;
use tokio;

// string do zamiany na slowo zdjete z pythonowej kolejki
const SPLITT_STRING: &str = "ZPR";

#[tokio::main]
async fn main() {
    // pobranie argumentow wiersza polecen
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        eprintln!("Usage: <url> <word> [--verbose | --no-verbose]");
        return;
    }

    // pobranie URL, slowa oraz flagi verbose z argumentow
    let url = &args[1];
    let word = &args[2];
    let verbose = args.contains(&"--verbose".to_string());

    // utworzenie nowego klienta HTTP
    let client = reqwest::Client::new();
    // wyslanie asynchronicznego zapytania typu GET; zamiana stringa SPLITT_STRING na slowo zdjete z pythonowej kolejki
    let response = client.get(&url.replace(SPLITT_STRING, word)).send().await;

    // przetwarzanie odpowiedzi
    match response {
        Ok(resp) => match resp.status() {
            // jesli status to 200 lub 300 informujemy prorgram Pythonowy o sukciesie
            StatusCode::OK => println!("[+] 200 OK: {}", resp.url()),
            StatusCode::FOUND | StatusCode::MOVED_PERMANENTLY => println!("[+] 300 REDIRECT: {}", resp.url()),
            // jesli flaga verbose jest ustawiona kazdy inny status  jest przekazywany do programu Pythonowego
            _ => {
                if verbose {
                    println!("[-] Other status: {} - {}", resp.status(), resp.url());
                }
            }
        },
        // jesli napotkamy wyjatek, program Pythonowy zostanie o tym poinformowany
        Err(err) => {
            if verbose {
                eprintln!("[-] Error: {}", err);
            }
        },
    }
}
