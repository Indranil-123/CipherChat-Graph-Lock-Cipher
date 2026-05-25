#this code is Basically the heart of the GraphCipher

import json
import base64
from modular_math import mod_multiply, mod_inverse, generate_large_prime



#I have to define a Constant value for ashcii

ASCII_MAX = 256

#first function Text to nodes

def text_to_nodes(text,max_len=None):
    
    nodes = [ord(char) for char in text]
    
    if max_len is not None:
        while len(nodes) <max_len:
            nodes.append(0)
        nodes = nodes[:max_len]
        
    return nodes

#second function Nodes to text
def nodes_to_text(nodes):
    while nodes and nodes[-1] == 0:
        nodes.pop()
        
    return ''.join(chr(n) for n in nodes if 0 < n < ASCII_MAX)


#function 3 for building adjancency matrix

def build_adjacency_matrix(nodes, prime):
    
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):

            # Diagonal stays zero — no self-edges
            if i == j:
                matrix[i][j] = 0

            else:
                weight = (nodes[i] + nodes[j] + i + j) % prime
                matrix[i][j] = weight

    return matrix


def apply_prime_field(matrix, prime):
    n = len(matrix)
    factor = (prime - 1) // 2

    # Create a new matrix to store scrambled values
    scrambled = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):

            if matrix[i][j] == 0:
                scrambled[i][j] = 0
            else:
                scrambled[i][j] = mod_multiply(matrix[i][j], factor, prime)

    return scrambled


def reverse_prime_field(matrix, prime):
    n = len(matrix)
    factor = (prime - 1) // 2

    inverse_factor = mod_inverse(factor, prime)
    unscrambled = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):

            if matrix[i][j] == 0:
                unscrambled[i][j] = 0
            else:
                unscrambled[i][j] = mod_multiply(matrix[i][j], inverse_factor, prime)

    return unscrambled


def recover_nodes_from_matrix(matrix, prime):

    n = len(matrix)
    nodes = [0] * n

    if n == 0:
        return nodes

    if n == 1:
        return [0]

    if n >= 3:
        S01 = (matrix[0][1] - 1) % prime
        S02 = (matrix[0][2] - 2) % prime
        S12 = (matrix[1][2] - 3) % prime

        inv2 = mod_inverse(2, prime)   # modular inverse of 2

        nodes[0] = (S01 + S02 - S12) * inv2 % prime
        nodes[1] = (S01 - nodes[0]) % prime
        nodes[2] = (S02 - nodes[0]) % prime

    elif n == 2:
        S = (matrix[0][1] - 1) % prime
        best = (0, 0)
        for c0 in range(1, ASCII_MAX):          
            c1 = (S - c0) % prime
            if 0 < c1 < ASCII_MAX:
                best = (c0, c1)
                break
        nodes[0], nodes[1] = best

    for i in range(3, n):
        nodes[i] = (matrix[i][0] - nodes[0] - i) % prime

    nodes = [v if 0 <= v < ASCII_MAX else 0 for v in nodes]

    return nodes







    