# CC2_attack.py

import argparse

from utils import client, server, generate_history_WUP_message, break_AES_key, decrypt_WUP_message


# Arguments Settings
parser = argparse.ArgumentParser()
parser.add_argument('--key_size', type=int, default=128)
args = parser.parse_args()

# Unit length
unit_length = 16


# Main function for CCA2 attack
def CCA2_attack_func():
    # Client
    m_client = client(args.key_size)
    # Server
    m_server = server(m_client.AES_key)
    # Generate history message with request and response encrypted with AES key
    history_message = generate_history_WUP_message(m_client.AES_key, m_client.public_key)

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
