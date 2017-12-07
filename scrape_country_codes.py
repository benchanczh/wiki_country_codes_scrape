from bs4 import BeautifulSoup
import requests


base_url = "https://en.wikipedia.org"
country_code_url = base_url + "/wiki/Country_code"

# Get wikipedia page
html = requests.get(country_code_url)

# Create BeautifulSoup object from the web page content
bs_obj = BeautifulSoup(html.text, "lxml")

country_urls = []

# For each BeautifulSoup object with tag 'a',
# find the attribute 'href' which starts with '/wiki/Country_code'
for element_a in bs_obj.find_all(name="a"):
    if element_a.attrs.get("href", " ").startswith("/wiki/Country_code"):
        country_urls.append(element_a["href"])


def get_country_details(url):
    # Get the web page
    country_html = requests.get(base_url + url)

    # Create BeautifulSoup object from the web page content
    country_bs_obj = BeautifulSoup(country_html.text, "lxml")

    # Find all elements that holds the country name
    country_name_elements = country_bs_obj.find_all(name="span", attrs="mw-headline")
    countries_data = []

    # Retrieve data from each element
    for country_name_element in country_name_elements:
        # For each element, find the country table
        country_table = country_name_element.parent.find_next("table")
        if not country_table:
            continue

        # Find all td tags in the country table
        tds = country_table.find_all("td")

        country_data = {}
        # For each td tag, save data with tag a as key and tag span as value
        for td in tds:
            country_data.update({td.find("a").text: td.find("span").text})

        # Add the country name and wikipedia url for the country
        country_name_element_a = country_name_element.find("a")
        country_data["country_name"] = country_name_element_a.text.replace("\n", "").strip()
        country_data["country_url"] = base_url + country_name_element_a["href"]
        countries_data.append(country_data)

    return(countries_data)


# test the function
get_country_details(country_urls[2])
