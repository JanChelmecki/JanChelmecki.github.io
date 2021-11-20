import timeit, random

def bauble_sort(L):
    route = 0
    done = False
    while not done:
        done = True
        index = 0
        while index + route + 1 < len(L):
            nextindex = index + 1
            if L[index] > L[nextindex]:
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
        while space>= 0 and L[space]>item:
            L[space+1] = L[space]
            space -= 1
        L[space+1] = item
    return L

def merge_lists(L1, L2):
    index1 = 0
    index2 = 0
    L = []
    while index1 < len(L1) and index2 < len(L2):
        if L1[index1]<L2[index2]:
            L.append(L1[index1])
            index1 += 1
        else:
            L.append(L2[index2])
            index2 += 1
    while index1 < len(L1):
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
    if len(L) == 0 or len(L) == 1:
        return L
    else:
        pivot = L[random.randint(0,len(L)-1)]
        return quick_sort([l for l in L if l<pivot]) + [pivot]*L.count(pivot) + quick_sort([l for l in L if l>pivot])


def test(length, trials):
    """
    Uses the build-in sort function to test a sorting algorythm
    """
    success = True
    trial = 0
    while success and trial < trials:
        L = [random.randint(0, 10*length) for i in range(length)]
        L1 = quick_sort(L)
        L2 = L; L2.sort()
        if L1 != L2:
            success = False
            print("Failed for", L)
            print("Your sort:", L1)
            print("Correct answer:", L2)
        trial += 1
    if success:
        print("Test OK")


L = [5,4,3,2,1]
time = timeit.timeit(setup = "from __main__ import merge_sort, merge_lists", stmt = "merge_sort(L)", number = 10, globals = {"L":"L"})