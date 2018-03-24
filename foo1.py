import utils

def get_name_from_symbol(sym):
    url = 'https://www.nasdaq.com/symbol/' + sym
    soup = utils.get_url_soup_no_user_agent(url)
    title_content = soup.find('title').contents[0]
    name = title_content.split('-')[1].strip()
    name = name.strip('Price').strip()

    return name

symbols = ['csco', 'goog', 'fb']
for sym in symbols:
    name = get_name_from_symbol(sym)
    print name

