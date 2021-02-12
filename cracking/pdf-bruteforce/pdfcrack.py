import pikepdf
from tqdm import tqdm

pdfFile = "secret.pdf"
wordlist = "/opt/wordlists/rockyou.txt"

passwords = [ line.strip() for line in open(wordlist) ]

for passowrd in tqdm(passwords, "Decrypting PDF"):
    try:
        with pikepdf.open(pdfFile, password=passowrd) as pdf:
            print("[+] Password found:", password)
            break
    except pikepdf._qpdf.PasswordError as e:
        continue
