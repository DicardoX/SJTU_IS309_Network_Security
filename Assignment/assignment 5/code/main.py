# main.py

import secrets
import time
from Utils import decimal_to_binary, get_maximum_number, is_perfect_number, euler_phi, are_prime_to_each_other, \
    repeated_modular_multiplication, square_and_multiply_algorithm, is_perfect_power

# Secret Generator
secret_generator = secrets.SystemRandom()


# Miller-Rabin primality test
# Input: num is the tested number, t is the security parameter
# Output: whether this num is prime
def primality_test(num, n):
    # If this number is even or perfect number, return False
    if num % 2 == 0 or is_perfect_number(num):
        return False

    print("Begin primality test...")

    # Compute r and u
    r = 0
    tmpNum = num
    while (tmpNum - 1) % 2 == 0:
        r += 1
        tmpNum = int((tmpNum - 1) / 2 + 1)
    u = int(tmpNum - 1)

    is_prime = False
    # Test for n times
    for idx in range(0, n, 1):
        # Random seed
        a = num
        while not (are_prime_to_each_other(a, num) and a != 1):
            # Must make sure that a is prime to num, so that we can use the Generation Statement of Euler Theorem
            a = secret_generator.randint(1, num - 1)

        # Time counter
        time_mark = time.process_time()
        # Use Generation Statement of Euler Theorem to simplify the calculation
        # Operate u
        new_u = u % euler_phi(num)
        for i in range(0, r, 1):
            new_pow_u = (pow(2, i) % euler_phi(num)) * new_u
            # Use Modular Exponentiation to simplify the pow calculation
            # Judge
            # if repeated_modular_multiplication(a, new_u, num) == 1 or repeated_modular_multiplication(a, new_pow_u, num) == -1:
            if square_and_multiply_algorithm(a, new_u, num) == 1 or square_and_multiply_algorithm(a, new_pow_u, num) == -1:
                is_prime = True
        print("Test", idx, ": a is set to be", a, "| time spent: ", round(time.process_time() - time_mark, 3), "seconds")
    # Output message
    message = "Successfully find a prime!"
    if not is_prime:
        message = "Could not find a prime..."

    print("Finish primality test!", message)
    return is_prime


# Generate number
# Input: n is the security parameter
def generate_prime(n):
    # Set boarder
    max_number = get_maximum_number(n - 1)
    min_number = 0

    # 3n^2 times at most
    for i in range(0, 3 * pow(n, 2), 1):
        print("Iteration", i, "for Prime Generation is processing...")
        # Random algorithm
        ret = secret_generator.randint(min_number, max_number)
        # Add 1 at the head of the binary expression
        ret += pow(2, n - 1)
        print("Successfully generate random seed:", ret)

        if primality_test(ret, n):
            print("---------------------------------------")
            return ret
        print("Failed to generate a prime...Keep trying!")
        print("---------------------------------------")
    return 0


if __name__ == '__main__':
    # Generate first prime
    print("Generating the first prime...")
    print("---------------------------------------")
    prime_num_1 = generate_prime(32)
    # Generate second prime
    print("Generating the second prime...")
    print("---------------------------------------")
    prime_num_2 = generate_prime(32)
    # Display
    print("---------------RESULT------------------")
    print("The first prime is:", prime_num_1)
    print("The second prime is:", prime_num_2)

    # # Test for perfect power
    # if is_perfect_power(4096):
    #     print("4096 is perfect power.")
    # else:
    #     print("4096 is not perfect power")
    # if is_perfect_power(4095):
    #     print("4095 is perfect power.")
    # else:
    #     print("4095 is not perfect power")


