# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.


# 1
def superFn(fn, *args):
    for el in args:
        fn(el)
    # [fn(el) for el in args]
    # return fn()


# 2-3
superFn(lambda a: print(a), 1, 2, 3, 4, 5)

# 4 
superFn(lambda a: print(f'Result:{a:^20}'), 1, 2, 3, 4, 5)

