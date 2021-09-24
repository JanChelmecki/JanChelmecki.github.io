Letters = input("Program displays all anagrams of a given word: ") #This is obviously equivalent to the PIN task.
Anagrams = {Letters[0]}
"""
Anagrams is the set of all combinations with available letters 
(currently just one, we will add them one by one later on).
"""

for n in range(1,len(Letters)):
    """
    In each step, we add a new available letter. It can be inserted 
    in n+1 positions (as every word in Anagrams is of length n), 
    making potentialy (if there are no duplicates) n+1 new words
    out of each of the words in Anagrams. 
    
    Anagrams being a set provides that there are no duplicates in any stage of the construction,
    greatly reducing the number of new words to add letters to (which normaly grows as n!)
    """
    Anagrams = {word[:i:]+Letters[n]+word[i::] for i in range(n+1) for word in Anagrams}

#displaying part
for word in Anagrams:
    print(word)