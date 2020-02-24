#################################
##### Name:
##### Uniqname:
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key

BASE_URL = "https://www.nps.gov"

class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone): # TODO Add defaults?
        self.category = category #TODO ADD CONDITIONAL CHECKING?
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone
        

    def info(self):
        '''Returns a string representation of itself

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string representation of itself #TODO maybe make this better
        '''

        return f"{self.name} ({self.category}): {self.address} {self.zipcode}" #TODO convert zip to str?
    pass


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''

    state_url_dict = {}
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    state_anchor_tags = soup.find(class_ = "dropdown-menu SearchBar-keywordSearch").find_all("a")    
    
    for tag in state_anchor_tags:
        state_url_dict[tag.text.lower()] = BASE_URL + tag["href"]
    
    return state_url_dict

def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''

    response = requests.get(site_url)
    soup = BeautifulSoup(response.text, "html.parser")

    category = soup.find(class_ = "Hero-designation").text.strip()
    name = soup.find(class_ = "Hero-title").text.strip()
    zipcode = soup.find(class_ = "postal-code").text.strip()
    phone = soup.find(class_ = "tel").text.strip()

    city = soup.find(attrs = {"itemprop": "addressLocality"}).text.strip()
    state = soup.find(attrs = {"itemprop": "addressRegion"}).text.strip()
    address = city + ", " + state

    site_instance = NationalSite(category,name,address,zipcode,phone)
    
    return site_instance


def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    pass


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    pass
    

if __name__ == "__main__":
    build_state_url_dict()
    get_site_instance("https://www.nps.gov/isro/index.htm")
    pass