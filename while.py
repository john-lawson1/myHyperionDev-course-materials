"""This program will perform the following tasks:
    1) continually ask the user to enter a number
    2) stop asking the user to enter a number when the user enters -1
    3) calculate the average of all the numbers entered by the user, except -1
"""

list_of_num = []
user_input = 0
user_sum = 0

print ("""***This programm will calculate the average of a list of positive \
numbers***\n""")

while user_input != -1:
    user_input = int(input("""Please enter a number, as an integer, \
or enter -1 to stop: """))
    if user_input == -1:
        break
    list_of_num.append(user_input)
    user_sum += user_input

print()
print("=" * 79)
print(f"""You entered {len(list_of_num)} positive numbers.
The average of the numbers you entered is {user_sum / len(list_of_num)}""")
print("=" * 79)