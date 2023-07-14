# index = 0.0588 * L - 0.296 * S - 15.8

# L = letters per 100 words / letters = a-z, A-Z
# S = sentences per 100 words / sentence = number of . ! ?

text = input("Text: ")

letters = 0
sentences = 0
words = 1

for c in text:
    if c == " ":
        words += 1

    elif c in [".", "!", "?"]:
        sentences += 1

    elif c.isalpha():
        letters += 1

L = (letters * 100) / words
S = (sentences * 100) / words

index = (0.0588 * L) - (0.296 * S) - 15.8
rounded = round(index)

if rounded < 1:
    print("Before Grade 1")
elif rounded > 16:
    print("Grade 16+")
else:
    print(f"Grade {rounded}")