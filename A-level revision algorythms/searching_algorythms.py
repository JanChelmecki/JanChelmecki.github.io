def linear_search(list, item):
    index = 0
    found = False
    while not found and index<len(list):
        if list[index] == item:
            found = True
        else:
            index += 1
    if found:
        return index
    else:
        return False

#print(linear_search([1,3,4,5,6], 6))

def binary_search(list, item):

    start = 0
    end = len(list)-1
    found = False

    while not found and start<=end:
        midpoint = start+(end-start)//2
        if item < list[midpoint]:
            end = midpoint-1
        elif item > list[midpoint]:        
            start = midpoint+1
        else:
            found = True
    
    if found:
        return midpoint
    else:
        return False

print(binary_search([1,3,5,7,9], -1))

        
