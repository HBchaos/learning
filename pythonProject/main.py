n=10
res = []
i=2
while n:
    for j in range(2,i):
        if i%j==0:
            break
    else:
        res.append(i)
        n-=1
    i+=1
print(res)
