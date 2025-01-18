import sys

print("sys.prefix:", sys.prefix)
print("sys.base_prefix:", sys.base_prefix)

if sys.prefix != sys.base_prefix:
    print("You are using a virtual environment.")
else:
    print("You are not using a virtual environment.")