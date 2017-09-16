from subprocess import Popen, PIPE
from queue import Queue
import sys
from threading import Thread, Event
import time

class Buffer(Queue):

    def __init__(self, *args, **kwargs):
        Queue.__init__(self, *args, **kwargs)

    def write(self, line):
        self.put(line)

    def read(self):
        return self.get()

buffer = Buffer()
stopped = Event()

def write_output(buffer, stopped):
    logcat = Popen(['cat', '/dev/urandom'], bufsize=0, stdout=PIPE)
    for line in logcat.stdout.readlines(8096):
        buffer.write(line)
        if stopped.is_set():
            break

def read_output(buffer):
    while not buffer.empty():
        output = buffer.read()
        print(output)
        sys.stdout.flush()

generate_random_output = Thread(target=write_output, args=(buffer, stopped))
process_output = Thread(target=read_output, args=(buffer,))

generate_random_output.start()
time.sleep(1)
process_output.start()
time.sleep(3)
stopped.set()
generate_random_output.join()
print('finished generating')
process_output.join()
print('finished processing')
