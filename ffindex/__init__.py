from ffindex.content import FFIndexContent
import mmap

try:
    isinstance("", basestring)

    def _is_string(s):
        return isinstance(s, basestring)
except NameError:
    def _is_string(s):
        return isinstance(s, str)


def _to_file(fn, mode="rb"):
    if _is_string(fn):
        return open(fn, mode)
    else:
        return fn


def read(ffindex_data, ffindex_db=None, encoding=None):
    """Generator to parse FFindex entries"""

    if ffindex_db is None:
        if _is_string(ffindex_data):
            ffindex_db = ffindex_data + ".index"
        else:
            raise Exception("When ffindex_data is passed as a file-like object, ffindex_db is required")

    f_db = _to_file(ffindex_db, "r")
    f_data = _to_file(ffindex_data, "r+b")

    m_data = mmap.mmap(f_data.fileno(), 0)

    for l_db in f_db:
        filename, start, length = l_db.strip().split("\t")

        yield FFIndexContent(m_data, int(start), int(length) - 1, filename, encoding)

    m_data.close()

    if _is_string(ffindex_db):
        f_db.close()

    if _is_string(ffindex_data):
        f_data.close()
