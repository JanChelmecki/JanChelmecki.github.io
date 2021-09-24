text = input("Type anything: ")
textrev = text[::-1]
print(textrev)

def simplify(text):
    """
    Function deletes non-letter characters and changes every letter to lowercase.
    This way, we can see that "Rise to vote, sir!" is indeed a palindrome.
    """
    simplified = ""
    for char in text:
        o = ord(char)
        if 65<=o<=90: #capital letter
            simplified += chr(o+32)
        elif 97<=o<=122: #lowercase letter
            simplified += char
    return simplified

if simplify(text)==simplify(textrev):
    print(text, "is a palindrome.")

    ## ACS - Well done