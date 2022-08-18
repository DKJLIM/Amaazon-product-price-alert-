#####################################################
############### Relevant Modules ####################
######################################################
import bs4
import smtplib
import requests
import personal_credentials
import product_details

########################################################
############### Web scraping element ####################
########################################################

productURL = product_details.productURL
headers_information= personal_credentials.headersInformation

response = requests.get(url=productURL, headers=headers_information).text

soup = bs4.BeautifulSoup(response, "lxml")
was_price=[]
current_price=[]
result = soup.find('span',class_='a-offscreen')
price_int = float(result.getText()[1::])

########################################################
############### Alerting element #######################
########################################################

# From Email credentials
emailFrom = personal_credentials.emailFrom
passwordFrom = personal_credentials.password
emailTo = personal_credentials.emailTo

# From product details
product_name = product_details.productName
price_floor= product_details.minimumPrice

message = f'subject:{product_name} is currently GBP{price_int} \n\n ' \
          f'Hey there, the price of {product_name} is currently GBP{price_int}. \n' \
          f'you can find it here: {productURL}'

if price_int<price_floor:
    with smtplib.SMTP("smtp.office365.com") as connection:
        connection.starttls()
        connection.login(user=emailFrom, password=passwordFrom)
        connection.sendmail(from_addr=emailFrom, to_addrs=emailTo,
                            msg=message)