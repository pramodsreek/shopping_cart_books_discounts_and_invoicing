#!/usr/bin/python3
"""
Solution/Algorithm
1. Get the books in shopping cart and get the series of books with discount.
2. Get the pricing model to calculate the discounts based on combination of books.
3. Both the lists i.e. Shopping Cart and series were converted to set to use symmetric_difference to separate all books in the shopping cart that are not in the series. Symmetric difference gives the additional books in the series that are not in the shopping cart as well. To avoid any incorrect operation, a subset operation was used to confirm the books that are in the symmetric difference belongs to shopping cart.
5. Books are objects of Book class. They cannot be used for grouping and discounting. There is a property called ISBN for the book. This is used for grouping and a hashtable is maintained. (If a database was used, the implementation would be different. )
4. Split the books in shopping cart to multiple lists based on the series, to have exactly one copy of a book in the series in the split list. The maximum number of split lists is the maximum number of a single book of the series in shopping cart. For example Book1 has 5 copies, Book4 has 3 copies -> the maximum number of sublists can be 5 copies. 
5. Use set operation intersection to identify the split set and store it in a separate list (list of lists).
6. Subtract the previous sublist and subtract it from copy of shopping cart and perform another intersection to get another sublist. Continue till the shopping cart is empty and maximum number of sublist available is reached. 
7. Calculate the price of individual books and discounts if applicable and then calculate the total price. 
"""
from collections import Counter

import logging

# A logger is used to avoid writing everything to screen and it is easier to identify issues.
logging.basicConfig(filename='discounting_book_series.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running Discount For Books in a Series")

LOGGER = logging.getLogger('DiscountingBookSeries')

class Book():
    '''
    The Book object contains ISBN. It is the most important property to identify a book. It cannot identify individual copies, but other unique characteristics of the book. It is the main property used for grouping and discounting. (In this code, all the rules of ISBN are not applied. ) 
    :param isbn: ISBN of the book
    :type isbn: str
    :param title: Title of the book
    :type title: str
    :param price: Price of the book
    '''
    def __init__(self, isbn, title, price):
        LOGGER.debug(f"Creating a book {isbn}")
        self.isbn = isbn
        self.title = title
        self.price = price

    def get_isbn(self):
        '''
        A getter method to get ISBN of the book. 
        :returns: isbn
        :rtype: str
        '''
        return self.isbn

    def get_title(self):
        '''
        A getter method to get title of the book.
        :returns: title
        :rtype: str
        '''
        return self.title

    def get_price(self):
        '''
        A getter method to get price of the book.
        :returns: price
        :rtype: float
        '''
        return self.price

class Pricing():
    '''
    Pricing object helps to encapsulate all the data, rules and methods to set up a specific pricing model.  
    :param series_of_books: Series of books that is eligible to use this pricing model.
    :type series_of_books: list
    '''
    def __init__(self, series_of_books):
        LOGGER.debug(f"Creating a pricing model for series_of_books")
        if type(series_of_books) == list:
            self.series_of_books = series_of_books
        else:
            self.series_of_books = []

    def get_discount_percentage(self, set_of_books):
        '''A method to return the discount applicable to a collection of books the customer wishes to purchase. The following discounts apply.

        a 5% discount is applied if two different books from the series are purchased
        a 10% discount is applied if three different books from the series are purchased
        a 20% discount is applied if four different books from the series are purchased
        a 25% discount is applied if all five books from the series are purchased

        :param set_of_books: A grouping of books from collection of books that the customer wishes to purchase to calculate the discount.
        :type set_of_books: list
        
        :returns: percentage_discount
        :rtype: int
        ''' 
        if type(set_of_books) == list:
            if len(set_of_books) == 5:
                percentage_discount = 25
            elif len(set_of_books) == 4:
                percentage_discount = 20
            elif len(set_of_books) == 3:
                percentage_discount = 10
            elif len(set_of_books) == 2:
                percentage_discount = 5
            else:
                percentage_discount = 0
        else:
            print("Unable to find discount for this set!")

        return percentage_discount


class CustomerShoppingCart():
    '''Shopping cart contains all the books that customer has selected to buy. It is mandatory to have a valid cart with books to create an instance of CustomerShoppingCart. 

    :param books_in_cart: A collection of books that the customer wishes to purchase.
    :type books_in_cart: list
    :ivar dict_books_in_cart: Mapping ISBN to Objects
    :vartype dict_books_in_cart: dict
    :raises: :class:`Exception`: Shopping Cart is empty.
    ''' 
    def __init__(self, books_in_cart):
        
        LOGGER.debug("Creating a shopping cart.")
        if type(books_in_cart) == list and len(books_in_cart) != 0:
            self.books_in_cart = books_in_cart
        else:
            LOGGER.warning('Shopping Cart is Empty!')
            raise Exception('Shopping Cart is Empty!')
        
        # not a good solution, needs modification later to identify each individual copy of the book.
        self.dict_books_in_cart = dict()
        for book in books_in_cart:
            self.dict_books_in_cart[book.get_isbn()] = book
        
    def set_series_of_books(self, series_of_books):
        '''Used to set the series of books for discounting purpose. Series can be empty, then there will be no discounts applied.

        :param series_of_books: A collection of books that belongs to a series with discounts.
        :type series_of_books: list
        :cvar pricing: pricing model to be used for the series of books
        :vartype pricing: Pricing
        ''' 
        if type(series_of_books) == list:
            self.series_of_books = series_of_books
            pricing = Pricing(series_of_books)
            self.pricing = pricing
        else:
            self.series_of_books = []

    def subtract_list(self, larger_list, smaller_list):
        '''A helper method to subtract a smaller list from larger list. It should be part of utility package. 

        :param larger_list: A list that requires removal of some of its items.
        :type larger_list: list
        :param smaller_list: A list that has the items that should be removed from larger list.
        :type smaller_list: list
        :returns: subracted_list
        :rtype: list
        ''' 
        counter1 = Counter(larger_list)
        counter2 = Counter(smaller_list)
        difference = counter1 - counter2
        return list(difference.elements())

    def get_object_for_isbn(self, isbn):
        '''
        A getter method to get instance of a book mapped to ISBN.
        :param isbn: ISBN of the book
        :type isbn: str
        :returns: book
        :rtype: Book
        '''
        return self.dict_books_in_cart[isbn]

    def print(self, set_of_books):
        '''
        This method is used to avoid printing objects that makes no sense. The properties of objects are extracted and printed. It can be used for printing to logs and terminal.
        :param set_of_books: list of books
        :type set_of_books: list
        :returns: book
        :rtype: Book
        '''
        print_string = ''
        for book in set_of_books:
            if print_string == '':
                print_string = book.get_title()
            else:
                print_string = print_string + " + " + book.get_title()
        print_string = "[" + print_string + "]"
        return print_string

    def calculate_discount(self, set_of_books):
        '''
        Calculates the discounts applicable to combination of books in a series. It calculates discounts in dollar value and percentage. 
        :param set_of_books: list of books
        :type set_of_books: list
        :returns: discount_in_dollars
        :rtype: float
        :returns: percentage_discount
        :rtype: int
        '''
        discount_in_dollars = 0
        percentage_discount = 0
        price_of_books = 0

        if type(set_of_books) == list: 
            if isinstance(self.pricing, Pricing):
                percentage_discount = self.pricing.get_discount_percentage(set_of_books)
                for book in set_of_books:
                    price_of_books += book.get_price()
                discount_in_dollars = price_of_books * percentage_discount/100
            else:
                percentage_discount = 0
                discount_in_dollars = 0
        return (discount_in_dollars, percentage_discount)

    def calculate_total_price(self):
        '''
        Calculates the total price including discounts for books in this shopping cart.  
        :returns: total_price
        :rtype: float
        '''
        total_price = 0.0

        if type(self.series_of_books) == list and len(self.series_of_books) != 0:
            # helps to get the maximum number of sublist based on the series. (details documented above in algorithm section)
            max_count_of_a_book = 0

            #convert series of books to series of ISBN's
            isbn_series_of_books = []
            isbn_books_in_cart = []

            for book in self.series_of_books:
                isbn_series_of_books.append(book.get_isbn())

            for book in self.books_in_cart:
                isbn_books_in_cart.append(book.get_isbn())

            for isbn_series in isbn_books_in_cart:
                if isbn_books_in_cart.count(isbn_series) > max_count_of_a_book:
                    max_count_of_a_book = isbn_books_in_cart.count(isbn_series)

            LOGGER.debug(f'Max count of book is {max_count_of_a_book}')

            # identifies books that are not in series but are in shopping cart.
            unknown_isbn_list = list(set(isbn_books_in_cart).symmetric_difference(set(isbn_series_of_books)))

            # geting book object mapped to isbn
            if set(unknown_isbn_list).issubset(set(isbn_books_in_cart)):    
                unknown_book_list = []
                for isbn_unknown in unknown_isbn_list:
                    unknown_book_list.append(self.get_object_for_isbn(isbn_unknown))
                LOGGER.debug(f'The following books are not in database : ')
                for unknown_book in unknown_book_list:
                    LOGGER.warning(f'Error - {unknown_book.get_title()}({unknown_book.get_isbn()}) is priced Zero to avoid inconvinience for Customer!')
                    print(f'Error - {unknown_book.get_title()}({unknown_book.get_isbn()}) is priced Zero to avoid inconvinience for Customer!')
                    self.books_in_cart.remove(unknown_book)
                #print('new list of books after removing unknown books : ')
                #for book in self.books_in_cart:
                #    print(f'{book.get_title()}-{book.get_isbn()}')
            else:
                LOGGER.debug("All books in list are valid!")

            # split books in shopping cart to multiple lists to help with applying discounts. Sets are not always used as it will delete duplicate ISBN's. 
            split_books_isbn_to_discount = [] 
            
            for i in range(max_count_of_a_book):
                isbn_extracted_combination = list(set(isbn_series_of_books).intersection(set(isbn_books_in_cart)))
                split_books_isbn_to_discount.append(isbn_extracted_combination)
                #print(f'counter{i}')
                if i != max_count_of_a_book:
                    isbn_books_in_cart = self.subtract_list(isbn_books_in_cart, isbn_extracted_combination)

            LOGGER.debug(split_books_isbn_to_discount)


            if type(split_books_isbn_to_discount) == list:
                for set_of_isbns in split_books_isbn_to_discount:
                    set_of_books = []
                    for isbn in set_of_isbns:
                        set_of_books.append(self.get_object_for_isbn(isbn))
                    for book in set_of_books:
                        LOGGER.debug(f'{book.get_title()} : {book.get_price()}')
                        total_price += book.get_price()
                    (discount_in_dollars, percentage_discount) = self.calculate_discount(set_of_books)
                    total_price -= discount_in_dollars
                    LOGGER.debug(f'{self.print(set_of_books)} discounted at {percentage_discount}% : -{discount_in_dollars}')

            else:
                LOGGER.debug("Unable to calculate discount!")
        else:
            LOGGER.debug("No Discounts Applicable!")
            for book in self.books_in_cart:
                LOGGER.debug(f'{book.get_title()} : {book.get_price()}')
                total_price += book.get_price()
        return total_price

if __name__ == "__main__":

    ''' A simple case of this would be:
        customerShoppingCart([book1, book2, book3]) => $21.60
        A more complex case using the pricing model is:
        customerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5]) => $51.60
    '''

    # Create five books in series and a book not in series
    # Cost of single copy of book is $8.0
    book1 = Book('ISBN-111', 'Young Wizard - Series 1', 8.0)
    book2 = Book('ISBN-222', 'Young Wizard - Series 2', 8.0)
    book3 = Book('ISBN-333', 'Young Wizard - Series 3', 8.0)
    book4 = Book('ISBN-444', 'Young Wizard - Series 4', 8.0)
    book5 = Book('ISBN-555', 'Young Wizard - Series 5', 8.0)

    book9 = Book('ISBN-UNKNOWN', 'XXXXXXXXX', 0.0)
    # books created

    # create the series of books
    series_of_books = [book1, book2, book3, book4, book5]

    print('\n######################## Test Scenario 1 from sample########')
    customerShoppingCart = CustomerShoppingCart([book1, book2, book3])
    customerShoppingCart.set_series_of_books(series_of_books)
    print(f'customerShoppingCart([book1, book2, book3]) => ${customerShoppingCart.calculate_total_price()}')

    print('\n######################## Test Scenario 2 from sample########')
    customerShoppingCart = CustomerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5])
    customerShoppingCart.set_series_of_books(series_of_books)
    print(f'customerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5]) => ${customerShoppingCart.calculate_total_price()}')

    print('\n#########Testing Scenario where one of the books has invalid entry in system.#######')
    list_of_books = [book1, book2, book3, book4, book5, book1, book3, book5,book1, book2, book3, book1, book9]
    customerShoppingCart = CustomerShoppingCart(list_of_books)
    customerShoppingCart.set_series_of_books(series_of_books)
    print(f'customerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5, book9]) => ${customerShoppingCart.calculate_total_price()}')

    print('\n#########Testing Scenario where no discount in applied.#######')
    customerShoppingCart = CustomerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5])
    customerShoppingCart.set_series_of_books([])
    print(f'customerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5]) => ${customerShoppingCart.calculate_total_price()}')

    print('\n########Testing Exception where shopping cart is empty.######')
    try:
        customerShoppingCart = CustomerShoppingCart([])
        customerShoppingCart.set_series_of_books([])
        print(f'customerShoppingCart([book1, book2, book3, book4, book5, book1, book3, book5]) => ${customerShoppingCart.calculate_total_price()}')
    except Exception as identifier:
        print(identifier)