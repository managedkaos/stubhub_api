low_price = 0

base_row = 3
base_tickets = 6
base_price = 300

compare_row = 5
compare_tickets = 6
compare_price = 285

if (compare_price < base_price):
    low_price = compare_price
    base_price = compare_price - 5
else:
    low_price = base_price



print("Low price: {}\nBase price: {}".format(low_price, base_price))
