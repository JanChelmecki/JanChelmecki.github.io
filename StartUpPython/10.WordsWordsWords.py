sentence = input("Input a sentence: ")
words = 1
for i in range(len(sentence)):
    if sentence[i]==" ":
        words+=1
print("There are", words, "words.")