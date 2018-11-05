def has_read_right(flag):
    return flag & 2 > 0


def has_write_right(flag):
    return flag & 1 > 0
