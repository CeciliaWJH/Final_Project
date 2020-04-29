#########################################
##### Name: Wen-Jye Hu              #####
##### Uniqname: huwenjye            #####
#########################################

import json
import requests
import secrets # file that contains your OAuth credentials

CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = []

api_key = secrets.OPEN_WEATHER_API_KEY

def open_city():
    ''' Opens the city list file
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened city list: list
    '''
    cache_file = open("city_list.json", 'r')
    cache_contents = cache_file.read()
    cache_dict = json.loads(cache_contents)
    cache_file.close()

    return cache_dict


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = []
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current cache_dict (city data) to cache
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def make_request_by_city(city):
    '''Check the cache for a saved city for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    city: dict
        The id number of the user-specified city

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache or 
        from web requests
        JSON
    '''
    #TODO Implement function
    for c in CACHE_DICT:
        if (c["id"] == city["id"]):
            print("cache hit! city_id=", city["id"], "city_name=", city["name"])
            return c

    print("cache miss! city_id=", city["id"], "city_name=", city["name"])
    baseurl = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q": city["name"],
        "appid": api_key
    }
    CACHE_DICT.append(requests.get(baseurl, params=params).json())
    save_cache(CACHE_DICT)
    return CACHE_DICT[-1]


if __name__ == "__main__":
    CITY_DICT= open_city()
    CACHE_DICT = open_cache()
    while(True):
        city_list = []
        response = input("Which city weather do you want to know?   ")
        if(response.lower() == "exit"):
            break
        for city in CITY_DICT:
            if(city["name"].lower() == response.lower()):  # the city exists
                city_list.append(city)
#                print(city)
        if(len(city_list) == 0):
            print("The city doesn't exist. Please enter an existed city name.")
            continue
        elif(len(city_list) == 1):
            # use requests.get() to grab the data
            print(make_request_by_city(city_list[0]))
            # print all data out in user friendly format
        else:
            while(True):
                count = 1 
                for c in city_list:
                    print(count, ":", c)
                    count = count + 1
                resp = input("Please specify the city number: ")
                if resp.isnumeric():
                    resp_num = int(resp)
                    if(resp_num>0 and resp_num<=len(city_list)):
                        # use requests.get(city_list[resp_num-1]) to grab the data
                        print(make_request_by_city(city_list[resp_num-1]))
                        # print all data out in user friendly format
                        break

