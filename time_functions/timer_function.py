import time


def time_function(arg):
    def decorator(func):
        def inner():
            start = time.perf_counter()
            value = func()
            print(
                f"The task {name} took {time.perf_counter() - start:0.4f} seconds.")
            return value

        return inner

    if callable(arg):
        name = ""
        return decorator(arg)
    else:
        name = arg
        return decorator
