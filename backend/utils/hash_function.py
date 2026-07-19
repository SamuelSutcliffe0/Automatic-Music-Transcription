def preprocessing(text: str, salt: int) -> int:
    data = text.encode()

    salt_bytes = salt.to_bytes(4, byteorder="big")

    data_bytes = bytearray(data)

    for i in range(len(data_bytes)):
        data_bytes[i] ^= salt_bytes[i % 4]

    x = int.from_bytes(data_bytes, byteorder="big")
    return x


def padding(integer: int, n: int = 16) -> str:
    string = str(integer)
    string += "1"

    target_length = (512 * n) - 64
    if len(string) < target_length:
        string += "0" * (target_length - len(string))

    length_64 = bin(integer % (2**64))[2:].zfill(64)
    string += length_64

    return string


K = [
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
    0xE49B69C1,
    0xEFBE4786,
    0x0FC19DC6,
    0x240CA1CC,
    0x2DE92C6F,
    0x4A7484AA,
    0x5CB0A9DC,
    0x76F988DA,
    0x983E5152,
    0xA831C66D,
    0xB00327C8,
    0xBF597FC7,
    0xC6E00BF3,
    0xD5A79147,
    0x06CA6351,
    0x14292967,
    0x27B70A85,
    0x2E1B2138,
    0x4D2C6DFC,
    0x53380D13,
    0x650A7354,
    0x766A0ABB,
    0x81C2C92E,
    0x92722C85,
    0xA2BFE8A1,
    0xA81A664B,
    0xC24B8B70,
    0xC76C51A3,
    0xD192E819,
    0xD6990624,
    0xF40E3585,
    0x106AA070,
    0x19A4C116,
    0x1E376C08,
    0x2748774C,
    0x34B0BCB5,
    0x391C0CB3,
    0x4ED8AA4A,
    0x5B9CCA4F,
    0x682E6FF3,
    0x748F82EE,
    0x78A5636F,
    0x84C87814,
    0x8CC70208,
    0x90BEFFFA,
    0xA4506CEB,
    0xBEF9A3F7,
    0xC67178F2,
]


def right_rotate(value, bits):
    return ((value >> bits) | (value << (32 - bits))) & 0xFFFFFFFF


def calculate_W(chunk: str):
    W = []

    for i in range(16):
        W.append(int(chunk[32 * i : 32 * (i + 1)]))

    for i in range(16, 64):
        s0 = right_rotate(W[i - 15], 7) ^ right_rotate(W[i - 15], 18) ^ (W[i - 15] >> 3)
        s1 = right_rotate(W[i - 2], 17) ^ right_rotate(W[i - 2], 19) ^ (W[i - 2] >> 10)
        W_i = (W[i - 16] + s0 + W[i - 7] + s1) & 0xFFFFFFFF
        W.append(W_i)

    return W


def chunk_cycle(buffer_values, chunk):
    W = calculate_W(chunk)

    for i in range(64):
        buffer_values = round_step(buffer_values, W[i], K[i])

    return buffer_values


def round_step(buffer_values, W, K):
    A, B, C, D, E, F, G, H = buffer_values
    Ch = (E & F) ^ ((~E) & G)
    Ma = (A & B) ^ (A & C) ^ (B & C)

    ΣA = right_rotate(A, 2) ^ right_rotate(A, 13) ^ right_rotate(A, 22)
    ΣE = right_rotate(E, 6) ^ right_rotate(E, 11) ^ right_rotate(E, 25)

    T1 = (H + ΣE + Ch + K + W) & 0xFFFFFFFF
    T2 = (ΣA + Ma) & 0xFFFFFFFF

    return ((T1 + T2) & 0xFFFFFFFF, A, B, C, (D + T1) & 0xFFFFFFFF, E, F, G)


def hash(message, salt):
    num = preprocessing(message, salt)
    padded = padding(num)

    buffer_values = (
        0x6A09E667,
        0xBB67AE85,
        0x3C6EF372,
        0xA54FF53A,
        0x510E527F,
        0x9B05688C,
        0x1F83D9AB,
        0x5BE0CD19,
    )

    for i in range(16):
        buffer_values = chunk_cycle(buffer_values, padded[512 * i : 512 * (i + 1)])

    return "".join(f"{v:08x}" for v in buffer_values)


