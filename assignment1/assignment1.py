#assignment 1
def hello():
    return "Hello!"

#assignment 2 
def greet(name):
    return f"Hello, {name}!"

#assignment 3



def calc(a, b, operation="multiply"):
    try:
        if operation == "multiply":
            return a * b
        if operation == "add":
            return a + b
        if operation == "divide":
            return a / b
        if operation == "subtract":
            return a - b
        if operation == "modulo":
            return a % b
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return f"You can't {operation} those values!"
    
#assignment 4


def data_type_conversion(value, data_type):
    try:
        if data_type == "int":
            return int(value)
        if data_type == "float":
            return float(value)
        if data_type == "str":
            return str(value)
    except ValueError:
        return f"You can't convert {value} into a {data_type}."

#assignment 5

def grade(*args):
    try:
        average = sum(args) / len(args)

        if average >= 90:
            return "A"
        if average >= 80:
            return "B"
        if average >= 70:
            return "C"
        if average >= 60:
            return "D"
        return "F"

    except TypeError:
        return "Invalid data was provided."
#assignment 6

def repeat(text, count):
    return text * count
#assignemnt 7


def student_scores(option, **kwargs):
    if option == "mean":
        return sum(kwargs.values()) / len(kwargs)

    if option == "best":
        return max(kwargs, key=kwargs.get)
#assignment 8

def titleize(title):
    small_words = ["and", "or", "the"]

    words = title.split()
    result = []

    for i, word in enumerate(words):
        if i == 0 or word not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word)

    return " ".join(result)
#assignment 9

def hangman(secret_word, guessed_letters):
    result = ""

    for letter in secret_word:
        if letter in guessed_letters:
            result += letter
        else:
            result += "_"

    return result
#assignment 10

def pig_latin(text):
    def convert_word(word):
        vowels = "aeiou"

        if word[0].lower() in vowels:
            return word + "ay"

        for i in range(len(word)):
            if word[i].lower() in vowels:
                if i > 0 and word[i - 1].lower() == "q":
                    return word[i + 1:] + word[:i + 1] + "ay"
                return word[i:] + word[:i] + "ay"

    words = text.split()
    converted = [convert_word(word) for word in words]
    return " ".join(converted)
   
