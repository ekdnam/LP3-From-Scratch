import random

random.seed(42)

ip = [] # 8
ip_inv = [] # 8
ep = [] # 8
p10 = [] # 10
p8 = [] # 8

def generate_random_permutation(n: int):
    out = [i+1 for i in range(n)]
    random.shuffle(out)
    return out

p10 = generate_random_permutation(10)
p8 = random.sample(generate_random_permutation(10), 8)
ep = generate_random_permutation(4)*2
ip = generate_random_permutation(8)
ip_inv = [1]*8

for i in range(len(ip)):
    ip_inv[ip[i]-1] = i+1

# Helpers
def bin_to_dec(x):
    return int(x, 2)

def dec_to_bin(x):
    return bin(x).replace('0b', '')

def split_str(text):
    mid = len(text)//2
    return text[:mid], text[mid:]

def left_circular_shift(x, shifts=1):
    shifts = shifts % len(x)
    return x[shifts:] + x[:shifts]

def permutate(key, perm):
    print('@key: ', key)
    print('@perm: ', perm)
    ret = ""
    for k in perm:
        ret += key[k-1]
    return ret

def xor(a, b):
    ret = []
    for i in range(len(a)):
        if a[i] == b[i]: ret.append('0')
        else: ret.append('1')
    return ''.join(ret)

s0 = [
    [1, 0, 3, 2], 
    [3, 2, 1, 0], 
    [0, 2, 1, 3], 
    [3, 1, 3, 0]
]

s1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

def gen_subkeys(key):
    new_key = permutate(key,p10)
    
    left_key, right_key = split_str(new_key)
    
    left_key = left_circular_shift(left_key, 1) 
    right_key = left_circular_shift(right_key, 1) 
    
    k1 = permutate(left_key + right_key, p8)
    
    left_key = left_circular_shift(left_key, 2) 
    right_key = left_circular_shift(right_key, 2)
    
    k2 = permutate(left_key + right_key, p8)
    
    return k1, k2

def foo_s_box(text, sbox):
    r = text[0] + text[3]
    c = text[1] + text[2]
    
    r = bin_to_dec(r)
    c = bin_to_dec(c)
    
    out = sbox[r][c]
    
    out = dec_to_bin(out)
    
    while len(out) < 2:
        out = '0' + out
    return out

def fk(left, right, subkey):
    text = right
    text = permutate(text, ep)
    text = xor(text, subkey)
    text_left, text_right = split_str(text)
    text = foo_s_box(text_left, s0) + foo_s_box(text_right, s1)
    text = xor(text, right)
    return text, right

def encryption(plaintext, key):
    k1, k2 = gen_subkeys(key)
    
    ciphertext = permutate(plaintext, ip)
    
    left, right = split_str(ciphertext)
    left, right = fk(left, right, k1)
    
    left, right = right, left
    
    left, right = fk(left, right, k2)
    
    ciphertext = permutate(left+right, ip_inv)
    
    return ciphertext
    
def decryption(ciphertext, key):
    k1, k2 = gen_subkeys(key)
    
    plaintext = permutate(ciphertext, ip)
    
    left, right = split_str(plaintext)
    left, right = fk(left, right, k2)
    
    right, left = left, right
    
    left, right = fk(left, right, k1)
    
    plaintext = permutate(left+right, ip_inv)
    
    return ciphertext

key = "1010001011"
plaintext = "10001010"

# k1, k2 = gen_subkeys(key)
c = encryption(plaintext, key)
p = decryption(c, key)

# print(p)
# print(plaintext)
    