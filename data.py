from pyquery import PyQuery as pq
from urllib2 import HTTPError, urlopen

BASE_URL = 'http://in.finance.yahoo.com/q?s='

def get_content(symbol):
    """
    Returns PyQuery instance with given symbol html data
    """
    # Currently, only BSE, NSE will be added.
    symbol_url = BASE_URL + symbol

    if(symbol_url+'.BS'):
        pq_contents = pq(urlopen(symbol_url).read())
        print 'T'
    else:
        symbol_url+= '.BS'
        pq_contents = pq(urlopen(symbol_url).read())
    return pq_contents

def get_quote(symbol):
    """
    Returns today's stock price
    """
    contents = get_content(symbol)
    return contents('.time_rtq_ticker span').text()

def get_previous_close(symbol):
    """
    Returns yesterday's closing price
    """
    contents = get_content(symbol)
    table1_rows = contents('#table1 tr')
    return float(table1_rows[0].find('td').text)

def get_opening_quote(symbol):
    """
    Returns today's opening stock price
    """
    contents = get_content(symbol)
    table1_rows = contents('#table1 tr')
    return float(table1_rows[1].find('td').text)

def get_todays_change(symbol):
    """
    Returns change in stock price today
    """
    change_price = float(get_quote(symbol)) - float(get_previous_close(symbol))
    return round(change_price, 2)

def get_todays_max(symbol):
    """
    Returns maximum price for today
    """
    contents = get_content(symbol)
    table2_rows = contents('#table2 tr')
    # ah, there is empty span
    text = table2_rows[0].find('td').text_content()
    return float(text.split('-')[0])

def get_todays_min(symbol):
    """
    Returns minimum price for today
    """
    contents = get_content(symbol)
    table2_rows = contents('#table2 tr')
    # ah, there is empty span
    text = table2_rows[0].find('td').text_content()
    return float(text.split('-')[1])

def get_volume(symbol):
    """
    Returns total volume of stock transaction
    """
    contents = get_content(symbol)
    table2_rows = contents('#table2 tr')
    volume = table2_rows[2].find('td').text_content()
    return int(volume.replace(',',''))

def get_summary(symbol):
    """
    Returns dict with stock summery
    """
    contents = get_content(symbol)
    date_time = contents('.time_rtq').text()

    summary = {
        'date_time': date_time,
        'price': get_quote(symbol),
        'previous_close': get_previous_close(symbol),
        'today_open': get_opening_quote(symbol),
        'today_change': get_todays_change(symbol),
        'max_price': get_todays_max(symbol),
        'min_price': get_todays_min(symbol),
        'volume': get_volume(symbol)
    }
    return summary

if __name__ == '__main__':
    symbol = raw_input('Enter the ticker name of BSE or NSE: ')
    #print get_content(symbol)
    print get_summary(symbol)