import sys
from time import sleep

print('first')
print('second', end='')
# uncomment to fix!
# sys.stdout.flush()
print('third', file=sys.stderr)

sleep(2)
