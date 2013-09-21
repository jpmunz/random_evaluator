import os
import math
import gzip
import datetime
import contextlib

READ_CHUNK_BITS = 2**10
WRITE_CHUNK_BITS = 2**10
TOTAL_WRITE_SIZE_BITS = 2**20
TEST_DIRECTORY = 'test_output'

def _write_random_file(filename, random_module):
    with open(filename, 'wb') as f:
        written = 0

        while written < TOTAL_WRITE_SIZE_BITS:
            bits = random_module.getrandbits(WRITE_CHUNK_BITS)
            f.write(bits)
            written += WRITE_CHUNK_BITS

def _compress_file(filename):
    with contextlib.nested(
        open(filename, 'rb'),
        gzip.open(filename + '.gz', 'wb')
    ) as (f_in, f_out):
        f_out.write(f_in.read())

def _shannon_entropy(filename):
    '''
    http://stackoverflow.com/questions/990477/how-to-calculate-the-entropy-of-a-file
    '''

    counts = {}

    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(READ_CHUNK_BITS)

            if not chunk:
                break

            for c in chunk:
                cnt = counts.setdefault(c, 0)
                cnt += 1
                counts[c] = cnt

    filesize = float(os.path.getsize(filename))
    entropy = 0

    for cnt in counts.values():
        if cnt > 0:
            p = cnt / filesize
            entropy -= (p * math.log(p, 2))

    return entropy / 8.0

def evaluate(title, random_module, directory=TEST_DIRECTORY):

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, datetime.datetime.now().isoformat())

    _write_random_file(filename, random_module)
    _compress_file(filename)

    compression_ratio = os.path.getsize(filename + '.gz') \
                        / float(os.path.getsize(filename))

    print "Test Case: %s" % title
    print
    print "GZIP Compression ratio: %0.3f" % compression_ratio
    print "Shannon entropy %0.3f" % _shannon_entropy(filename)
    print
