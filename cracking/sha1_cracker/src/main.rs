use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 3 {
        println!("Usage: ");
        println!("sha1_cracker: <wordlist.txt> <sha1_hash>");
        return;
    }

}
