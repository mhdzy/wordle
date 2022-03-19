
outputs: list = []

def kLengthRec(set, prefix, n, k):
    global outputs
    
    if (k == 0):
        outputs.append(prefix)
        return
 
    for i in range(n):
        newPrefix = prefix + set[i]
        kLengthRec(set, newPrefix, n, k - 1)

def kLength(set, k):
    kLengthRec(set, "", len(set), k)

# stores results in 'outputs'
kLength(['0', '1', '2'], k = 5)
