low_price = 0
adjustment = 5

base_row = 3
base_tickets = 6
base_price = 300
min_price = 135

compare_row = 5
compare_tickets = 6
compare_price = 285

prices = [300, 300, 300, 295, 295, 230, 225, 200, 215, 170, 170, 150, 140, 130, 130, 130, 1]

for price in prices:
    price_change = False
    min_price_reached = False

    if (price < base_price):
        price_change = True
        low_price = price

        if (base_price - adjustment) > min_price:
            base_price = price - adjustment
        else:
            min_price_reached = True
    else:
        low_price = base_price

    print("Price change: {}\tMin reached: {}\tLow price: {}\tBase price: {}".format(price_change, min_price_reached, low_price, base_price))


