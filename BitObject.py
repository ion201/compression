import struct


class ByteFields:
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
        s = ''
        tmp = self._d
        for i in range(self._index+1):
            s = str(tmp & 1) + s
            tmp >>= 1

        return s

    def __int__(self):
        return self._d

    def __len__(self):
        return self._index + 1

    def clear(self):
        self._d = 0
        self._index = -1

    def append(self, value, bits=8):
        if type(value) == bytes:
            value = ord(value)

        self._d <<= bits
        self._d += value
        self._index += bits

    def hasbits(self, number):
        if self._index >= number-1:
            return True
        return False

    def hasbyte(self):
        if self._index >= 7:
            return True
        return False

    def popbits(self, number):
        while self._index < (number - 1):
            number -= 1

        popped_byte = self._d >> self._index - number + 1
        self._d ^= popped_byte << self._index - number + 1

        self._index -= number

        return popped_byte

    def popbyte(self):
        return struct.pack('>B', self.popbits(8))