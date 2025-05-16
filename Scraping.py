from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd

# scraping sandali divari website of nilper to get price and product data

website = "https://store.nilper.ir/%D8%B5%D9%86%D8%AF%D9%84%DB%8C-%D8%A7%D8%AF%D8%A7%D8%B1%DB%8C"
path = "chromedriver.exe"

# headless-mode
options = Options()
options.headless = True

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options = options)

driver.get(website)

# XPath Syntax
# //tagName[@AttributeName="Value"]
# //tagName[@AttributeName="Value"]/text()


# example --> //div[@class="full-script"]/text()
# example --> //p[(@class="plot") or (@class="plot2")]/text()
# example --> //p[contains((@class,"plot")]/text()


# / --> means the children form the node set on the left side of this character
# // --> specifies that the matching node set should be located at any level within the document
 

 # xpath <p class="price same">   ---> //p[@class="price same"]
# xpath <p class="price same">   ---> //div[@class="caption"]/h4/a/text()

containers = driver.find_elements(by="xpath", value='//div[@class="caption"]')
containers_images = driver.find_elements(by="xpath", value='//div[@class="image"]')

products = []
prices = []
images = []
links = []


for i in containers:
    product= i.find_element(by="xpath", value='./h4/a').text
    price = i.find_element(by="xpath", value='./p[@class="price same"]').text
    price = price.replace('ریال','')	
    products.append(product)
    prices.append(price)

for i in containers_images:
    link = i.find_element(by="xpath", value='./a').get_attribute("href")
    image = i.find_element(by="xpath", value='./a/img').get_attribute("src")
    links.append(link)
    images.append(image)


my_dict={'Product': products , 'Price': prices, 'Link': links, 'Image': images }

df = pd.DataFrame(my_dict)

df['Price'] = df['Price'].apply(lambda x: int(x.replace(',','')) /10 )

df.to_csv('Nilper_Sandali_Edari_headless.csv')

driver.quit()