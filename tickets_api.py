import requests

key = '1g89Fx2KHiAD3WdLaBFtpKdTxZEW2lvS'

response = requests.get('https://app.ticketmaster.com/discovery/v2/events?.json?{key}' , 
                        params= {
                                 'keyword':'concert'})
