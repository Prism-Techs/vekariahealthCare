def palindrome(n):
    """
    Determines if a given integer is a palindrome.

    Args:
        n (int): The integer to be checked.

    Returns:
        bool: True if the integer is a palindrome, False otherwise.
    """
    # Convert the integer to a string for easier manipulation
    n = str(n)
    # Check if the string is equal to its reverse
    return n == n[::-1]