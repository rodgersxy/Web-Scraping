import sys

def singleton(func):
    instances = {}
    def wrapper(force_new=False, *args, **kwargs):
        if force_new or func not in instances:
            instances[func] = func(*args, **kwargs)
        return instances[func]
    return wrapper

def logger(msg):
    sys.stdout.write('\r')
    # sys.stdout.flush()
    sys.stdout.write(msg)


def clean_xpath_res(l):
    return "\n".join(l).strip()

def _aux_clean_number(number_text):
    return int(number_text[0])