
def load_coin_list(filepath: str = "resources/coin_list.txt") -> str:
    '''
    Return the comma separated values of all the crypto symbols to be used to fetch the data
    ''' 
    with open(filepath, "r") as f:
        coins = f.read().replace('\n',',')
    return coins

