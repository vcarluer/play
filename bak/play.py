from playcoder.playcoder import transcode_agent
from playscanner.playscanner import scan_agent
import multiprocessing
import signal


def main():
    print('Running play')
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = multiprocessing.Pool(2)
    signal.signal(signal.SIGINT, original_sigint_handler)
    m = multiprocessing.Manager()
    try:
        playQueue = m.Queue()
        print('play transcode')
        transcodeQueue = m.Queue()
        transcodeAgent = pool.apply_async(transcode_agent, (transcodeQueue, playQueue,))
        print('play scan')
        scanQueue = m.Queue()
        scanAgent = pool.apply_async(scan_agent, (scanQueue, playQueue,))
        # srt scanner
        # vtt encoder
        # media move (on transcoded + vtt: file tag?)
        print('play loop')
        doLoop = True
        while doLoop:
            if not playQueue.empty():
                message = playQueue.get()
                print('Play server message received: ' + message)
                msg = message.split(':')
                if msg[0] == 'scan_video':
                    transcodeQueue.put(msg[1])

    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        pool.terminate()
    else:
        print("Normal termination")
        pool.close()
    pool.join()

if __name__ == "__main__":
    main()
