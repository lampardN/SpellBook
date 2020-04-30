n = int(input())
a = [int(input()) for i in range(n)]
count = 0
for i in range(n-5):
    for j in range(i+5, n):
        if (a[i] + a[j]) % 2 == 1 and (a[i]*a[j]) % 13 == 0:
            count += 1
print(count)
