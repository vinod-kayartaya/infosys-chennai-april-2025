from threading import Thread, current_thread
import time

def function1(message="hello, world!", delay=1):
    for i in range(10):
        print(f'{message} (in a thread called {current_thread().name})')  
        time.sleep(delay)

def main():
    print(f'starting of main() in a thread called {current_thread().name}')
    t1 = Thread(target=function1, name="t1")
    t2 = Thread(target=function1, args = ("Welcome to threading", 0.1), name="t2")
    t1.start() # sets up the thread (allocate a new stack, add to scheduler etc)
    t2.start() # sets up the thread (allocate a new stack, add to scheduler etc)
    t1.join() # wait for t1 to finish the target task (thread's run() method)
    t2.join() # wait for t1 to finish the target task (thread's run() method)
    print(f'ending of main() in a thread called {current_thread().name}')

if __name__ == '__main__':
    main()