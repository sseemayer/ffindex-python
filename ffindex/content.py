BUF_SIZE = 1024


class FFIndexContent(object):
    def __init__(self, parent, start, length, name, encoding=None):
        self.parent = parent
        self.start = start
        self.pos = 0
        self.length = length
        self.name = name
        self.mode = 'rb'
        self.encoding = encoding

        self.closed = False
        self.readbuffer = b''

    def close(self):
        pass

    def flush(self):
        pass

    def isatty(self):
        return False

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration()

        return line

    next = __next__

    def read(self, size=None):
        if size is None:
            size = self.length - self.pos

        if size <= 0:
            return b""

        buffered = len(self.readbuffer)
        unbuffered = size - buffered
        if unbuffered > 0:
            self.parent.seek(self.start + self.pos + buffered)
            self.pos += size
            self.readbuffer += self.parent.read(unbuffered)

        return self.readbuffer[0:size]

    def readline(self, size=None):

        bufofs = 0
        while True:
            i = self.readbuffer.find(b'\n', bufofs) + 1
            if i > 0:
                line = self.readbuffer[0:i]
                self.readbuffer = self.readbuffer[i:]
                self.pos += i
                break

            else:
                self.parent.seek(self.start + self.pos + bufofs)

                read_until = self.length - self.pos
                if read_until > BUF_SIZE:
                    read_until = BUF_SIZE

                elif read_until < 1:
                    line = b''
                    break

                newbuf = self.parent.read(read_until)
                bufofs = len(self.readbuffer)
                self.readbuffer += newbuf

        if self.encoding:
            line = line.decode(self.encoding)

        return line

    def readlines(self, sizehint=None):
        if sizehint is None:
            s = self.readline()
            while s:
                yield s
                s = self.readline()
        else:
            for _ in range(sizehint):
                yield self.readline()

    def seek(self, offset, whence=0):

        if whence == 1:
            offset = self.pos + offset

        elif whence == 2:
            offset = self.length + offset

        if offset < 0:
            offset = 0

        if offset > self.length:
            offset = self.length

        self.readbuffer = b''
        self.pos = offset

    def tell(self):
        return self.pos

    def truncate(self, size=None):
        if size is None:
            size = self.pos

        if size > self.length:
            size = self.length

        self.length = size

    def write(self, str):
        raise Error("Read-only access!")

    def writelines(self, sequence):
        raise Error("Read-only access!")

    def __iter__(self):
        return self

    def __repr__(self):
        return "FFIndexEntry('{name}', start={start}, length={length})".format(name=self.name, start=self.start, length=self.length)
