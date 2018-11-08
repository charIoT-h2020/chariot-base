#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastecdsa import curve
from fastecdsa.point import Point

from chariot_base.utilities.encryption import pad, unpad, string_to_number, decode_point, encode_point, \
    generate_new_keypair


def test_pad():
    assert len(pad("0", 256)) == 256
    assert len(pad("0", 512)) == 512
    assert len(pad("0", 1024)) == 1024

    assert len(pad("test", 2)) == 6
    assert len(pad("test", 4)) == 8


def test_unpad():
    msg = pad("0", 256)
    assert unpad(msg, 256) == "0"
    msg = pad("0", 512)
    assert unpad(msg, 512) == "0"
    msg = pad("0", 1024)
    assert unpad(msg, 1024) == "0"

    msg = pad("test", 2)
    assert unpad(msg, 2) == "test"
    msg = pad("test", 4)
    assert unpad(msg, 4) == "test"

    msg = unpad(b'very secret thing\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f', 16)
    assert msg == b'very secret thing'


def test_string_to_number():
    assert string_to_number(b'\x00\x00') == 0
    assert string_to_number(b'\x00\x15') == 21
    assert string_to_number(b'\x01\x00') == 256


def test_encode_point():
    xs = 0xde2444bebc8d36e682edd27e0f271508617519b3221a8fa0b77cab3989da97c9
    ys = 0xc093ae7ff36e5380fc01a5aad1e66659702de80f53cec576b6350b243042a256
    s = Point(xs, ys, curve=curve.P256)
    assert encode_point(s,
                        True) == b'\x02\xde$D\xbe\xbc\x8d6\xe6\x82\xed\xd2~\x0f\'\x15\x08au\x19\xb3"\x1a\x8f\xa0\xb7|\xab9\x89\xda\x97\xc9'

    s = Point(xs, ys, curve=curve.P256)
    assert encode_point(s,
                        False) == b'\x04\xde$D\xbe\xbc\x8d6\xe6\x82\xed\xd2~\x0f\'\x15\x08au\x19\xb3"\x1a\x8f\xa0\xb7|\xab9\x89\xda\x97\xc9\xc0\x93\xae\x7f\xf3nS\x80\xfc\x01\xa5\xaa\xd1\xe6fYp-\xe8\x0fS\xce\xc5v\xb65\x0b$0B\xa2V'


def test_decode_point():
    xs = 0xde2444bebc8d36e682edd27e0f271508617519b3221a8fa0b77cab3989da97c9
    ys = 0xc093ae7ff36e5380fc01a5aad1e66659702de80f53cec576b6350b243042a256
    p1 = b'\x02\xde$D\xbe\xbc\x8d6\xe6\x82\xed\xd2~\x0f\'\x15\x08au\x19\xb3"\x1a\x8f\xa0\xb7|\xab9\x89\xda\x97\xc9'
    p2 = b'\x04\xde$D\xbe\xbc\x8d6\xe6\x82\xed\xd2~\x0f\'\x15\x08au\x19\xb3"\x1a\x8f\xa0\xb7|\xab9\x89\xda\x97\xc9\xc0\x93\xae\x7f\xf3nS\x80\xfc\x01\xa5\xaa\xd1\xe6fYp-\xe8\x0fS\xce\xc5v\xb65\x0b$0B\xa2V'

    pp1 = decode_point(p1)
    assert pp1.x == xs
    assert pp1.y == ys

    pp2 = decode_point(p2)
    assert pp2.x == xs
    assert pp2.y == ys


def test_encrypt():
    key_store = generate_new_keypair()
    secret = 'very secret thing'
    message = key_store.encrypt(secret)
    assert len(message) == 140

    secret = 'κατι πολυ κρυφο'  # UTF checking
    message = key_store.encrypt(secret)
    assert len(message) == 136


def test_decrypt():
    key_store = generate_new_keypair()
    secret = 'very secret thing'
    message = key_store.encrypt(secret)
    assert key_store.decrypt(message).decode() == secret

    secret = 'κατι πολυ κρυφο'  # UTF checking
    message = key_store.encrypt(secret)
    assert key_store.decrypt(message).decode() == secret


def test_sign():
    key_store = generate_new_keypair()
    message = 'very secret thing'
    s = key_store.sign(message)
    assert len(s) == 88

    message = 'κατι πολυ κρυφο'  # UTF checking
    s = key_store.sign(message)
    assert len(s) == 88


def test_verify():
    key_store = generate_new_keypair()
    message = 'very secret thing'
    s = key_store.sign(message)
    assert key_store.verify(message, s) is True

    message = 'κατι πολυ κρυφο'  # UTF checking
    s = key_store.sign(message)
    assert key_store.verify(message, s) is True

    message = '早上好'  # Good morning in Mandarin Chinese
    s = key_store.sign(message)
    assert key_store.verify(message, s) is True
