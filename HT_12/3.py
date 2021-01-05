"""
Створіть за допомогою класів та продемонструйте свою реалізацію
шкільної бібліотеки (включіть фантазію).
"""


class PaperItem(object):
    '''
    Main class for all paper items in library.

    Methods:
        __init__(title: str)  --> must have some title
        read(visitor: str)    --> print reader`s name and what he is reading
    '''

    def __init__(self, title):
        self.title = title

    def read(self, visitor):
        print(f'{visitor} are reading "{self.title}"')


class Person(object):
    '''
    Main Class for any person.

    Methods:
        __init__(name: str)  --> must have some name
    '''

    def __init__(self, name):
        self.name = name


class Book(PaperItem):
    '''
    Class for books. Inherits from class PaperItem.

    Attributes: str
        author, genre, pages, year, publisher

    Methods:
        info()  --> print title and all attributes of book
    '''

    author = 'Unknown'
    genre = 'Unknown'
    pages = 'Unknown'
    year = 'Unknown'
    publisher = 'Unknown'

    def info(self):
        print(f'"{self.title}" by {self.author}.\
            \nGenre: {self.genre}\
            \nPublished by "{self.publisher}" in {self.year} year')


class Newspaper(PaperItem):
    '''
    Class for newspapers. Inherits from class PaperItem.

    Attributes: str
        number  --> s/n of newspaper if available
        spec    --> theme, specialization of newspaper

    Methods:
        info()  --> print title and all attributes of book
    '''

    number = 'n/a'
    spec = 'common'

    def info(self):
        print(f'"{self.title}", number {self.number}.\
                \nSpecialization of newspaper: {self.spec}')


class Visitor(Person):
    '''
    Class with all actions for any visitor. Inherits from class Person.

    Attributes:
        all_visitors          --> list of all visitors of library

    Methods:
        take_item(item)       --> take instance of PaperItem and
                                  add to personal own list
        return_item(id: int)  --> remove item with id-position
                                  from personal owm list
        have_item()           --> print personal own list
        read_item(id: int)    --> read item with id-position
                                  in personal owm list
        item_info(id: int)    --> print info about item with id-position
                                  in personal own list
    '''

    all_visitors = []

    def take_item(self, item):
        if len(self.own_items) >= 3:
            print(f'{self.name}, you must return some items!')
        self.item = item
        print(f'{self.name}, you took "{self.item.title}"')
        self.own_items.append(self.item)

    def return_item(self, id):
        self.id = id
        try:
            print(f'{self.name} returned "{self.own_items[id - 1].title}"')
            del self.own_items[id - 1]
        except IndexError:
            print('Wrong number')

    def have_item(self):
        if self.own_items:
            print('Must return:')
            for i, returns in enumerate(self.own_items):
                print(i + 1, returns.title)
        else:
            print('No items to return')

    def read_item(self, id):
        try:
            self.own_items[id - 1].read(self.name)
        except IndexError:
            print('Wrong number')

    def item_info(self, id):
        try:
            self.own_items[id - 1].info()
        except IndexError:
            print('Wrong number')


class Pupil(Visitor):
    '''
    Class for pupils. Inherits from class Visitor.

    Methods:
        __init__(name: str, age: str, p_class: str) --> name, age and classname
        info()  --> print name, age, classname and personal own list
    '''

    def __init__(self, name, age, p_class):
        Visitor.__init__(self, name)
        self.age = age
        self.p_class = p_class
        # add parson to all_visitors list
        self.all_visitors.append(self)
        # personal own list
        self.own_items = []

    def info(self):
        print(f'Name: {self.name}\nAge: {self.age}\nClass: {self.p_class}')
        self.have_item()


class Teacher(Visitor):
    '''
    Class for teachers. Inherits from class Visitor.

    Methods:
        __init__(name: str, subject: str) --> name and teacher`s subject
        info()  --> print name, teacher`s subject and personal own list
    '''

    def __init__(self, name, subject):
        Visitor.__init__(self, name)
        self.subject = subject
        # add parson to all_visitors list
        self.all_visitors.append(self)
        # personal own list
        self.own_items = []

    def info(self):
        print(f'Name: {self.name}\nSubject: {self.subject}')
        self.have_item()


class Librarian(Person):
    '''
    Class for librarian actions. Inherits from class Person.

    Methods:
        check_visitors()        --> print list of all visitors
        check_returns(id: int)  --> print information about visitor
                                    with id-position in all visitors list
    '''

    def check_visitors(self):
        try:
            for i, visitor in enumerate(Visitor.all_visitors):
                print(i + 1, visitor.name)
        except IndexError:
            print('Wrong number')

    def check_returns(self, id):
        try:
            Visitor.all_visitors[id - 1].info()
        except IndexError:
            print('Wrong number')


# books
book_1 = Book('Физика. Основы и механическое движение')
book_1.author = 'Павел Виктор'
book_1.genre = 'Учебники'
book_1.pages = '416'
book_1.publisher = 'BookChef'
book_1.year = '2020'

book_2 = Book('Велика книга тестів. 5-6 років')
book_2.genre = 'Учебники'
book_2.pages = '112'
book_2.publisher = 'Перо'
book_2.year = '2015'

# journal
journal_1 = Newspaper('Журнал Сваты на кухне')
journal_1.number = '3'
journal_1.spec = 'Кулинария'

# pupils
pupil_1 = Pupil('Иннокентий Бест', '13', '7a')
pupil_2 = Pupil('Виктор Павлик', '7', '1b')

# teacher
teach_1 = Teacher('Лучезар Всеволодович', 'Математика')

# librarian
lib_1 = Librarian('Маргарита Людвиговна')

# test
lib_1.check_visitors()
pupil_2.info()
pupil_2.take_item(book_2)
pupil_2.take_item(book_1)
pupil_2.info()
lib_1.check_returns(2)
pupil_1.read_item(1)  # print error
