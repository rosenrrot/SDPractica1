'''
Peer actor 5
'''

from pyactor.context import set_context,set_context,create_host,serve_forever,sleep,interval
from UserString import MutableString
import random



class Echo(object):
    _tell = ['push','cycle','start']
    _ask = ['pull']



    def push(self,chunk_id,chunk_data):
        infile = open('fichero_torrent5.txt', 'r+')
        for line in infile:
            word = MutableString(line)
        infile.close()
        if (word[chunk_id] == '0'):
            infile = open('fichero_torrent5.txt', 'w+')
            word[chunk_id]=chunk_data
            infile.write(str(word))
            infile.close()
            self.chunk_number += 1
            infile = open('average_peer5.txt', 'a')
            infile.write(str(self.chunk_number))
            infile.write(';')
            infile.write(str(self.gossip_cicle))
            infile.write('\n')
            infile.close()

    def pull(self,chunk_id):
        infile = open('fichero_torrent5.txt', 'r')
        for line in infile:
            line2 = MutableString(line)
        infile.close()
        if (line2[chunk_id] != '0'):
            return line2[chunk_id]
        else:
            return None

    def __init__(self):
        self.vecinos = []
        self.chunk_number = 0
        self.seconds = 0
        self.gossip_cicle = 0

    def cycle(self,tracker,host_ref,opcion):
        self.gossip_cicle += 1
        if self.seconds == 2:
            self.vecinos = tracker.get_peers('torrentFile1')
            self.seconds = 0
        self.seconds += 1
        if len(self.vecinos) > 1:
            if (opcion == 'push' or opcion == 'push-pull'):
                infile = open('fichero_torrent5.txt', 'r+')
                for line in infile:
                    word = MutableString(line)
                infile.close()
                chunk_id = random.randint(0, 8)
                n_veces = 0
                while word[chunk_id] == '0' and n_veces < 9:
                    chunk_id = random.randint(0, 8)
                    n_veces += 1
                if word[chunk_id] != '0':
                    for i in range(len(self.vecinos)):
                        ref = self.vecinos[i]
                        ref_lookup = ref.split(";")
                        if ref != host_ref:
                            rpeer = self.host.lookup_url(ref_lookup[0], ref_lookup[1], ref_lookup[2])
                            rpeer.push(chunk_id, word[chunk_id])

            if ((opcion == 'pull' or opcion == 'push-pull') and self.chunk_number < 9):
                infile = open('fichero_torrent5.txt', 'r+')
                for line in infile:
                    word = MutableString(line)
                infile.close()
                for i in range(len(self.vecinos)):
                    chunk_id = random.randint(0, 8)
                    while word[chunk_id] != '0':
                        chunk_id = random.randint(0, 8)
                    ref = self.vecinos[i]
                    ref_lookup = ref.split(";")
                    if ref != host_ref:
                        rpeer = self.host.lookup_url(ref_lookup[0], ref_lookup[1], ref_lookup[2])
                        chunk_data=rpeer.pull(chunk_id)
                        if chunk_data != None:
                            infile = open('fichero_torrent5.txt', 'w+')
                            word[chunk_id] = chunk_data
                            infile.write(str(word))
                            infile.close()
                            self.chunk_number += 1
                            infile = open('average_peer5.txt', 'a')
                            infile.write(str(self.chunk_number))
                            infile.write(';')
                            infile.write(str(self.gossip_cicle))
                            infile.write('\n')
                            infile.close()

    def start(self):
        infile = open('fichero_torrent5.txt', 'w+')
        infile.write('000000000')
        infile.close()
        host_ref = "http://127.0.0.1:1298/peer5;Echo;peer5"
        tracker = self.host.lookup_url('http://127.0.0.1:1285/tracker', 'Echo', 'tracker')
        self.interval1 = interval(self.host,10,tracker,"announce","torrentFile1",host_ref)
        self.interval2 = interval(self.host,1,self.proxy,"cycle",tracker,host_ref,'push-pull')


if __name__ == "__main__":
    set_context('green_thread')
    host = create_host('http://127.0.0.1:1298/')
    peer1 = host.spawn('peer5', Echo)
    peer1.start()
    serve_forever()