# weather-scraper
A Python 3 web scraping script to extract the current weather and extended forecast for a given US zip code.
The script prompts the user for a 5 digit code and then calls a web service at www.melissadata.com that converts
the zip code to latitude and longitude coordinates, which are in turn passed to forecast.weather.gov. The script
extracts the desired information and displays it to the console. It can highlight (capitalize) a term specified
in the code (or perhaps by the user). By default the highlighted term is "SNOW".
