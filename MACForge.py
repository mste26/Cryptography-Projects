"""
This script implements forgery attacks against a custom Grid-based Message Authentication Code (MAC)
and a Merkle-Damgard Hash-and-MAC protocol.

The attacks exploit the linear structure of the MAC definitions:
    s = sum(k[i, n] for i in 0..m)
    t = sum(k[m, j] for j in 0..n)

Functions:
- selective_forge: Performs an existential forgery by deriving the tag for (0,0) using a single query to (1,0).
- universal_forge: Performs a universal forgery for any target message (m,n). It handles boundary conditions 
  (axes vs. interior) to algebraically isolate specific row/column sums using differential queries.
- md_forge: Exploits the compression function in the Hash-and-MAC protocol to produce a valid collision.
"""

def selective_forge(MAC): 
    s0,t0 = MAC((1,0))
    # s0 = [0][0] + [1][0]
    # t0 = [1][0]
    # t1 - t2 = [1][1] --> s1 - (t1 - t2) = [0][1]
    # s2 - t2 = [0][0] --> (s2 - t2) + s = [0][0] + [0][1]
    
    s = s0 - t0
    t = s

    # s, t = query_tag 
    # # s = 76 = key[0][4] + key[1][4] + key[2][4] + key[3][4] 
    # # t = 160 = key[3][0] + key[3][1] + key[3][2] + key[3][3] + key[3][4]
   
    forged_msg = (0, 0) 
    # s = [0][1] 
    # t = [0][0] + [0][1]
    forged_tag = (s, t) 
    return (forged_msg, forged_tag)

def universal_forge(MAC, msg):
    m,n = msg
    if (msg == (0,0)):
        s0,t0 = MAC((0,1))
        t = s = (t0 - s0)
    elif (msg == (0,n)):
        if(n < 15):
            s1,t1 = MAC((0,n+1))
            t = (t1 - s1)
            s2,t2 = MAC((0,n-1))
            s = (t - t2)
        else:
            s1,t1 = MAC((1,n))
            s2,t2 = MAC((1,n-1))
            s3,t3 = MAC((0,n-1))
            s = (s1 - (t1 - t2))
            t = t3 + (s1 - (t1 - t2))

    elif (msg == (m,0)):
        if (m < 15):
            s1,t1 = MAC((m+1,0))
            s = (s1 - t1)
            s2,t2 = MAC((m-1,0))
            t = (s - s2)
        else:
            s1,t1 = MAC((m,1))
            s2,t2 = MAC((m-1,1))
            s3,t3 = MAC((m-1,0))
            t = (t1 - (s1 - s2))
            s = s3 + (t1 - (s1 - s2))
            
    else:
        if (m < 15 & n < 15):
            s1,t1 = MAC((m+1,n))
            s2,t2 = MAC((m+1,n-1))
            s3,t3 = MAC((m,n+1))
            s4,t4 = MAC((m-1,n+1))
            s = s1 - (t1 - t2)
            t = t3 - (s3 - s4)
        elif (m < 15):
            s1,t1 = MAC((m+1,n))
            s2,t2 = MAC((m+1,n-1))
            s3,t3 = MAC((m,n-1))
            s4,t4 = MAC((m-1,n))
            s = s1 - (t1 - t2)
            t = t3 + (s - s4)
        elif (n < 15):
            s1,t1 = MAC((m, n+1)) # 58
            s2,t2 = MAC((m-1, n+1)) # 48
            s3,t3 = MAC((m-1, n)) #47
            s4,t4 = MAC((m, n-1)) #56
            t = t1 - (s1 - s2)
            s = s3 + (t - t4)
        
    forged_tag = (s, t)
    return forged_tag

def md_forge(MD):
    query_hashtag = MD([5,1,1,1,1]) 
    forged_msg = [5,4,3,2,1]
    forged_hashtag = query_hashtag
    return (forged_msg, forged_hashtag)   