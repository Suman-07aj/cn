
def binary_add(a, b):
    total = int(a, 2) + int(b, 2)

    # Wrap the carry around
    while total > 255:
        total = (total & 255) + 1

    return format(total, "08b")


def ones_complement(bits):
    result = ""

    for bit in bits:
        if bit == "0":
            result += "1"
        else:
            result += "0"

    return result


def generate_checksum(words):
    total = words[0]

    for word in words[1:]:
        total = binary_add(total, word)

    return ones_complement(total)


def verify(words, checksum):
    total = words[0]

    for word in words[1:]:
        total = binary_add(total, word)

    total = binary_add(total, checksum)

    return total == "11111111"



