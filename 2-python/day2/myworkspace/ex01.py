from threading import current_thread
import time


def function1(message="hello, world!", delay=1):
    for i in range(10):
        print(f'{message} (in a thread called {current_thread().name})')  
        time.sleep(delay)

def main():
    print(f'starting of main() in a thread called {current_thread().name}')
    function1()
    function1("welcome to threading", 0.5)
    print(f'ending of main() in a thread called {current_thread().name}')


if __name__ == '__main__':
    main()