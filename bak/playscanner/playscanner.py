testSource = '/var/local/localms/movies/Sample (2017)/test.mkv'

def scan_test(playQueue):
    message = ('scan_video:' + testSource)
    playQueue.put(message)

def scan_agent(queue, playQueue):
    print('Scan agent starting')
    doLoop = True
    # dogwatch on mkv (mp4?)
    scan_test(playQueue)
    while doLoop:
        if not queue.empty():
            source = queue.get()
            if source == 'exit':
                print('Scanner agent exit')
                doLoop = False
