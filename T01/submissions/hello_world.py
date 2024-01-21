"""
The following code will perform 3 tasks:
1) ask a user to input their name. After they input their name and press enter, the code will print the name that they had input
2) ask a user to input their age. After they input their age and press enter, the code will print the age that they had input
3) print the string "Hello World!"
"""

name_var = input("please enter your name, then press enter: ")
print(f"Your name is {name_var}")
age_var = input("now please enter your age, then press enter: ")
print("Your age is {}".format(age_var))
print("Hello World!")

