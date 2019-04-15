def get_price_bin(price: float) -> float:
    'Convert a given numeric grade into a letter'
    if price >= 650000:
        return 10
    elif price >= 600000:
        return 9
    elif price >= 550000:
        return 8
    elif price >= 500000:
        return 7
    elif price >= 450000:
        return 6
    elif price >= 400000:
        return 5
    elif price >= 350000:
        return 4
    elif price >= 300000:
        return 3
    elif price >= 250000:
        return 2
    elif price >= 200000:
        return 1
def bin_from_diff(diff: float) -> float:
    if diff >= 500000:
        return 20
    elif diff >= 475000:
        return 19
    elif diff >= 450000:
        return 18
    elif diff >= 425000:
        return 17
    elif diff >= 400000:
        return 16
    elif diff >= 375000:
        return 15
    elif diff >= 350000:
        return 14
    elif diff >= 325000:
        return 13
    elif diff >= 300000:
        return 12
    elif diff >= 275000:
        return 11
    elif diff >= 250000:
        return 10
    elif diff >= 225000:
        return 9
    elif diff >= 200000:
        return 8
    elif diff >= 175000:
        return 7
    elif diff >= 150000:
        return 6
    elif diff >= 125000:
        return 5
    elif diff >= 100000:
        return 4
    elif diff >= 75000:
        return 3
    elif diff >= 50000:
        return 2
    elif diff >= 25000:
        return 1