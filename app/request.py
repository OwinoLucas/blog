import urllib.request,json
from .models import Quote


# Getting the news base url
base_url = None

def configure_request(app):
    global base_url
    base_url = app.config['QUOTES_API_BASE_URL']

def get_quotes():
    """
    Function that gets the json response to our url request
    """
    get_quotes_url = base_url

    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quotes_results = None

        if get_quotes_response:
            quotes_list = get_quotes_response
            quotes_results = process_results(quotes_list)

    return quotes_results

def process_results(quotes_list):
    """
    Function that processes the quotes_results and transforms it to a list of objests
    
     Args:
        get_quotes_response: A list of dictionaries that contain quotes details

    Returns :
       quotes_results: A list of quotes objects
    """
    quotes_results = []

    for quotes_item in quotes_list:
        id = quotes_item.get('id')
        author = quotes_item.get('author')
        quote = quotes_item.get('quote')
        permlink = quotes_item.get('permlink')

        if permlink:
            quotes_object = Quote(id,author,quote,permalink)
            quotes_results.append(quotes_object)

    return quotes_results

         


  

