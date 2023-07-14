while True:
    try:
        height = int(input("Height: "))
        if height < 1 or height > 8:
            raise ValueError()
        break
    except ValueError:
        pass

j = height - 1
for i in range(height):
    print(" " * j, end="")
    print("#" * (i + 1))
    j -= 1