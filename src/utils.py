# -*- coding: utf-8 -*-

def factorial(n):
    """ return n! where 'n' is an integer """

    if(n == 1 or n == 0):
        return 1
    else:
        return n*factorial(n-1)
        

def combination(n, k):
    """ return nCk where n and k are integers """

    num = factorial(n)
    denom = factorial(n-k)*factorial(k)
    return num/denom