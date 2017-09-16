import time
from subprocess import Popen, PIPE
from queue import Queue
import sys
from threading import Thread, Event
import threading



class FilterOutput:

    def __init__(self, cmd):
        self.cmd = cmd.split(' ')
        self.words = {b'f7', b'c3', b'c9'}
        self.counter = {}
        self.thread = Thread(target=self.filter_output)

    def start(self):
        self.thread.start()

    def stop(self):
        self.hexdump.terminate()
        self.hexdump.wait()
        self.thread.join()

    def read_output(self):
        self.hexdump = Popen(self.cmd, stdout=PIPE)
        for line in iter(self.hexdump.stdout.readline, b''):
            yield line


    def filter_output(self):
        for line in self.read_output():
            result = [word for word in self.words if word in line]

            sys.stdout.flush()

            if b'f7' in result:
                print(line)
            if b'c3' in result:
                print(line)
            sys.stdout.flush()


filter_output = FilterOutput('hexdump -C /dev/urandom')
filter_output.start()

try:
    while True:
        time.sleep(5)
        raise KeyboardInterrupt
except KeyboardInterrupt:
    filter_output.stop()
    print('finished processing')

# performance results
# without yield
# b'00d16d10  92 16 fa cf ab 37 16 75  4b f3 e2 f3 25 f7 b0 b4  |.....7.uK...%...|\n'

# b'00d3f960  d5 ca a2 1e c6 f0 f7 61  88 1c ae 58 b6 70 d1 18  |.......a...X.p..|\n'

# b'00c043d0  f7 65 7f f0 cb d4 75 9b  54 ae 80 61 98 85 49 75  |.e....u.T..a..Iu|\n'

# b'00ca6aa0  6e 50 b0 84 96 73 f7 55  3a 02 29 20 fc 36 70 b2  |nP...s.U:.) .6p.|\n'

# b'00d6b510  8d c3 ec 2c e3 0b 94 75  94 b6 ed e9 7f fa a4 ef  |...,...u........|\n'

# # with yield

# b'00c4d910  ae e6 95 a3 a2 d1 d9 54  df 90 a1 8a b8 c3 5d fc  |....'

# b'00cab8a0  b6 9b b5 04 c3 51 23 b1  87 e4 f1 d1 e0 e2 c9 71  |.....Q#........q|\n'

# b'00c99b70  70 c3 c9 5e 06 60 b8 4f  b8 2d dd ba 3c 53 63 e1  |p..^.`.O.-..<Sc.|\n'

# b'00c62380  53 0c 60 77 0b 1d cb f5  54 1c 4a 71 d8 01 f7 f4  |S.`w....T.Jq....|\n'

# b'00c716a0  dc 7e 5b 98 e6 d5 1e 66  34 38 b7 c3 c5 10 19 43  |.~[....f48...'


            
