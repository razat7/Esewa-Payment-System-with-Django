import string 
import random
from django.shortcuts import render
from .models import *
def code_generator():
    length = 4
    pw  = string.ascii_letters+string.digits+string.ascii_uppercase
    gen_pw = ''.join(random.choice(pw)for _ in range(length))
    return gen_pw

code = code_generator()
print(code)
