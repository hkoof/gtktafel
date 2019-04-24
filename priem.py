#!/usr/bin/env python3

def heeft_delers(getal, deler=2):
    return getal != deler and not getal % deler or not deler**2 >= getal and heeft_delers(getal, deler + 1)

def print_priems_tot(getal=200):
    getal > 2 and print_priems_tot(getal - 1) or heeft_delers(getal) or print(getal)

print_priems_tot(200)
