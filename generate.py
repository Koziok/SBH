import random

def generate(n):
    data = ["A", "C", "G", "T"]
    sequence = []
    for i in range(0, n):
        randomLetter = random.randint(0, 3)
        if i > 3:
            if data[randomLetter] == sequence[i-2]:
                j = randomLetter
                while j == randomLetter:
                    j = random.randint(0, 3)
                sequence.append(data[j])
            else:
                sequence.append(data[randomLetter])
        else:
            sequence.append(data[randomLetter])

    return sequence

def save(sequence):
    f = open("sequence.txt", "w")
    for i in sequence:
        f.write(i)
    f.close()

if __name__ == '__main__':
    n = 30
    sequence = generate(n)
    save(sequence) 