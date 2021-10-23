list1 = [2,5,15,36,47,56,59,78,156,244,268]
list2 = [18,39,42,43,66,69,100]
List = []

index1 = 0
index2 = 0

while index1<len(list1) and index2<len(list2):
    if list1[index1]<=list2[index2]:
        List.append(list1[index1])
        index1 += 1
    else:
        List.append(list2[index2])
        index2 += 1

while index1<len(list1):
    List.append(list1[index1])
    index1+=1

while index2<len(list2):
    List.append(list2[index2])
    index2+=1

print(List)