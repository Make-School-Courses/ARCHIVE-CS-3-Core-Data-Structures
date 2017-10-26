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
    # List of characters to represent digits up to base 36 [0-9a-z]
    characters = string.digits + string.ascii_lowercase

    # Solution 1: Start decoding rightmost digit and count powers up
    number1 = 0
    for power, digit in enumerate(reversed(digits)):
        # Decode next rightmost digit into a number
        assert digit in characters, 'no character for digit: {}'.format(digit)
        digit_value = characters.index(digit)
        assert 0 <= digit_value < base
        # Add this digit value times this power of base
        number1 += digit_value * (base ** power)

    # Solution 2: Start decoding leftmost digit and count powers down
    number2 = 0
    max_power = len(digits) - 1
    for iteration, digit in enumerate(digits):
        # Decode next leftmost digit into a number
        assert digit in characters, 'no character for digit: {}'.format(digit)
        digit_value = characters.index(digit)
        assert 0 <= digit_value < base
        # Calculate actual power of base
        power = max_power - iteration
        # Add this digit value times this power of base
        number2 += digit_value * (base ** power)

    # Solution 3: Start decoding leftmost digit and shift number left
    number3 = 0
    for digit in digits:
        # Decode next leftmost digit into a number
        digit_value = characters.index(digit)
        assert 0 <= digit_value < base
        # Shift number left one power of base
        number3 *= base
        # Now add this digit value
        number3 += digit_value
        # Equivalently, in one expression:
        # number3 = (number3 * base) + digit_value

    # Solution 4: Cast string to int type (cheating)
    number4 = int(digits, base)
    assert number1 == number2
    assert number2 == number3
    assert number3 == number4
    return number3


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
    # List of characters to represent digits up to base 36 [0-9a-z]
    characters = string.digits + string.ascii_lowercase

    # Solution 1: Start encoding leftmost digit and count powers down
    digits1 = ''
    # Find the maximum base power for leftmost digit
    max_power = 0
    while base ** max_power < number:
        max_power += 1
    remainder = number
    # Loop base powers from max_power down to 0
    for power in range(max_power, -1, -1):
        # Get value of next leftmost digit
        # (Calculate how many multiples of this base power we need)
        digit_value = remainder // (base ** power)
        assert 0 <= digit_value < base
        # Get character to represent next leftmost digit
        character = characters[digit_value]
        # Append next digit onto right side of previous digits
        digits1 = digits1 + character
        # Subtract/modulus off value of completed digit
        # remainder -= digit_value * (base ** power)
        remainder = remainder % (base ** power)
        # Equivalently, in one function call:
        # digit_value, remainder = divmod(remainder, base ** power)
    # Strip any leading zeros from the result
    digits1 = digits1.lstrip('0')

    # Solution 2: Start encoding rightmost digit and shift number right
    digits2 = ''
    # Loop until we shift number all the way to the right
    quotient = number
    while quotient > 0:
        # Get value of next rightmost digit in base range
        digit_value = quotient % base
        assert 0 <= digit_value < base
        # Get character to represent next rightmost digit
        character = characters[digit_value]
        # Prepend next digit onto left side of previous digits
        digits2 = character + digits2
        # Divide by base to shift off value of completed digit
        quotient = quotient // base
        # Equivalently, in one function call:
        # quotient, digit_value = divmod(quotient, base)
    assert digits1 == digits2
    return digits2


def convert(digits, base1, base2):
    """Convert given digits in base1 to digits in base2.
    digits: str -- string representation of number (in base1)
    base1: int -- base of given number
    base2: int -- base to convert to
    return: str -- string representation of number (in base2)"""
    # Handle up to base 36 [0-9a-z]
    assert 2 <= base1 <= 36, 'base1 is out of range: {}'.format(base1)
    assert 2 <= base2 <= 36, 'base2 is out of range: {}'.format(base2)
    # Solution: This is much easier than you think...
    # First, decode the digits in base1 into a number
    number = decode(digits, base1)
    # Then, encode the number into digits in base2
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
