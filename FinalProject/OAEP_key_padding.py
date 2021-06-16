# OAEP_key_padding.py


import hashlib
from binascii import b2a_hex, a2b_hex
import random


# K0
k0_bits_int = 256
k0_bits_fill = '0256b'


# Transfer 10-based into binary
def dec_to_binary(num):
    binary_form = bin(num)[2:]
    return binary_form


# Transfer binary into 10-based
def binary_to_dec(bits):
    num = int(bits, 2)
    return num


# Padding
def binary_padding(msg, key_size):
    # Oracle
    oracle_1 = hashlib.sha512()
    oracle_2 = hashlib.sha512()
    # Rand bits
    rand_bits = format(random.SystemRandom().getrandbits(k0_bits_int), k0_bits_fill)

    if len(msg) <= (key_size - k0_bits_int):
        k1_bits = key_size - k0_bits_int - len(msg)
        padded_msg = msg + ("0" * k1_bits)
    else:
        padded_msg = msg

    # Update oracles
    oracle_1.update(rand_bits.encode('utf-8'))
    x = format(int(padded_msg, 2) ^ int(oracle_1.hexdigest(), 16), '0768b')
    oracle_2.update(x.encode('utf-8'))
    y = format(int(oracle_2.hexdigest(), 16) ^ int(rand_bits, 2), k0_bits_fill)

    return x + y, len(msg)


# Unpadding
def binary_unpadding(padded_msg, n_bits):
    # Oracle
    oracle_1 = hashlib.sha512()
    oracle_2 = hashlib.sha512()

    x = padded_msg[0:768]
    y = padded_msg[768:]

    oracle_2.update(x.encode('utf-8'))
    r = format(int(y, 2) ^ int(oracle_2.hexdigest(), 16), k0_bits_fill)

    oracle_1.update(r.encode('utf-8'))
    msg = format(int(x, 2) ^ int(oracle_1.hexdigest(), 16), '0768b')
    msg = msg[0: n_bits]
    return binary_to_dec(msg)


# OAEP key padding
def OAEP_key_padding(plaintext, key_size):
    # Transfer to binary
    bits = dec_to_binary(plaintext)
    # Padding
    padded_msg, n_bits = binary_padding(bits, key_size)
    # New cipher
    plaintext = binary_to_dec(padded_msg)
    # plaintext = binary_unpadding(padded_msg, n_bits)
    return plaintext, n_bits


# OAEP key unpadding
def OAEP_key_unpadding(plaintext, n_bits):
    # Transfer to binary
    padded_msg = dec_to_binary(plaintext)
    # # Padding
    # padded_msg, n_bits = binary_padding(bits, key_size)
    # New cipher
    plaintext = binary_unpadding(padded_msg, n_bits)
    return plaintext
