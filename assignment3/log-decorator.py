#Task 1: Writing and Testing a Decorator
import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs) 
            logger.log(logging.INFO, f"function: {func.__name__}")
            logger.log(logging.INFO, f"positional parameters: {args}")
            logger.log(logging.INFO, f"keyword parameters: {kwargs}")
            logger.log(logging.INFO, f"return: {result}")
            return result
        return inner

@logger_decorator
def hello():
    print("Hello, World!")

@logger_decorator
def positional_args_function(*args):
    return True

@logger_decorator
def keyword_args_function(**kwargs):
    return logger_decorator

hello()

positional_args_function(1, 2, 3)

keyword_args_function(name="Heather", age=30)
