# textbook_RSA.py

import argparse
from utils import generate_keys, encrypt_plaintext, decrypt_ciphertext, read_keys

# Arguments Settings
parser = argparse.ArgumentParser()
parser.add_argument('--key_size', type=int, default=1024)
parser.add_argument('--generate_keys', action="store_true")
parser.add_argument('--OAEP_key_padding', action="store_true")
parser.add_argument('--decrypt_OAEP', action="store_true")
parser.add_argument('--encrypt_file', type=str, default="")
parser.add_argument('--decrypt_file', type=str, default="")
args = parser.parse_args()


# main function of textbook RSA
def textbook_RSA_func():
    # Key padding option: 0 for not padding, 1 for padding
    key_padding_option = 1 if args.OAEP_key_padding else 0
    # Decrypt OAEP key padding: 0 for not decrypted, 1 for decrypted
    decrypted_OAEP_option = 1 if args.decrypt_OAEP else 0

    # Generate keys
    if args.generate_keys:
        # Generate new keys and return
        generate_keys(key_size=args.key_size)
        return
    else:
        # Read old keys
        public_key, private_key = read_keys()

    # Encrypt plaintext
    if args.encrypt_file != "":
        # File path
        file_path = args.encrypt_file
        # Output path
        output_path = "./test/ciphertext.txt"
        encrypt_plaintext(public_key, file_path, output_path, args.key_size, key_padding_option, decrypted_OAEP_option)

    # Decrypt ciphertext
    if args.decrypt_file != "":
        # File path
        file_path = args.decrypt_file
        # Output path
        output_path = "./test/plaintext.txt"
        decrypt_ciphertext(private_key, file_path, output_path)


if __name__ == '__main__':
    textbook_RSA_func()



