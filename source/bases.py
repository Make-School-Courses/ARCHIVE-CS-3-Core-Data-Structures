#!python

import string
# Hint: Use these string constants to encode/decode hexadecimal digits and more
# string.digits is '0123456789'
# string.hexdigits is '0123456789abcdefABCDEF'
# string.ascii_lowercase is 'abcdefghijklmnopqrstuvwxyz'
# string.ascii_uppercase is 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# string.ascii_letters is ascii_lowercase + ascii_uppercase
# string.printable is digits + ascii_letters + punctuation + whitespace

# Characters to represent digits up to base 36 [0-9a-z]
BASE_36_CHARS = string.digits + string.ascii_lowercase
# Dictionary of character-to-value mappings for fast (constant-time) lookup
BASE_36_CHAR_MAP = {char: index for index, char in enumerate(BASE_36_CHARS)}
# Immutable set of uppercase characters for fast (constant-time) lookup
UPPERCASE_CHARS = frozenset(char for char in string.ascii_uppercase)


def char_for_value(value):
    """Return character to represent digit with given numerical value."""
    assert 0 <= value < 36, 'digit value out of range (0-35): {}'.format(value)
    # This is fast due to constant-time lookup by string index
    return BASE_36_CHARS[value]


def value_of_char(digit):
    """Return numerical value represented by given digit character."""
    # Handle uppercase letters [A-Z] by lowercasing them
    if digit in UPPERCASE_CHARS:
        digit = digit.lower()
    assert digit in BASE_36_CHAR_MAP, 'unknown digit value: {}'.format(digit)
    # This works but is slow due to linear search through string of characters
    # return BASE_36_CHARS.index(digit)  # Worst case O(base) time
    # This is faster due to constant-time lookup in dictionary using hashing
    return BASE_36_CHAR_MAP[digit]


def decode(digits, base):
    """Decode given digits in given base to number in base 10.
    digits: str -- string representation of number (in given base)
    base: int -- base of given number
    return: int -- integer representation of number (in base 10)"""
    # Handle up to base 36 [0-9a-z]
    assert 2 <= base <= 36, 'base is out of range: {}'.format(base)

    # Call decode functions for all solutions
    number_1 = decode_solution_1(digits, base)
    number_1b = decode_solution_1b(digits, base)
    number_2 = decode_solution_2(digits, base)
    number_3 = decode_solution_3(digits, base)
    number_4 = decode_solution_4(digits, base)
    number_5 = decode_recursive(digits, base)
    number_6 = decode_cheating(digits, base)
    # All results should match
    assert number_1 == number_1b
    assert number_1 == number_2
    assert number_2 == number_3
    assert number_3 == number_4
    assert number_4 == number_5
    assert number_5 == number_6
    return number_4


def decode_solution_1(digits, base):
    """Solution 1: Start decoding rightmost digit and count exponents up.
    Running time: O(n^2) where n is number of digits in given string (length).
    Although it has only one loop, it uses slow exponentiation operation that
    takes O(exponent) time, which is worst case O(n) time at end of loop."""
    number = 0
    # Loop over digits in reverse order and iterate exponent from 0 up to n-1
    for exponent, digit in enumerate(reversed(digits)):  # Always n iterations
        # Find numerical value of next rightmost digit
        digit_value = value_of_char(digit)
        assert 0 <= digit_value < base
        # Add this digit value times power of base
        number += digit_value * (base ** exponent)  # Worst case O(n) time
    return number


def decode_solution_1b(digits, base):
    """Solution 1b: Code above rewritten as a super compact list comprehension
    that's incomprehensible and abhorrent. Please *NEVER* write code like this.
    It's cute, but clearly you hate working with other people. You're fired."""
    return sum(value_of_char(d) * base**e for e, d in enumerate(digits[::-1]))


def decode_solution_2(digits, base):
    """Solution 2: Start decoding leftmost digit and count exponents down.
    Running time: O(n^2) where n is number of digits in given string (length).
    Although it has only one loop, it uses slow exponentiation operation that
    takes O(exponent) time, which is worst case O(n) time at start of loop."""
    number = 0
    max_exponent = len(digits) - 1
    # Loop over digits and iterate exponent from n-1 down to 0
    for iteration, digit in enumerate(digits):  # Always n iterations
        # Find numerical value of next leftmost digit
        digit_value = value_of_char(digit)
        assert 0 <= digit_value < base
        # Calculate actual exponent to use
        exponent = max_exponent - iteration
        # Add this digit value times power of base
        number += digit_value * (base ** exponent)  # Worst case O(n) time
    return number


def decode_solution_3(digits, base):
    """Solution 3: Start decoding rightmost digit and count base powers up.
    Running time: O(n) where n is number of digits in given string (length).
    Faster than Solutions 1 & 2 because it avoids exponentiation operation and
    only slow operation used is multiplication, which is still much faster."""
    number = 0
    # Iterate power of base with exponent from 0 up to n-1
    power = 1  # power is (base ** exponent) at all times
    # Loop over digits in reverse order
    for digit in reversed(digits):  # Always n iterations
        # Find numerical value of next rightmost digit
        digit_value = value_of_char(digit)
        assert 0 <= digit_value < base
        # Add this digit value times power of base
        number += digit_value * power
        # Multiply power by base to increment exponent by one
        power *= base
    return number


def decode_solution_4(digits, base):
    """Solution 4: Start decoding leftmost digit and shift number left.
    Running time: O(n) where n is number of digits in given string (length).
    Faster than Solutions 1 & 2 because it avoids exponentiation operation and
    only slow operation used is multiplication, which is still much faster."""
    number = 0
    # Loop over digits
    for digit in digits:  # Always n iterations
        # Find numerical value of next leftmost digit
        digit_value = value_of_char(digit)
        assert 0 <= digit_value < base
        # Multiply by one power of base to shift number left one 'digit'
        # After this, all 'digits' in number now represent larger values
        number *= base
        # Add this digit value (now least significant 'digit' of number)
        number += digit_value
        # Equivalently, in one assignment expression
        # number = (number * base) + digit_value
    return number


def decode_recursive(digits, base):
    """Solution 5: Decode rightmost digit and then recursively decode the rest.
    Running time: O(n) where n is number of digits in given string (length).
    Faster than Solutions 1 & 2 because it avoids exponentiation operation and
    only slow operation used is multiplication, which is still much faster."""
    # Check if there are no digits to decode (base case)
    if len(digits) < 1:
        return 0
    # Find numerical value of next rightmost digit
    digit_value = value_of_char(digits[-1])
    assert 0 <= digit_value < base
    # If there's only one digit, return its value (base case)
    if len(digits) == 1:
        return digit_value
    # Otherwise, there are multiple digits to decode (recursive case)
    assert len(digits) > 1
    # Call decode recursively on rest and add digit value onto right side
    number = decode_recursive(digits[:-1], base)
    # Multiply by one power of base to shift number left one 'digit'
    # After this, all 'digits' in number now represent larger values
    number *= base
    # Add this digit value (now least significant 'digit' of number)
    number += digit_value
    # Equivalently, in one assignment expression
    # number = (number * base) + digit_value
    return number


def decode_cheating(digits, base):
    """Solution 6: Cast string of digits to int type and use base parameter.
    Cheating a bit on this challenge, but it's simple, robust, and built-in."""
    return int(digits, base)


def encode(number, base):
    """Encode given number in base 10 to digits in given base.
    number: int -- integer representation of number (in base 10)
    base: int -- base to convert to
    return: str -- string representation of number (in given base)"""
    # Handle up to base 36 [0-9a-z]
    assert 2 <= base <= 36, 'base is out of range: {}'.format(base)
    # Handle unsigned numbers only for now
    assert number >= 0, 'number is negative: {}'.format(number)
    # Handle zero as special case to avoid returning empty string
    if number == 0:
        return '0'

    # Call encode functions for all solutions
    digits_1 = encode_solution_1(number, base)
    digits_2 = encode_solution_2(number, base)
    digits_3 = encode_recursive(number, base)
    # if base in (2, 8, 10, 16):
    digits_4 = encode_cheating(number, base)
    # All results should match
    assert digits_1 == digits_2
    assert digits_2 == digits_3
    if digits_4:
        assert digits_2 == digits_4
    return digits_2


def encode_solution_1(number, base):
    """Solution 1: Start encoding leftmost digit and count exponents down.
    Running time: O(n^2) where n is number of digits in string result (length).
    Although it has only one loop, it uses slow exponentiation operation that
    takes O(exponent) time, which is worst case O(n) time at start of loop."""
    digits1 = ''
    # Find maximum power of base for leftmost digit
    max_exponent = 0
    while base ** max_exponent <= number:
        max_exponent += 1
    # We went one exponent too far, so come back down one
    max_exponent -= 1
    # Alternative: calculate how many digits it take to encode number in base
    # import math
    # max_exponent2 = math.floor(math.log(number, base))
    # assert max_exponent == max_exponent2

    # Rename variable for clarity and to avoid destroying value of argument
    remainder = number
    # Loop exponents from max_exponent down to 0
    for exponent in range(max_exponent, -1, -1):
        # Calculate power of base for this exponent (DRY: reused twice below)
        power = (base ** exponent)  # Worst case O(n) time
        # Calculate value of next leftmost digit
        # This is how many multiples of this power of base we need
        digit_value = remainder // power  # See divmod operation below
        # Alternative: calculate quotient and remainder in one operation
        # digit_value, remainder = divmod(remainder, power)
        assert 0 <= digit_value < base
        # Find character to represent next leftmost digit
        character = char_for_value(digit_value)
        # Append next digit onto *right* side of previous digits
        digits1 = digits1 + character
        # Subtract off total value of this digit
        remainder = remainder - digit_value * power
        # Alternative: take modulus of this power of base
        # remainder = remainder % power  # See divmod operation above
    return digits1


def encode_solution_2(number, base):
    """Solution 2: Start encoding rightmost digit and shift number right.
    Running time: O(n) where n is number of digits in string result (length).
    Faster than Solution 1 above because it avoids exponentiation operation and
    only slow operations are division and modulus but can be done in one op."""
    digits2 = ''
    # Rename variable for clarity and to avoid destroying value of argument
    quotient = number
    # Loop until we shift number all the way right (divide until it's zero)
    while quotient > 0:
        # Calculate value of next rightmost digit
        # This is how many multiples of this power of base we need
        digit_value = quotient % base  # See divmod operation below
        # Alternative: calculate quotient and remainder in one operation
        # quotient, digit_value = divmod(quotient, base)
        assert 0 <= digit_value < base
        # Find character to represent next rightmost digit
        character = char_for_value(digit_value)
        # Prepend next digit onto *left* side of previous digits
        digits2 = character + digits2
        # Divide by base to shift off value of completed digit
        quotient = quotient // base  # See divmod operation above
    return digits2


def encode_recursive(number, base):
    """Solution 3: Encode rightmost digit and then recursively encode the rest.
    Running time: O(n) where n is number of digits in string result (length).
    Faster than Solution 1 above because it avoids exponentiation operation and
    only slow operations are division and modulus but can be done in one op."""
    # Calculate value of rightmost digit
    # This is how many multiples of this power of base we need
    digit_value = number % base  # See divmod operation below
    # Alternative: calculate quotient and remainder in one operation
    # quotient, digit_value = divmod(number, base)
    assert 0 <= digit_value < base
    # Find character to represent rightmost digit
    character = char_for_value(digit_value)
    # Divide by base to shift off value of completed digit
    quotient = number // base  # See divmod operation above
    # Check if there's a quotient left (recursive case)
    if quotient > 0:
        # Call encode recursively on quotient and append digit onto right side
        return encode_recursive(quotient, base) + character
    # Otherwise we encoded the only digit (base case)
    return character


def encode_cheating(number, base):
    """Solution 4: Use string formatting function and integer base parameter.
    Cheating on this challenge as well, but it's simple enough and it works."""
    base_format = {2: 'b', 8: 'o', 10: 'd', 16: 'x'}
    if base in base_format:
        return format(number, base_format[base])


def convert(digits, base1, base2):
    """Convert given digits in base1 to digits in base2.
    digits: str -- string representation of number (in base1)
    base1: int -- base of given number
    base2: int -- base to convert to
    return: str -- string representation of number (in base2)"""
    # Handle up to base 36 [0-9a-z]
    assert 2 <= base1 <= 36, 'base1 is out of range: {}'.format(base1)
    assert 2 <= base2 <= 36, 'base2 is out of range: {}'.format(base2)

    """Solution: This is much easier than you might have originally thought."""
    # Decode digits in base1 into a number
    number = decode(digits, base1)
    # Encode number into digits in base2
    return encode(number, base2)


def main():
    """Read command-line arguments and convert given digits between bases."""
    import sys
    args = sys.argv[1:]  # Ignore script file name
    if len(args) == 3:
        digits = args[0]
        base1 = int(args[1])
        base2 = int(args[2])
        # Convert given digits between bases
        result = convert(digits, base1, base2)
        print('{} in base {} is {} in base {}'.format(digits, base1, result, base2))
    else:
        print('Usage: {} digits base1 base2'.format(sys.argv[0]))
        print('Converts digits from base1 to base2')


if __name__ == '__main__':
    main()
