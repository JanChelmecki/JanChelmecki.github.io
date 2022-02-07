import random

def bauble_sort(L):
    route = 0
    done = False
    while not done:
        done = True
        index = 0
        while index + route + 1 < len(L):
            nextindex = index + 1
            if L[index] > L[nextindex]: #swap, if in wrong order
                temp = L[index]
                L[index] = L[nextindex]
                L[nextindex] = temp
                done = False
            index = nextindex
        route += 1
    return L

def insertion_sort(L):
    for index in range(1, len(L)): #list is all sorted before index, we need to insert L[index] in the right place
        item = L[index]
        space = index - 1
        while space>= 0 and L[space]>item: #keep going left until you find the right spot
            L[space+1] = L[space] #shift the current element one space right
            space -= 1
        L[space+1] = item
    return L

def merge_lists(L1, L2):
    #merges two sorted lists into one sorted list
    index1 = 0
    index2 = 0
    L = []
    while index1 < len(L1) and index2 < len(L2):
        """
        Choose smaller from the first elements of the two lists and move up one space in
        the list you chose item from. Do this until you run out of elements in a list.
        """
        if L1[index1]<L2[index2]:
            L.append(L1[index1])
            index1 += 1
        else:
            L.append(L2[index2])
            index2 += 1
    while index1 < len(L1): #add what's left from L1
        L.append(L1[index1])
        index1 += 1
    while index2 < len(L2):
        L.append(L2[index2])
        index2 += 1
    return L
    
def merge_sort(L):
    if len(L) == 1 or len(L)==0:
        return L
    else:
        return merge_lists(merge_sort(L[:len(L)//2:]), merge_sort(L[len(L)//2::]))

def quick_sort(L):
    if len(L)<=1:
        return L
    stack = [(0, len(L)-1)]
    while stack != []:
        (start, end) = stack.pop()        
        pivot = start
        left = start + 1
        right = end
        swap = True
        while swap:
            swap = False
            while L[left]<=L[pivot] and left<end:
                left+=1
            while L[right]>=L[pivot] and right>start:
                right-=1
            if left<right:
                temp = L[left]
                L[left] = L[right]
                L[right] = temp
                swap = True
        temp = L[pivot]
        L[pivot] = L[right]
        L[right] = temp
        if start< right:
            stack.append((start, right))
        if left<end:
            stack.append((left, end))
    return L

L = [34, 56, 23, 81, 28, 66, 35, 17, 88, 37, 18, 50]
print(quick_sort(L.copy()))
print(L)


def test(length, trials):
    
    #Uses the build-in sort function to test a sorting algorythm
    
    success = True
    trial = 0
    while success and trial < trials:
        L = [random.randint(0, 10*length) for i in range(length)]
        L1 = quick_sort(L.copy())
        L2 = L.copy(); L2.sort()
        if L1 != L2:
            success = False
            print("Failed for", L)
            print("Your sort:", L1)
            print("Correct answer:", L2)
        trial += 1
    if success:
        print("Test OK")

test(13, 10)