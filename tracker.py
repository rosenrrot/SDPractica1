'''
Tracker server.
'''


from pyactor.context import set_context,create_host,serve_forever,sleep,interval

import random

list_users = {}
files = {'torrentFile1': list_users}

class Echo(object):
    _tell = ['announce','cycle','start']
    _ask = ['get_peers']
    _ref = ['get_peers','announce']

    def announce(self,fichero_torrent,peer_ref):
         if files[fichero_torrent].has_key(peer_ref):
            files[fichero_torrent][peer_ref] = 10
         else:
            files[fichero_torrent][peer_ref] = 10
            print "Included:",peer_ref

    def get_peers(self,fichero_torrent):
        num_elementos = len(files[fichero_torrent])
        list2=files[fichero_torrent].keys()
        random.shuffle(list2)
        if num_elementos > 3:
            num_elementos=3
        list=random.sample(list2,num_elementos)
        return list

    def cycle(self):
        seconds = 0
        list = files['torrentFile1'].keys()
        for i in list:
            seconds = files['torrentFile1'][i]
            if seconds == 0:
                del files['torrentFile1'][i]
                print "removed:", i
            else:
                seconds -= 1
                files['torrentFile1'][i] = seconds

    def __init__(self):
        self.list = []
        self.list2 = []

    def start(self):
        self.interval1 = interval(self.host,1,self.proxy,"cycle")

if __name__=="__main__":
    set_context('green_thread')
    host = create_host('http://127.0.0.1:1285/')
    tracker = host.spawn('tracker', Echo)
    tracker.start()
    serve_forever()