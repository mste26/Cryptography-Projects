# Made to decrypt text via Vigenere Cipher
import numpy as np
str = "LZNEZYEQGTKBMVUOJVRUNVBFTTHIKRDUUKHFOETFXJEDZZOOUWFJLKHBTUEJMYTIYKRFKKAOJXEUOETPZYECRLEMKOUTGEDBYBFPXTHBXCET"

# count frequency of each letter
def frequency(str):
    def f(s):
        x = ord(s) - ord('A')
        return x
    Af = [0 for i in range(26)]
    A = [i for i in str]
    for i in A:
        Af[f(i)] += 1
    return Af

# count coincedences for up to 6 shifts
def shiftlen(str):
    coinc = [0 for i in range(6)]
    A = [i for i in str]
    for i in range(6):
        for j in range(len(A)):
            if j+1+i < len(A):
                if ord(A[j]) == ord(A[j+1+i]):
                    coinc[i] += 1
    x = 0
    for i in range(len(coinc)):
        if coinc[i] == max(coinc):
            x = i+1
            break
    return x
    
# returns a frequency array
def getfreq(str, ln):
    def shift(V):
        Vn = [V[i - 1] if i > 0 else V[len(V) - 1] for i in range(len(V))]
        return Vn

    V = [.082, .015, .028, .043, .127, .022, .02, .061, .07, .002,
         .008, .04, .024, .067, .075, .019, .001, .06, .063, .091,
         .028, .01, .023, .001, .02, .001]
    U = [i/ln for i in str[0]]
    shft = 0
    max = 0
    for i in range(26):
        if max < np.dot(U,V):
            max = np.dot(U,V)
            shft = i
        V = shift(V)
    return shft

# divides a string in by its key character
def divstr(str, klen):
    A = [[] for _ in range(klen)]
    idx = 0
    for i in str:
        A[idx].append(i)
        if idx < klen - 1:
            idx += 1
        else:
            idx = 0
    return A

# takes a string and key and decrypts
def decrypt(str, key):
    A = [ord(i) - ord('A') for i in str]
    idx = 0
    for i in range(len(A)):
        A[i] = A[i] - key[idx]
        if A[i] < 0:
            A[i] += 26
        if idx < (len(key) - 1):
            idx += 1
        else:
            idx = 0
    At = [chr(i + ord('A')) for i in A]
    return At 

klen = shiftlen(str)
#klen = 4
As = divstr(str, klen)
Af = [[frequency(As[i])] for i in range(klen)]
key = []
for i in range(klen):
    key.append(getfreq(Af[i], len(Af[i])))
print("key:", "".join([chr(i + ord('A')) for i in key]))
print("plaintext:", "".join(decrypt(str, key)))