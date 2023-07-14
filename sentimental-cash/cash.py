from cs50 import get_float

while True:
    try:
        change = get_float("Change owed: ")
        change = int(change * 100)
        if change >= 1:
            break
        else:
            raise ValueError
    except ValueError:
        pass


coin25 = change // 25
change %= 25

coin10 = change // 10
change %= 10

coin5 = change // 5
change %= 5

coin1 = change

coins = coin25 + coin10 + coin5 + coin1
print(coins)