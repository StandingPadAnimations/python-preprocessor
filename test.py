#ifdef ANNOTATIONS
def example(val: str) -> str:
    return val + " World"
#elsedef
def example(val):
    return val + " World"
# endif

res = example("Hello")
print(res)
