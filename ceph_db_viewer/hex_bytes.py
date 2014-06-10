import sys
import os
import struct


class HexBytes(object):

    def __init__(self, raw='', limit=-1):
        self.raw = raw
        self.limit = limit

    def raw(self):
        return self.raw

    def hex(self, space=False):
        hex_str = self.raw.encode("hex")
        out = []
        idx = 0
        total_len = 0
        for c in hex_str:
            out.append(c)
            if space and idx % 2 == 1:
                out.append(' ')
                total_len += 1
            idx += 1
            total_len += 2
            if total_len >= self.limit and self.limit > 0:
                out.append(' ...')
                break
        return ''.join(out)

    def _txt_omit(self):
        out = []
        total_len = 0
        for c in self.raw:
            if ord(c) < ord(' '):
                pass
            elif ord(c) < 127:
                out.append(c)
                total_len += 1
            elif ord(c) == 127:
                pass
            else:
                out.append('?')
                total_len += 1
            if total_len >= self.limit and self.limit > 0:
                out.append(' ...')
                break
        return ''.join(out)

    def _txt_no_omit(self):
        out = []
        total_len = 0
        for c in self.raw:
            if ord(c) < ord(' '):
                # control character
                if c == '\t':
                    out.append(r'\t')
                    total_len += 2
                elif c == '\n':
                    out.append(r'\n')
                    total_len += 2
                elif c == '\r':
                    out.append(r'\r')
                    total_len += 2
                else:
                    str = r'\x'+c.encode("hex")
                    out.append(str)
                    total_len += len(str)
            elif ord(c) <= ord('~'):
                # text character
                out.append(c)
                total_len += 1
            else:
                str = r'\x'+c.encode("hex")
                out.append(str)
                total_len += len(str)
            if total_len >= self.limit and self.limit > 0:
                out.append(' ...')
                break

        return ''.join(out)

    def txt(self, omit=True):
        return omit and self._txt_omit() or self._txt_no_omit()

    # @param byte_order: same with struct lib
    def int(self, length=4, signed=False, byte_order='@'):
        format = byte_order
        if length == 1:
            if signed:
                format += 'b'
            else:
                format += 'B'
        elif length == 2:
            if signed:
                format += 'h'
            else:
                format += 'H'
        elif length == 4:
            if signed:
                format += 'i'
            else:
                format += 'I'
        elif length == 8:
            if signed:
                format += 'q'
            else:
                format += 'Q'
        else:
            raise ValueError("length illegal: %s" % length)

        out = []
        total_len = 0
        idx = 0
        raw_len = len(self.raw)
        while idx < raw_len:
            token = self.raw[idx:(idx+length)]
            if len(token) >= length:
                number = struct.unpack(format, token)[0]
                num_str = str(number)
                out.append(num_str)
                out.append('\t')
                total_len += len(num_str)
                if total_len >= self.limit and self.limit > 0:
                    out.append(' ...')
                    break
            idx += length

        return ''.join(out)

    def uint32(self):
        return self.int(length=4)

    def uint64(self):
        return self.int(length=8)
