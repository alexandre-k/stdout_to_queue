from subprocess import Popen, PIPE
from queue import Queue
import sys
from threading import Thread, Event
import threading


words = {b'f7', b'c3', b'c9'}

def write_output(words, stopped):
    hexdump = Popen(['hexdump', '-C', '/dev/urandom'], stdout=PIPE)
    while hexdump.returncode is None:
        while not stopped.is_set():
            for line in iter(hexdump.stdout.readline, b''):
                # print(line)
                yield [word for word in words if word in line]

def read_output(words, stopped):
    for result in write_output(words, stopped):
        if b'f7' in result:
            print('got it')
        if b'c3' in result:
            print('********* found: {}'.format(result))
        sys.stdout.flush()


stopped = Event()

process_output = Thread(target=read_output, args=(words, stopped))
process_output.name = 'process_output'
process_output.start()

try:
    while True:
        continue
except KeyboardInterrupt:
    stopped.set()
    process_output.join()
    print('finished processing')
