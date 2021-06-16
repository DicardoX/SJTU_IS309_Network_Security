# utils.py

import random
import numpy as np
from binascii import b2a_hex, a2b_hex
import argparse
import os
# pip install Crypto pycryptodome, then modify the corresponding lib folder from crypto/crypto-1.4.1.dist-info
# into Crypto/Crypto-1.4.1.dist-info
from Crypto.Cipher import AES

# Small primes
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]


# ------------------------------------- Implementation of Textbook RSA -------------------------------------


# Judge whether a number is perfect number
# Very limited amount, directly judge
def is_perfect_number(num):
    return (num == 6) or (num == 28) or (num == 496) or (num == 8128) or (num == 33550336) or (num == 8589869056)


# Test whether the target is a prime by using Miller-Rabin algorithm
# Optimized version, much faster
def miller_rabin_test(target, n):
    # If this number is even or perfect number, return False
    if target % 2 == 0 or is_perfect_number(target):
        return False

    # If in the list of small primes, return
    if target in small_primes:
        return True

    # If can be divided to the small primes, return False
    for prime in small_primes:
        if target % prime == 0:
            return False

    target_op = target - 1
    r = 0
    while target_op % 2 == 0:
        target_op = target_op // 2
        r += 1
    u = int(target_op)

    # Recursively test
    for i in range(n):
        a = random.randrange(2, target - 1)
        v = pow(a, u, target)
        if v != 1:
            j = 0
            while v != target - 1:
                if j == r - 1:
                    # print("Testing for target %d ... False" % target)
                    return False
                else:
                    j += 1
                    v = (v ** 2) % target
    # print("Testing for target %d ... Succeed!" % target)
    return True


# Generate prime with the length of bits equals to key_size
def generate_prime(key_size):
    # print("----------------- Begin Generating Prime ---------------------")
    # print("Prime length: %d bits" % key_size)
    # This loop will end in 3 * pow(length, 2) at most
    while True:
        # Set 1 in the highest bit
        target = random.randrange(2 ** (key_size - 1), 2 ** key_size)
        if miller_rabin_test(target, key_size):
            return target


# Fast exp with mod
def fast_exp_mod(base, exponent, mod_base):
    res = 1
    while exponent != 0:
        if (exponent & 1) == 1:
            res = (res * base) % mod_base
        exponent >>= 1
        # base, base^2, base^4, ...., base^{2^n}
        base = (base * base) % mod_base
    return res


# Get gcd(a, b) by Euclidean algorithm
def gcd(a, b):
    remainder = a % b
    while remainder != 0:
        a = b
        b = remainder
        remainder = a % b
    return b


# Extended Euclidean Algorithm
# Ref: https://anh.cs.luc.edu/331/notes/xgcd.pdf
def extended_euclidean(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        q = a // b
        x1, x0 = x0 - q*x1, x1
        y1, y0 = y0 - q*y1, y1
        a, b = b, a % b
    return a, x0, y0


# Generate keys
def generate_keys(key_size):
    print("----------------- Begin Generating Keys ---------------------")

    # Counter
    counter = 0

    # Generate big primes
    print("Generating big primes (may take some time) ...")
    N = 1
    prime_p, prime_q = 1, 1
    # Generate N with the target size
    while N.bit_length() != key_size:
        print("Try %d for the generation of big primes..." % counter)
        # Generate big prime p and q to form N
        unit_key_size = key_size // 2
        prime_p = generate_prime(unit_key_size)
        prime_q = generate_prime(key_size - unit_key_size)
        N = prime_p * prime_q
        counter += 1
    # Euler phi function of N
    print("Calculating Euler phi function of N...")
    phi_N = (prime_p - 1) * (prime_q - 1)

    # Public key elm, smaller should be better
    print("Formulating public key and private key...")
    e = random.randrange(3, phi_N)
    gcd_res = 0
    while True:
        gcd_res, _, _ = extended_euclidean(e, phi_N)
        if gcd_res != 1:
            e = random.randrange(3, phi_N)
        else:
            break
    # Private key elm, use extended Extended Euclidean Algorithm
    gcd_res, d, _ = extended_euclidean(e, phi_N)
    if gcd_res != 1:
        print("Error occurred when generating the inverse of the modular...exit")
        exit(1)

    # Form the keys
    public_key = (N, e)
    private_key = (N, d % phi_N)
    print("Keys generation if completed! | Public key: (N, %d) | Private key: (N, %d)" % (e, d % phi_N))

    # Write into txt
    # Public key
    txt_writer(public_key, "./keys/public_key.txt")
    # Private key
    txt_writer(private_key, "./keys/private_key.txt")


# Read keys from txt
def read_keys():
    # Keys
    public_key = []
    private_key = []

    public_str_list = txt_reader("./keys/public_key.txt")
    for i in range(len(public_str_list)):
        public_key.append(int(public_str_list[i]))

    private_str_list = txt_reader("./keys/private_key.txt")
    for i in range(len(private_str_list)):
        private_key.append(int(private_str_list[i]))

    return tuple(public_key), tuple(private_key)


# Read txt
def txt_reader(file_path):
    ret = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            # Remove \n
            line = line.replace("\n", "")
            ret.append(line)
    f.close()
    return ret


# Write txt
def txt_writer(output_list, output_path):
    ret = []
    # Reconstruct the output file
    if os.path.exists(output_path):
        os.remove(output_path)
    # Write
    with open(output_path, "w") as f:
        for i in range(len(output_list)):
            f.write(str(output_list[i]) + "\n")
    f.close()


# Encrypt
def encrypt_plaintext(public_key, file_path, output_path):
    print("-------------- Begin Encrypting plaintext ------------------")

    # Ciphertext list
    ciphertext_list = []
    # Str list from txt
    str_list = txt_reader(file_path)

    for i in range(len(str_list)):
        cur_str = bytes(str_list[i], encoding='utf-8')
        plaintext = int(b2a_hex(cur_str), 16)
        ciphertext = fast_exp_mod(plaintext, public_key[1], public_key[0])
        ciphertext_list.append(ciphertext)
    # Write to txt
    print("Encrypted result:", ciphertext_list)
    txt_writer(ciphertext_list, output_path)


# Decrypt
def decrypt_ciphertext(private_key, file_path, output_path):
    print("-------------- Begin Encrypting plaintext ------------------")

    # Plaintext list
    plaintext_list = []
    # Str list from txt
    str_list = txt_reader(file_path)

    for i in range(len(str_list)):
        ciphertext = int(str_list[i])
        interpret = fast_exp_mod(ciphertext, private_key[1], private_key[0])
        cur_int = a2b_hex(hex(interpret)[2:])
        plaintext = str(cur_int, encoding='utf-8')
        plaintext_list.append(plaintext)
    # Write to txt
    print("Decrypted result:", plaintext_list)
    txt_writer(plaintext_list, output_path)


# --------------------------------------- CCA2 Attack on Textbook RSA ---------------------------------------


# WUP class
class WUP:
    def __init__(self, request, response, key):
        self.request = request
        self.response = response
        self.encrypted_key = key


# Client class
class client:
    def __init__(self, key_size):
        # Keys generated by textbook_RSA
        self.public_key, self.private_key = read_keys()
        # AES key
        self.AES_key = random.randrange(1 << (key_size - 1), 2 ** key_size)
        while self.AES_key % 2 == 0:
            self.AES_key = random.randrange(1 << (key_size - 1), 2 ** key_size)

    # Encrypt the plaintext
    def encrypt_plaintext(self, plaintext):
        # AES Encryptor with ECB mode
        AES_encryptor = AES.new(a2b_hex(hex(self.AES_key)[2:]), AES.MODE_ECB)
        # Unit length
        unit_length = 16
        # Padding
        while len(plaintext) % unit_length != 0:
            plaintext += "\0"
        # Ciphertext
        ciphertext = str(b2a_hex(AES_encryptor.encrypt(plaintext.encode('utf-8'))), encoding='utf-8')
        return ciphertext

    # Decrypt the ciphertext
    def decrypt_ciphertext(self, ciphertext):
        # AES Decryptor with ECB mode
        AES_decryptor = AES.new(a2b_hex(hex(self.AES_key)[2:]), AES.MODE_ECB)
        # Plaintext
        plaintext = str(AES_decryptor.decrypt(a2b_hex(ciphertext)), encoding='uft-8')
        return plaintext.rstrip("\0")


# Server class
class server:
    def __init__(self, AES_key):
        # Keys generated by textbook_RSA
        self.public_key, self.private_key = read_keys()
        # AES key
        self.AES_key = AES_key

    # Encrypt the plaintext
    def encrypt_plaintext(self, plaintext):
        # AES Encryptor with ECB mode
        AES_encryptor = AES.new(a2b_hex(hex(self.AES_key)[2:]), AES.MODE_ECB)
        # Unit length
        unit_length = 16
        # Padding
        while len(plaintext) % unit_length != 0:
            plaintext += "\0"
        # Ciphertext
        ciphertext = str(b2a_hex(AES_encryptor.encrypt(plaintext.encode('utf-8'))), encoding='utf-8')
        return ciphertext

    # Decrypt the ciphertext
    def decrypt_ciphertext(self, ciphertext):
        # AES Decryptor with ECB mode
        AES_decryptor = AES.new(a2b_hex(hex(self.AES_key)[2:]), AES.MODE_ECB)
        # Plaintext
        plaintext = str(AES_decryptor.decrypt(a2b_hex(ciphertext)), encoding='utf-8')
        return plaintext.rstrip("\0")


# Generate a history message
def generate_history_WUP_message(AES_key, public_key):
    print("--------- Begin Generating history WUP message -----------")

    # WUP message
    message = WUP("", "", "")
    # Unit length
    unit_length = 16
    # AES Encryptor with ECB mode
    AES_encryptor = AES.new(a2b_hex(hex(AES_key)[2:]), AES.MODE_ECB)

    # Request
    request = txt_reader("./test/request.txt")[0]
    # Padding
    while len(request) % unit_length != 0:
        request += "\0"
    # Encrypt request with AES
    message.request = b2a_hex(AES_encryptor.encrypt(request.encode('utf-8')))

    # Response
    response = txt_reader("./test/response.txt")[0]
    # Padding
    while len(response) % unit_length != 0:
        response += "\0"
    # Encrypt response with AES
    message.response = b2a_hex(AES_encryptor.encrypt(response.encode('utf-8')))

    # Encrypt AES with public key in RSA
    message.encrypted_key = fast_exp_mod(AES_key, public_key[1], public_key[0])

    print("Original request:", request)
    print("Original response:", response)
    print("")
    print("######################## History WUP Message Info ########################")
    print("- Encrypted request (bytes): ", message.request)
    print("- Encrypted response (bytes): ", message.response)
    print("- Encrypted AES key:", message.encrypted_key)
    print("##########################################################################")

    return message


# Decrypt WUP message with CCA method
def query_decryptor(encrypted_request, encrypted_key, private_key, key_size):
    # Decrypted AES key with private key in RSA
    AES_key = bin(fast_exp_mod(encrypted_key, private_key[1], private_key[0]))[-key_size:]
    AES_key = int(AES_key, 2)
    string = ""
    for i in hex(AES_key)[2:]:
        string += i
    # Padding, since we transfer from binary to hex
    while len(string) < int(key_size / 4):
        string = "0" + string
    # AES Decryptor
    AES_decryptor = AES.new(a2b_hex(string), AES.MODE_ECB)

    plaintext = AES_decryptor.decrypt(a2b_hex(encrypted_request))
    return plaintext


# Break AES key
# Ref: https://arxiv.org/abs/1802.03367
def break_AES_key(fake_request, public_key, private_key, message_encrypted_key, key_size):
    print("Breaking AES key...")

    # AES key
    AES_key = 0

    # Traverse each bit
    for i in range(key_size, 0, -1):
        trial_key = int(AES_key >> 1) + (1 << (key_size - 1))
        # print("Trial key:", bin(trial_key)[2:])
        # AES Encryptor with ECB mode
        AES_encryptor = AES.new(a2b_hex(hex(trial_key)[2:]), AES.MODE_ECB)
        # Encrypted request
        encrypted_request = str(b2a_hex(AES_encryptor.encrypt(fake_request.encode('utf-8'))), encoding='utf-8')
        # Encrypted key
        factor = fast_exp_mod(2, (i - 1) * public_key[1], public_key[0])
        encrypted_key = fast_exp_mod(message_encrypted_key * factor, 1, public_key[0])
        # Plain request from querying decryptor (CCA)
        plain_request = query_decryptor(encrypted_request, encrypted_key, private_key, key_size)

        try:
            plain_request = plain_request.decode().strip(b'\x00'.decode())
        except UnicodeDecodeError:
            plain_request = "error"

        if plain_request == "We attempt to perform CCA2 attack on textbook RSA":
            AES_key = trial_key
        else:
            trial_key = int(AES_key >> 1)
            # print("Trial key (again):", bin(trial_key)[2:])
            string = ""
            for j in hex(trial_key)[2:]:
                string += j
            # Padding, since we transfer from binary to hex
            while len(string) < int(key_size / 4):
                string = "0" + string
            AES_encryptor = AES.new(a2b_hex(string), AES.MODE_ECB)
            encrypted_request = str(b2a_hex(AES_encryptor.encrypt(fake_request.encode('utf-8'))), encoding='utf-8')
            # Encrypted key
            factor = fast_exp_mod(2, (i - 1) * public_key[1], public_key[0])
            encrypted_key = fast_exp_mod(message_encrypted_key * factor, 1, public_key[0])
            # Plain request from querying decryptor (CCA)
            plain_request = query_decryptor(encrypted_request, encrypted_key, private_key, key_size)
            AES_key = trial_key

    return AES_key


# Decrypt WUP message using AES key
def decrypt_WUP_message(message, AES_key):
    AES_decryptor = AES.new(a2b_hex(hex(AES_key)[2:]), AES.MODE_ECB)
    plain_request = str(AES_decryptor.decrypt(a2b_hex(message.request)), encoding='utf-8').rstrip("\0")
    plain_response = str(AES_decryptor.decrypt(a2b_hex(message.response)), encoding='utf-8').rstrip("\0")
    print("")
    print("################### Decrypted History WUP Message Info ###################")
    print("- Decrypted request: ", plain_request)
    print("- Decrypted response: ", plain_response)
    print("##########################################################################")
    print("")



