from ex01 import Book

def main():
    b1 = Book(title='C++ exaplained', author='Vinod')
    b1.price = 1200
    print(f'The book {b1.title} is written by {b1.author}')

    b1.print()

if __name__ == '__main__':
    main()