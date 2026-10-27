
def xor(a, b):
    result = ""

    for i in range(1, len(b)):
        result += "0" if a[i] == b[i] else "1"

    return result


def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[:pick]

    while pick < len(dividend):
        if tmp[0] == "1":
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor("0" * pick, tmp) + dividend[pick]

        pick += 1

    if tmp[0] == "1":
        tmp = xor(divisor, tmp)
    else:
        tmp = xor("0" * pick, tmp)

    return tmp


def encode_data(data, generator):
    appended = data + "0" * (len(generator) - 1)
    remainder = mod2div(appended, generator)

    return data + remainder 


def verify(frame, generator):
    remainder = mod2div(frame, generator)

    return set(remainder) == {"0"}
