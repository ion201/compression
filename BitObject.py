import struct


class ByteFields:
    """Allows for bit manipulation in a byte"""
    def __init__(self, value=0):
        self._d = value
        self._index = -1
        while value != 0:
            value >>= 1
            self._index += 1

    def __getitem__(self, index):
        return (self._d >> index) & 1

    def __setitem__(self, index, value):
        value = (value & 1) << index
        mask = 1 << index
        self._d = (self._d & ~mask) | value
        if index > self._index:
            self._index = index

    def __str__(self):
        return bin(self._d)

    def __int__(self):
        return self._d

    def __len__(self):
        return self._index + 1

    def append(self, value, bits):
        for i in range(bits):
            self._d <<= 1
            self._d += value >> i & 1
            self._index += 1

    def popbyte(self):
        if self._index < 7:
            return None

        popped_byte = self._d >> self._index - 8
        self._d ^= popped_byte << self._index - 8

        self._index -= 8

        return struct.pack('>B', popped_byte)