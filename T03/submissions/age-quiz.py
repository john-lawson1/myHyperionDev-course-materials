"""This code will:
1) take in a user’s age and store it in an integer variable called age
2) output a variety of responses determined by the data the user enters,
- If the user is 40 or over, output the message "You're over the hill."
- Assume that the oldest someone can be is 100; if the user enters a
higher number, output the message "Sorry, you're dead.".
- If the user is 65 or older, output the message "Enjoy your retirement!"
- If the user is under 13, output the message "You qualify for the kiddie
discount."
- If the user is 21, output the message "Congrats on your 21st!"
- For any other age, output the message "Age is but a number."
"""

age = int(input("please enter your age as an integer:"))

if age > 100:
    print("Sorry, you're dead!")

elif age >= 65 and age <= 100:
    print("Enjoy your retirement!")

elif age >= 40 and age < 65:
    print("You're over the hill.")

elif age < 13:
    print("You qualify for the kiddie discount.")

elif age ==21:
    print("Congrats on your 21st!")
    
else:
    print("Age is but a number.")
