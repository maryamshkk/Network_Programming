import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

''' Request library to build connection with https websites.  ,
    Beautiful library to parse html content,
    urljoin is to combine base url and relative url to an absolute url '''

s = requests.session()
''' request session obj to maintain session active accross multiple requests,
    user-agent is a string that http clients send in the http headers to identify itself'''
s.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"


def get_forms(url):
    '''Function to get all forms'''
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")


def form_details(form):
    '''return form details'''
    details_of_form = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    '''Input list gets extracted details of form'''

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        
        inputs.append({
        ''' extracted details of each field are stored 
            in a dictionary and appends into input list'''

            "type": input_type,
            "name": input_name,
            "value": input_value,
        })

    details_of_form['action'] = action
    details_of_form['method'] = method
    details_of_form['input'] = inputs
    return details_of_form
''' dictionary contains action, method and list of all inputs fields'''

def vulnerable(response):
    '''list of common errors that indicate SQL injection vulnerability '''
    errors = {
        "quoted string not  properly terminated",
        "unclosed question mark after the character string",
        "you have an error in your SQL syntax"
    }
    for error in errors:
        ''' loop checks if any error is found or not and response potential vulnerability'''
        if error in response.content.decode().lower():
            return True   
    return False
    
def sql_injection_scanner(url):
    ''' scanner detects vulnerabilities on a web page 
        by sending harmful inputs(quotes | char)to see
        if it responds with error messages'''
    print(f"Scanning the URL {url} for SQL injection vulnerablities")
    
    forms = get_forms(url)
    '''Retrieves forms from url'''
    print(f'[+] Detected {len(forms)} forms on {url}')

    if not forms:
        '''exiting if no forms are detected'''
        print(f'[!] No forms were detected on the given url. Exiting scan')
        return

    for form in forms:
        ''' Iterate over each form'''
        details = form_details(form)
        print(f'[+] Form details {details}')

    for i in "\"'":
        ''' (' | ") as these interfere with structure of SQL queries '''
        data = {}
        '''for special char i dictionary is created '''
        for input_tag in details['input']:
            '''hidden fields or field with pre-set value'''
            if input_tag['type'] == "hidden" or input_tag['value']:
                data[input_tag['name']] = input_tag['value'] + i
                '''Blocks that are (not hidden | no pre-set value | no submit buttons)'''
            elif input_tag['type'] != "submit":
                data[input_tag['name']] = f"test[{i}]"

    
    form_action_url = urljoin(url, details['action'])
    '''Complete URL where the form submission will be sent'''
    print(f'Submitting form to {form_action_url}')

    
    try:
        '''To catch potential errors when making an HTTP request,
        checks if the method is get or post'''
        if details['method'] == "post":
            res = s.post(form_action_url, data=data)
        else:
            res = s.get(form_action_url, params=data)

        
        if res.status_code == 200:
            '''Checks if the request is successful, server sent back the 
            requested data or confirmation. '''
            if vulnerable(res):
                print(f'[!] SQL injection attack vulnerability in link', (form_action_url))
            else:
                print(f'NO SQL injection attack vulnerability detected', (form_action_url))
        else:
            print(f'Recieved unexpected status code {res.status_code} for {form_action_url}')
    except requests.RequestException as e:
        '''Catches exception during HTTP request (connection errors | timeouts)'''
        print(f'Unexpected error during request: {e}')


if __name__ == "__main__":
    url_to_be_checked = "https://demo.owasp-juice.shop/"
    sql_injection_scanner(url_to_be_checked)