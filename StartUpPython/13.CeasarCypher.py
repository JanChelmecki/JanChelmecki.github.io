message = input("Write anything: ")
offset = int(input("Offset: "))

newmessage = ""

for character in message:
    ordinal = ord(character)
    if 97<=ordinal<=122: #lowercase letters
        newmessage += chr(97+(ordinal-97+offset)%26)
    elif 65<=ordinal<=90: #capital letters
        newmessage += chr(65+(ordinal-65+offset)%26)
    else:
        newmessage += character
    
print(newmessage)

## ACS - Very good