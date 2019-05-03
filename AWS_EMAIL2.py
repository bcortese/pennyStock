import boto3
from botocore.exceptions import ClientError
import requests
import datetime

class AWS_EMAIL2:
    
    def __init__(self, stock="nothing", originalValue=0.0):
        self.stock = stock
        self.amount = originalValue
                
    def setStockInfo(self, stockName, orginalAmount):
       self.stock = stockName
       self.amount = orginalAmount
       
    #contact api to retrieve current price, this will only run successfully between monday - friday 9:30 am - 4pm. 
    def getCurrentPrice(self):
       API_KEY = 'WCJ7NEVWD0NMZGWE'
       r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+self.stock+'&interval=5min&outputsize=full&apikey=' + API_KEY)
       result = r.json()
       dataForAllDays = result['Time Series (5min)']
       now = datetime.datetime.now()
           
       self.currentStock = self.amount* float(dataForAllDays['2019-04-09 16:00:00'].get("1. open", "none"))
       return self.currentStock
   
   #rule of thumb, if the stock is 20% greater than my initial buying price, it should be a time to flip.
    def getFlipPrice(self):
       self.twentyPercentStock = self.amount+(self.amount*.20)
       return self.twentyPercentStock

    def stockReturn(self):
        # This address must be verified with Amazon SES.
        SENDER = "Sender Name <emailenteredhere@gmail.com>"
        
        RECIPIENT = "emailenteredhere@gmail.com"        
        
        AWS_REGION = "us-west-2"
        
        # The subject line for the email.
        Subject = self.stock
        
        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Penny Stocks Notification\r\n"
                     "%s is at 20%% or greater intitial buy: %s "
                     "AWS SDK for Python (Boto)."
                    )
        BODY_TEXT = BODY_TEXT % (self.stock, self.twentyPercentStock)            
        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Stock in Reviewal %s</h1>
          <p>%s is at 20%% or greater intitial buy: %s</p>
        </body>
        </html>
                    """     
        BODY_HTML = BODY_HTML % (self.stock, self.stock, self.twentyPercentStock)
        
        # The character encoding for the email.
        CHARSET = "UTF-8"
        
        # Create a new SES resource and specify a region.
        client = boto3.client('ses',region_name=AWS_REGION)

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': Subject,
                    },
                },
                Source=SENDER,

            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID: %s" % self.stock)

        
