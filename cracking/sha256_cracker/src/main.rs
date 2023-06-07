use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use sha2::{Sha256, Digest};
use std::process::exit;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();

    if args.len() != 3 {
        println!("Invalid amount of arguments");
        println!("Example: cargo run <sha256 hash> <wordlist>");
        exit(1);
    }

    let wanted_hash = &args[1];
    let password_file = &args[2];
    let mut attempts = 1;

    println!("Attempting to crack: {}!\n", wanted_hash);

    let password_list = File::open(password_file)?;
    let reader = BufReader::new(password_list);

    for line in reader.lines() {
        let line = line?;
        let password = line.trim().as_bytes();
        let password_hash = format!("{:x}", Sha256::digest(password));

        println!("[{}] {} == {}", attempts, std::str::from_utf8(password)?, password_hash);
        if password_hash == *wanted_hash {
            println!("Password Found:");
            println!("Password: {} found after {} attempts!!", std::str::from_utf8(password)?, attempts);
            exit(0);
        }
        attempts +=1;
    }

    println!("Not matches found!");
    Ok(())
}
