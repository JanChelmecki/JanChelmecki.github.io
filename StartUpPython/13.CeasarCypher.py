message = input("Write anything: ")
offset = input("Offset: ")

for character in message:
    ordinal = ord(character)
    if 97<=ordinal<=122: #lowercase letters
        character = chr(97+(ordinal-97+offset)%26)
    elif 65<=ordinal<=90: #capital letters
        character = chr(65+(ordinal-65+offset)%26)
    else:
        pass
    
print(message)