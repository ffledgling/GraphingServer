""" This module contains all the custom functions used throughout """

def identity(x):
    return x

def convert1(l):
    return l[0], l[1]

def Gbpu(l):
    """ Gb/unit vs unit """
    return float(l[1])/1024**3, float(l[0]) 
