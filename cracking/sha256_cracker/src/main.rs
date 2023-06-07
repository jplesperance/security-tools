use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use sha2::{Sha256, Digest};
use std::process::exit;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 3 {
        println!("Invalid amount of arguments");
        println!("Example: cargo run <sha256 hash> <wordlist>");
        exit(1);
    }

    let wanted_hash: &String = &args[1];
    let password_file: &String = &args[2];
    let mut attempts = 1;

    println!("Attempting to crack: {}!\n", wanted_hash);

    let password_list: File = File::open(password_file).unwrap();
    let reader: BufReader<File> = BufReader::new(password_list);

    for line in reader.lines() {
        let line: String = line.unwrap();
        let password: Vec<u8> = line.trim().to_owned().into_bytes();
        let password_hash: String = format!("{:x}", Sha256::digest(&password));

        println!("[{}] {} == {}", attempts, std::str::from_utf8(&password).unwrap(), password_hash);
        if &password_hash == wanted_hash {
            println!("Password Found:");
            println!("Password: {} found after {} attempts!!", std::str::from_utf8(&password).unwrap(), attempts);
            exit(0);
        }
        attempts +=1;
    }

    println!("Not matches found!")
}