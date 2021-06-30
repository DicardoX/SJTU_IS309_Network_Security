# Utils.py

#############################################################################################################
#                                              UTILS LIST                                                   #
#############################################################################################################
# - decimal_to_binary(decNum): Transfer decimal into binary expression                                      #
# - is_perfect_number(num): Judge whether a number is perfect number                                        #
# - euler_phi(n): Euler Phi Function                                                                        #
# - get_maximum_number(t): Get the maximum number when input the security parameter n                       #
# - are_prime_to_each_other(num1, num2): Judge whether num1 and num2 are prime to each other,               #
#   use Euclidean Algorithm                                                                                 #
# - repeated_modular_multiplication(a, u, num): Repeated Modular Multiplication to use                      #
#   Modular Exponentiation to simplify the pow calculation                                                  #
# - square_and_multiply_algorithm(a, u, num): Square and Multiply Algorithm to see Modular Exponentiation   #
#   to simplify the pow calculation                                                                         #
# - is_perfect_power(num): Judge whether num is a perfect power                                             #
#############################################################################################################

# Transfer decimal into binary expression
# Input: a int number of decimal expression
# Output: a string indicates the binary expression of the number
def decimal_to_binary(decNum):
    ret = []
    if decNum < 0:
        return '-' + decimal_to_binary(abs(decNum))
    while True:
        decNum, remainder = divmod(decNum, 2)
        ret.append(str(remainder))
        if decNum == 0:
            return ''.join(ret[::-1])


# Judge whether a number is perfect number
# Very limited amount, directly judge
def is_perfect_number(num):
    return (num == 6) or (num == 28) or (num == 496) or (num == 8128) or (num == 33550336) or (num == 8589869056)


# Euler Phi Function
# Input: a number n
# Output: Euler phi function \phi(n)
def euler_phi(n):
    m = int(pow((n + 0.5), 0.5))
    ans = n
    for i in range(2, m, 1):
        if n % i == 0:
            ans = int(ans / i * (i - 1))
        while n % i == 0:
            n /= i
    if n > 1:
        ans = int(ans / n * (n - 1))
    return ans


# Get the maximum number when input the security parameter n
def get_maximum_number(n):
    ret = 1
    while n > 0:
        ret *= 2
        n -= 1
    return ret - 1


# Judge whether num1 and num2 are prime to each other, use Euclidean Algorithm
def are_prime_to_each_other(num1, num2):
    A = max(num1, num2)
    B = min(num1, num2)
    while B > 0:
        Remainder = A % B
        A = B
        B = Remainder
    return A == 1


# Repeated Modular Multiplication
# Input: a^u % n
# Output: the calculated value
def repeated_modular_multiplication(a, u, num):
    ret = a
    for i in range(1, u, 1):
        ret = (ret * a) % num
    return ret


# Square and Multiply Algorithm
# Input: a^u % n
# Output: the calculated value
def square_and_multiply_algorithm(a, u, num):
    # Build dictionary
    count = 1
    remainders = {}
    while count <= u:
        if int(count / 2) in remainders.keys():
            remainders[count] = pow(remainders[int(count / 2)], 2) % num
        else:
            # First element
            remainders[count] = a % num
        count *= 2
    # Statistic
    ret = 1
    while count > 0 and u > 0:
        # Too big
        if count > u:
            count /= 2
            continue
        # Fit
        u -= count
        ret = (ret * remainders[count]) % num
        count /= 2
    return ret


# Judge whether num is a perfect power
def is_perfect_power(num):
    s = int(pow(num, 0.5))
    for i in range(2, s + 1, 1):
        k = 2
        while pow(i, k) < num:
            k += 1
        if pow(i, k) == num:
            return True
    return False
