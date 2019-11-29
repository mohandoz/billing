import requests

body = """
ضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضض
ضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضضض
21

3ق21






"""

phone = "962785627788"
url = f"http://josmsservice.com/smsonline/msgservicejo.cfm?numbers={phone},&senderid=Quekeeper&AccName=rihinnov&AccPass=rihinnov123&msg={body}&requesttimeout=5000000"
x = requests.post(url)
print("Sms Sent")

#print(x)
#print(x.__dict__)
print(body)
