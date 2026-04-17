import hashlib
import sys

if len(sys.argv) < 2:
    exit(-1)

TARGET = 'source/problems/files/'
content = open(sys.argv[1], 'rb').read()

dst = TARGET + hashlib.md5(content).hexdigest() + ('' if '.' not in sys.argv[1] else ('.' + sys.argv[1].rsplit('.', 1)[-1]))
open(dst, 'wb').write(content)

print(f'copy to {dst.removeprefix('source/problems/')}')
