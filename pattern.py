"""
This program will print out a star pattern using:
1) an if-else statement
2) a single 'for' loop
"""

symbol = ('*')

for i in range (1,10):
    if i <= 5:
        symbol = i * '*'
        print(symbol)
    elif i > 5:
        symbol = (10 - i) * '*'
        print(symbol)