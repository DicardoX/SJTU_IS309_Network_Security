# CC2_attack.py

import argparse

from utils import client, server, generate_history_WUP_message, break_AES_key, decrypt_WUP_message


# Arguments Settings
parser = argparse.ArgumentParser()
parser.add_argument('--key_size', type=int, default=128)
parser.add_argument('--OAEP_key_padding', action="store_true")
parser.add_argument('--decrypt_OAEP_for_receiver', action="store_true")
args = parser.parse_args()

# Unit length
unit_length = 16


# Main function for CCA2 attack
def CCA2_attack_func():
    # Key padding option: 0 for not padding, 1 for padding
    key_padding_option = 1 if args.OAEP_key_padding else 0
    # Decrypt OAEP key padding: 0 for not decrypted, 1 for decrypted
    decrypted_OAEP_option = 1 if args.decrypt_OAEP_for_receiver else 0

    # Client
    m_client = client(args.key_size, key_padding_option, decrypted_OAEP_option)
    # Server
    m_server = server(m_client.AES_key, key_padding_option, decrypted_OAEP_option)
    # Generate history message with request and response encrypted with AES key
    history_message = generate_history_WUP_message(m_client.AES_key, m_client.public_key, key_padding_option, decrypted_OAEP_option)

    # --------------- In the following steps, we attempt to break the history message ----------------\
    print("")
    print("-------- Performing CCA2 attack on textbook RSA ----------")

    # First, we need to fake a new message between client and server, which is allowed by CCA2
    fake_request = "We attempt to perform CCA2 attack on textbook RSA"
    # Padding
    while len(fake_request) % unit_length != 0:
        fake_request += "\0"

    # Then, we break the AES key according to method described in the paper
    AES_key = break_AES_key(fake_request, m_client.public_key, m_client.private_key, history_message.encrypted_key, args.key_size)
    print("Decrypted AES key:", AES_key)
    print("")

    # At last, we decrypt the history message
    print("Decrypting history WUP message with decrypted AES key...")
    decrypt_WUP_message(history_message, AES_key)


if __name__ == '__main__':
    CCA2_attack_func()
