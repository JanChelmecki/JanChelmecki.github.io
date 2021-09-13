sentence = input("Input a sentence: ")
words = 1
for char in sentence:
    if char==" ":
        words+=1
print("There are", words, "words.")