
def custom_fench(exp:str = "+"):
    def fench(func):
        def wrapper(txt:str):
            print(exp*len(txt))
            func(txt)
            print(exp*len(txt))

        return wrapper
        
    return fench

@custom_fench("=")
def sad(txt:str):
    print(txt)



sad("saddest life")