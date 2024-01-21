"""
This program will determine the award a person  competing in a triathlon
will receive based on the sum of their time (in minutes)
for each of the 3 triathlon events:
- simming
- cycling
- running
The award will be based on the following rules,
where 100 minutes is the qualifying time:
- if 0-100 minutes, then "Provincial Colours"
- if 101-105 minutes, then "Provincial Half Colours"
- if 106-110 minutes, then "Provincial Scroll"
- if > 110 minutes, then "No award"
"""

swimming = int(input("enter your time, in minutes, for the swimming event: "))
cycling = int(input("enter your time, in minutes, for the cycling event: "))
running = int(input("enter your time, in minutes, for the running event: "))
total_time = swimming + cycling + running

if total_time <= 100:
    print(f"""
    Your total time was {total_time} minutes,
    which is within the qualifying time
    and you have been awarded "Provincial Colours".
    Congratulations!""")

elif total_time > 100 and total_time <= 105:
    print(f"""
    Your total time was {total_time} minutes,
    which is within 5 minutes of the qualifying time
    and you have been awarded "Provincial Half Colours".
    Great effort!""")

elif total_time > 105 and total_time <= 110:
    print(f"""
    Your total time was {total_time} minutes,
    which is within 10 minutes of the qualifying time
    and you have been awarded "Provincial Scroll".
    Good effort!""")

elif total_time > 110:
    print(f"""
    Your total time was {total_time} minutes,
    which is more than 10 minutes off the qualifying time
    and means you have not qualified for an award.
    Better luck next time!""")

else:
    print("somthing seems to have gone wrong, please rerun the program.")