from threading import Thread, Lock
import time

lock = Lock()

def text_to_words(sentence, bucket):
    words = sentence.split(' ')
    lock.acquire()
    for each_word in words:
        bucket.append(each_word)
        time.sleep(0.5) # simulation of IO bound operations (which block the thread execution)
    lock.release()

def text_to_words(sentence, bucket):
    words = sentence.split(' ')
    with lock:  # lock is ackquired here
        for each_word in words:
            bucket.append(each_word)
            time.sleep(0.5) # simulation of IO bound operations (which block the thread execution)
    # lock is released here
    
def main():
    s1 = "this is a quite large sentence to be broken into words by python"
    s2 = "the quick brown fox jumed over the lazy dog"
    words = []
    t1 = Thread(target=text_to_words, args=(s1, words))
    t2 = Thread(target=text_to_words, args=(s2, words))
    threads = [t1, t2]
    # both t1 and t2 use the shared resource "words" for writing
    
    [t.start() for t in threads]
    [t.join() for t in threads]

    print(f'words = {words}')

if __name__ == '__main__':
    main()