"""
The following code will:
1) ask the user to input the following information,
a.  Name
b. Age
c. House number
d. Street name
2) Print a sentence containing all the details provided by the user
"""
name_var = input("Please input your name, then press enter: ")
age_var = input("Please input your age, then press enter: ")
house_var = input("Please input your house number, then press enter: ")
street_var = input("Please input your street, then press enter: ")

print(f"""
Hi {name_var}
Based on your inputs, I now know that your name is {name_var},
you are {age_var} and you live at {house_var} {street_var}.
""")
