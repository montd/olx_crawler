def merge_the_tools(string, k):
    n = len(string)
    print(n)
    sub = []
    i = 0
    while (i<n):
        sub.append(string[i:i+k])
        i+=k
        print(i)
    print(list(sub))
    i = 0
    subsub = sub[:]
    while (i<k):
        subsub[i] = [i for i in sub[i]]
        i+=1
    print(set(subsub))



if __name__ == '__main__':
    merge_the_tools("AABCAAADA",3)