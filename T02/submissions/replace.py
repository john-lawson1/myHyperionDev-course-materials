""" This code will:
1) Save the sentence:
“The!quick!brown!fox!jumps!over!the!lazy!dog.” as a single string.
2) Reprint this sentence as “The quick brown fox jumps over the lazy
dog.” using the replace() function to replace every “!” exclamation
mark with a blank space.
3) Reprint that sentence as: “THE QUICK BROWN FOX JUMPS OVER
THE LAZY DOG.” using the upper() function
4) Reprint the sentence in reverse
"""

sentence = "The!quick!brown!fox!jumps!over!the!lazy!dog."
sentence_1 = sentence.replace("!"," ")
sentence_2 = sentence_1.upper()
sentence_3 = sentence[::-1]

print(f"The original sentence is:\n{sentence}\n")
print(f"The sentence with \"!\" replaced by a blank space is:\n{sentence_1}\n")
print(f"The sentence in capital letters is:\n{sentence_2}\n")
print(f"The sentence in reverse is:\n{sentence_3}\n")

