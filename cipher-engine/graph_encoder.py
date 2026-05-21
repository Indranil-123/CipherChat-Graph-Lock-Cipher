import json
import base64
from modular_math import mod_inverse, mod_multiply, generate_large_prime


ASCII_MAX = 256

def text_to_nodes(text, max_len=None):
    
    # Convert each character to its ASCII number
    # ord('H') gives the ASCII value of 'H' → 72
    nodes = [ord(char) for char in text]
    
    # If max_len is given, pad with zeros to reach that length
    # This makes sure our matrix is always n×n
    if max_len is not None:
        while len(nodes) < max_len:
            nodes.append(0)
        nodes = nodes[:max_len]
        
    return nodes
    

def nodes_to_text(nodes):
    
    while nodes and nodes[-1] == 0:
        nodes.pop()  # Remove trailing zeros
        
    return ''.join(chr(n) for n in nodes if 0 < n < ASCII_MAX)


def build_adjacency_matrix(nodes, prime):
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i ==j:
                matrix[i][j] = 1  # Self-loop
            else:
                weight = (nodes[i] + nodes[j]) % prime
                matrix[i][j] = weight
    return matrix


# WHAT IS THIS?
#   After building the adjacency matrix, we apply one more
#   scrambling step: multiply every cell by a "scramble factor"
#   using modular arithmetic.
#
# WHY?
#   The adjacency matrix alone is reversible if you know the formula.
#   Multiplying by a secret factor (derived from the prime) makes
#   it much harder to work backwards without the key.
#
# THE SCRAMBLE FACTOR:
#   factor = (prime - 1) // 2
#   This gives a number roughly half the prime.
#   It's derived from the prime itself, so the recipient
#   can compute it too — they just need the prime (the key).
#
# REVERSING IT (decryption):
#   To undo the multiplication, multiply by the modular inverse
#   of the factor. That's why mod_inverse exists!