from playcoder.playcoder import transcode_agent
import multiprocessing
import time
import signal

testSource = '/var/local/localms/movies/Sample (2017)/test.mkv'

def main():
    print('Running play')
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = multiprocessing.Pool(2)
    signal.signal(signal.SIGINT, original_sigint_handler)
    m = multiprocessing.Manager()
    try:
        transcodeQueue = m.Queue()
        transcodeAgent = pool.apply_async(transcode_agent, (transcodeQueue,))
        print('Starting transcoder agent')
        transcodeQueue.put(testSource)
        transcodeAgent.get()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        transcodeQueue.put('exit')
        pool.terminate()
    else:
        print("Normal termination")
        pool.close()
    pool.join()

if __name__ == "__main__":
    main()
