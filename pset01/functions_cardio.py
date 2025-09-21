def print_square(n):
    for _ in range(n):
        print('*' * n)


def is_odd(n):
    return n % 2 != 0


def median_of_three(a, b, c):
    if (a <= b <= c) or (c <= b <= a):
        return b
    elif (b <= a <= c) or (c <= a <= b):
        return a
    else:
        return c


def is_palindrome(s):
    left = 0
    right = len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def count_of_latin_vowels(s):
    vowels = "aeiou"
    count = 0
    for char in s.lower():
        if char in vowels:
            count += 1
    return count


def at_beginning_or_end(part, whole):
    return whole.startswith(part) or whole.endswith(part)


def longest_string(strings):
    longest = ""
    for s in strings:
        if len(s) > len(longest):
            longest = s
    return longest


def collatz(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def test_print_square():
    import io
    import contextlib
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_square(2)
    assert f.getvalue() == "**\n**\n"
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_square(5)
    assert f.getvalue() == "*****\n*****\n*****\n*****\n*****\n"
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_square(1)
    assert f.getvalue() == "*\n"
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_square(0)
    assert f.getvalue() == ""


def test_is_odd():
    assert is_odd(3) is True
    assert is_odd(8) is False
    assert is_odd(-3) is True
    assert is_odd(-8) is False


def test_median_of_three():
    assert median_of_three(1, 2, 3) == 2
    assert median_of_three(10, 30, 20) == 20
    assert median_of_three(25, 15, 35) == 25
    assert median_of_three(900, 9999, -1050) == 900
    assert median_of_three(193, 191, 192.5) == 192.5
    assert median_of_three(99999, 0, -1000) == 0


def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(6) == 720
    assert factorial(20) == 2432902008176640000


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("madam") is True
    assert is_palindrome("python") is False


def test_count_of_latin_vowels():
    assert count_of_latin_vowels("hello world") == 3
    assert count_of_latin_vowels("aeiou") == 5
    assert count_of_latin_vowels("xyz") == 0
    assert count_of_latin_vowels("Python programming") == 4
    assert count_of_latin_vowels("Aeiou") == 5


def test_at_beginning_or_end():
    assert at_beginning_or_end("pre", "prefix") is True
    assert at_beginning_or_end("fix", "suffix") is True
    assert at_beginning_or_end("middle", "start middle end") is False
    assert at_beginning_or_end("dog", "doghouse") is True
    assert at_beginning_or_end("doghouse", "dog") is False
    assert at_beginning_or_end("cat", "dog") is False
    assert at_beginning_or_end("", "anything") is True


def test_longest_string():
    assert longest_string(["apple", "banana", "cherry"]) == "banana"
    assert longest_string(["cat", "dog", "elephant"]) == "elephant"
    assert longest_string(["short", "longer", "longest"]) == "longest"
    assert longest_string(["a", "ab", "abc"]) == "abc"
    assert longest_string(["one", "two", "three", "four"]) == "three"


def test_collatz():
    assert collatz(1) == [1]
    assert collatz(2) == [2, 1]
    assert collatz(3) == [3, 10, 5, 16, 8, 4, 2, 1]
    assert collatz(4) == [4, 2, 1]
    assert collatz(5) == [5, 16, 8, 4, 2, 1]
    assert collatz(15) == [
        15, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1
    ]


test_print_square()
test_is_odd()
test_median_of_three()
test_factorial()
test_is_palindrome()
test_count_of_latin_vowels()
test_at_beginning_or_end()
test_longest_string()
test_collatz()
print("All tests passed!")
