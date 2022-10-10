outLinks = {"A":["B", "C"], "B":["C"], "C":["A"], "D":["C"]}
pages = outLinks.keys()
totalOut = {}
for page in pages:
    totalOut[page] = len(outLinks[page])

inLinks = {}
for page in pages:
    inLinks[page] = []

for page in pages:
    for p in outLinks[page]:
        inLinks[p].append(page)



iterations = 2000
PR = {}
for page in pages: #initialize page rank values
    PR[page] = 1
PR_new = {}
d = 0.85

for iteration in range(iterations):
    for page in pages: #compute new page rank
        sum = 0
        for p in inLinks[page]:
            sum += PR[p]/totalOut[p]
        PR_new[page] = 1-d + d*sum

    for page in pages: #update page rank values
        PR[page] = PR_new[page]
#next iteration

for page in pages:
    print("PR["+page+"] = ", PR[page])