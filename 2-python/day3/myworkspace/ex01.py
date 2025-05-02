class Book:
    # any member variable created in this part of the class
    # becomes a static member (shared by all object)
    def __init__(self, **kwargs):
        # this equivalent of a constructor in C++ or Java
        # Python interpreter calls this function when an object
        # is created, and supplies the reference of the newly created object
        # as the first argument (`self`), which can now be used for adding
        # additional member variables to the object
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.price = kwargs.get('price')

    def __repr__(self):
        return f'Book(title="{self.title}", author="{self.author}", price={self.price})'
    
    def print(self):
        print(f'Title  : {self.title}')
        print(f'Author : {self.author}')
        print(f'Price  : ₹{self.price}')

def main():
    b1 = Book(title="Let us C", author="Y Kanitkar", price=499.0)  # create a new object
    b2 = Book(title="Python Unleashed", price=2999.0)  # create another object

    print(b1)  # here __repr__ or __str__ is called implicitly by the `print` method
    print(b2)

if __name__ == '__main__':
    main()
