import random

def generate(n):
    data = ["A", "C", "G", "T"]
    sequence = []
    for i in range(0, n):
        sequence.append(data[random.randint(0, 3)])

    return sequence

def save(sequence):
    f = open("sequence.txt", "w")
    for i in sequence:
        f.write(i)
    f.close()

if __name__ == '__main__':
    n = 500
    sequence = generate(n)
    save(sequence)