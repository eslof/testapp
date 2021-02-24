import locale
import os
import subprocess
import sys
from typing import List
exe = sys.executable
head, tail = os.path.split(exe)


def print_and_call(app_args: List[str]):
    statement = [exe, "app.pyz"] + app_args
    print(' '.join([tail, "app.pyz"] + app_args))
    r = subprocess.check_output(statement).decode(locale.getpreferredencoding()).replace('\r\n', '').strip()
    print(r)
    return r


ret = print_and_call(["login", "ola", "123"])
token_ola = ret[-9:].strip()
print_and_call(["balance", token_ola])
print_and_call(["deposit", token_ola, "100"])
print_and_call(["withdraw", token_ola, "25"])
print_and_call(["balance", token_ola])
print()
ret = print_and_call(["login", "ingvar", "456"])
token_ingvar = ret[-9:].strip()
print_and_call(["deposit", token_ingvar, "500"])
print_and_call(["transfer", token_ingvar, "ola", "400"])
print()
print_and_call(["balance", token_ola])