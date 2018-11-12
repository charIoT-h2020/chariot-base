import math
import binascii
import base64
import hashlib
import hmac
import struct
import os
import textwrap

from ecdsa import numbertheory

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Random import random

from fastecdsa import curve, ecdsa, keys
from fastecdsa.point import Point


BASE_CURVE = curve.P256


def generate_new_keypair(curve=BASE_CURVE):
    priv_key, pub_key = keys.gen_keypair(curve)
    return KeyPair(pub_key, priv_key, curve)


def pad(message, block_size):
    """
    PKCS#7 padding
    """
    padded = message
    last_block = len(message) % block_size
    to_pad = block_size - last_block
    for i in range(to_pad):
        padded = padded + chr(to_pad)
    return padded


def unpad(message, block_size):
    if type(message) is bytes:
        return binary_unpad(message, block_size)

    length = len(message)
    if length == 0:
        return message

    to_pad = ord(message[length - 1])
    if to_pad > block_size:
        return message

    if length < to_pad:
        return message

    pad_start = length - to_pad
    for c in message[pad_start:]:
        if c != chr(to_pad):
            return message

    return message[:pad_start]


def binary_unpad(message, block_size):
    length = len(message)
    if length == 0:
        return message

    to_pad = message[length - 1]
    if to_pad > block_size:
        return message

    if length < to_pad:
        return message

    pad_start = length - to_pad
    return message[:pad_start]


def string_to_number(string):
    return int(binascii.hexlify(string), 16)


def number_to_string(num, order):
    length = orderlen(order)
    fmt_str = "%0" + str(2 * length) + "x"
    string = binascii.unhexlify((fmt_str % num).encode())
    assert len(string) == length, (len(string), length)
    return string


def orderlen(order):
    return (1 + len("%x" % order)) // 2  # bytes


def randrange(order, entropy=None):
    """Return a random integer k such that 1 <= k < order, uniformly
    distributed across that range. For simplicity, this only behaves well if
    'order' is fairly close (but below) a power of 256. The try-try-again
    algorithm we use takes longer and longer time (on average) to complete as
    'order' falls, rising to a maximum of avg=512 loops for the worst-case
    (256**k)+1 . All of the standard curves behave well. There is a cutoff at
    10k loops (which raises RuntimeError) to prevent an infinite loop when
    something is really broken like the entropy function not working.
    Note that this function is not declared to be forwards-compatible: we may
    change the behavior in future releases. The entropy= argument (which
    should get a callable that behaves like os.urandom) can be used to
    achieve stability within a given release (for repeatable unit tests), but
    should not be used as a long-term-compatible key generation algorithm.
    """

    if entropy is None:
        entropy = os.urandom
    assert order > 1
    bytes = orderlen(order)
    dont_try_forever = 10000  # gives about 2**-60 failures for worst case
    while dont_try_forever > 0:
        dont_try_forever -= 1
        candidate = string_to_number(entropy(bytes)) + 1
        if 1 <= candidate < order:
            return candidate
        continue
    raise RuntimeError("randrange() tried hard but gave up, either something"
                       " is very wrong or you got really unlucky. Order was"
                       " %x" % order)


def encode_point(p, compressed, curve=BASE_CURVE):
    order = curve.q
    x_str = number_to_string(p.x, order)
    if compressed:
        return bytes(chr(2 if (p.y & 1) == 0 else 3), 'utf-8') + x_str
    else:
        y_str = number_to_string(p.y, order)
    return bytes(chr(4), 'utf-8') + x_str + y_str


def decode_point(point, curve=BASE_CURVE):
    # See http://www.secg.org/download/aid-780/sec1-v2.pdf section 2.3.4
    elliptic_curve = curve
    order = elliptic_curve.q
    base_length = orderlen(order)

    if point[0] == 4:
        # 3
        x_str = point[1:base_length + 1]
        y_str = point[base_length + 1:]
        return Point(string_to_number(x_str), string_to_number(y_str), curve=elliptic_curve)
    else:
        # 2.3
        if point[0] == 2:
            yp = 0
        elif point[0] == 3:
            yp = 1
        else:
            return None
        # 2.2
        x_str = point[1:base_length + 1]
        x = string_to_number(x_str)
        # 2.4.1
        alpha = ((x * x * x) + (elliptic_curve.a * x) + elliptic_curve.b) % elliptic_curve.p
        beta = numbertheory.square_root_mod_prime(alpha, elliptic_curve.p)
        if (beta - yp) % 2 == 0:
            y = beta
        else:
            y = elliptic_curve.p - beta

    return Point(x, y, curve=elliptic_curve)


class KeyPair:
    def __init__(self, public_key, private_key, curve=BASE_CURVE):
        self.public_key = public_key
        self.private_key = private_key
        self.curve = curve

    def sign(self, message):
        r, s = ecdsa.sign(message, self.private_key)
        return self.encode_signature(r, s)

    def verify(self, message, r_s):
        r, s = self.decode_signature(r_s)
        return ecdsa.verify((r, s), message, self.public_key)

    def encode_signature(self, r, s):
        length = orderlen(self.curve.q)
        fmt_str = "%0" + str(2 * length) + "x"
        s = binascii.unhexlify((fmt_str % s).encode())
        r = binascii.unhexlify((fmt_str % r).encode())
        return base64.b64encode(r + s)

    def decode_signature(self, r_s):
        s_decoded = base64.b64decode(r_s)
        base_length = orderlen(self.curve.q)
        r = int(binascii.hexlify(s_decoded[:base_length]), 16)
        s = int(binascii.hexlify(s_decoded[base_length:]), 16)
        return r, s

    def decrypt(self, message, curve=BASE_CURVE):
        R_size = 1 + orderlen(curve.q)
        mac_size = hashlib.sha256().digest_size

        message_binary = base64.b64decode(message)
        if len(message_binary) < (R_size + mac_size):
            return None

        R = decode_point(message_binary)
        d = message_binary[R_size:R_size + mac_size]
        prefix_bytes = message_binary[R_size + mac_size:R_size + mac_size + 8]
        c = message_binary[R_size + mac_size + 8:]
        S = (self.private_key * R).x
        S_bytes = number_to_string(S, curve.q)
        k_E = hashlib.sha256(S_bytes + struct.pack(">I", 1)).digest()
        k_M = hashlib.sha256(S_bytes + struct.pack(">I", 2)).digest()
        d_verify = hmac.new(k_M, prefix_bytes + c, hashlib.sha256).digest()
        if d_verify != d:
            return None
        ctr = Counter.new(64, prefix=prefix_bytes)
        cipher = AES.new(key=k_E, mode=AES.MODE_CTR, counter=ctr)
        padded = cipher.decrypt(c)
        return unpad(padded, AES.block_size)

    def encrypt(self, message, curve=BASE_CURVE):
        padded = pad(message, AES.block_size).encode("utf-8")
        r = randrange(curve.q)
        R = curve.G * r
        S = (self.public_key * r).x
        S_bytes = number_to_string(S, curve.q)

        k_E = hashlib.sha256(S_bytes + struct.pack(">I", 1)).digest()
        k_M = hashlib.sha256(S_bytes + struct.pack(">I", 2)).digest()

        prefix = random.getrandbits(64)
        prefix_bytes = struct.pack("<Q", prefix)
        ctr = Counter.new(64, prefix=prefix_bytes)
        cipher = AES.new(key=k_E, mode=AES.MODE_CTR, counter=ctr)
        c = cipher.encrypt(padded)
        d = hmac.new(k_M, prefix_bytes + c, hashlib.sha256).digest()

        return textwrap.fill(base64.b64encode(encode_point(R, True) + d + prefix_bytes + c).decode(), 200)
