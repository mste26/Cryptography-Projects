# Made to decrypt text via an Affine Cipher: y = 3x + 22 % 26
ctext = "BRIZMNUYZQBRIKUJFGUDD"

def convert(s):
     x = ord(s) - ord('A')
     return x

def dec(s):
     x = (int(A) * s + B) % 26
     return chr(x + ord('A'))

def euclidsP1(a,m):
     x = 1
     while m >= a*x:
        x += 1
     x -= 1 # account for last iteration

     b = m-(a*x)
     print(m, "=", a, "*", x, "+", b)
     d[b] = [a,x,m]
     s.append(b)

     if b == 1:
        return
     elif b == 0:
        print("err")
     else: 
          euclidsP1(b, a)

def euclidsP2():
    a = 1
    m = 0

    for i in reversed(s):
        x = d[i][1]
        temp = m
        m = a
        a = temp - (x * a)
    return a

d = {}
s = []

A = 3
B = 22
M = 26

euclidsP1(A, M)
x = euclidsP2()

A = x / (A * x % M) % M
B = 0 - (B * x % M) % M



for i in [convert(i) for i in ctext]:
    print(dec(i), end=" ")

