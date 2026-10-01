## Make objects from mymod.py available as mypkg.foo rather than mypkg.mymod.foo.
## The "." is a "relative" import that means "find 'mymod' here in this directory".
from .mymod import *

print("Welcome to my package.")
