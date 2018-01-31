#prompt for 5 digit US zip code
#embed zip code in url to www.melissadata.com
#on result page, find <table> element with class = "Tableresultborder";
#there should be only one

#https://www.melissadata.com/lookups/GeoCoder.asp?InData=55403&submit=Search

#find <td> elements with class = "padd" and text like \d{2,3}\.\d{4}
#first one is latitute, second is longitude

#compose url to forecast.weather.gov/MapClick.php using latitude and longitude
#coordinates found in previous step
#example:
#https://forecast.weather.gov/MapClick.php #?lat=44.970570&lon=-93.284044#.WnHvpYgbPIU

import sys, bs4, requests, re

get_geo_data_page_url = r'https://www.melissadata.com/lookups/GeoCoder.asp' #?InData=zipcode&submit=Search'

weather_forcast_url = 'https://forecast.weather.gov/MapClick.php' #'https://www.weather.gov/tg/'

zip_re = re.compile(r'^\d{5}$')

#prompt for zipcode
zip_code = input("Enter 5 digit US zip code: ")
if not zip_code:
    print('Zip code not entered. Program terminated.')
    sys.exit(-999)
elif not zip_re.search(zip_code):
    print('\"{}\" is not a valid zip code. Program terminated.'.format(zip_code))


#inect 'zipcode' in url for geo data and then download
data = {'InData': zip_code}
#download page for processing
geo_data_page = requests.get(get_geo_data_page_url,  params = data)

if geo_data_page.status_code != 200:
    print("Geo data page not downloaded. Program terminated.")
    sys.exit(-999)

#scrape the page for latitude and longitude
geo_data_soup = bs4.BeautifulSoup(geo_data_page.text, 'html.parser')
td_tags = geo_data_soup.findAll("td", class_ = "padd", string = re.compile(r'\d{2,3}\.\d{4}'))
if td_tags != []:
    coords = {'lat': td_tags[0].text, 'lon': td_tags[1].text}
else:
    print('{} is not a valid zip code.'.format(zip_code))
    sys.exit(-999)

          
#download weather forecast page for given geo coordinates
weather_page = requests.get(weather_forcast_url, params = coords)
if weather_page.status_code != 200:
    print('Weather forecast pafe not downloaded. Program terminated.')
    sys.exit(-999)

#analyze page and extract data
weather_soup = bs4.BeautifulSoup(weather_page.text, 'html.parser')
#get location name (city)
city = weather_soup.find("h2", class_ = 'panel-title').text

#get current condition, current temp in F and current temp in C
#look for <p> elements with class myforecast-current*
print('Weather data extracted from forecast.weather.gov\n' + '*' * 40)
p_tags = weather_soup.findAll("p", class_ = re.compile('myforecast-current[a-z-]*', re.I))
print('Current weather conditions in {0} {1}:'.format(city, zip_code))
print('\t' + p_tags[0].text)
print('\tTemperature: {0}/{1}'.format(p_tags[1].text, p_tags[2].text))
print('=' * 40)

#now print the extended forecast
# capitalize selected term, using 'snow' for now
high_light_text = 'snow'
img_tags = weather_soup.findAll("img", class_ = 'forecast-icon')
print('Extended forecast:\n')
for item in list(img_tags):
    #print day in upper case
    title_text = item['title']
    title_parts = title_text.split(':', 1)
    title_text = title_parts[0].upper() + ': ' + title_parts[1]
    title_text = title_text.replace(high_light_text, high_light_text.upper())
    print(title_text + '\n')

    






