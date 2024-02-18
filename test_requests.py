import requests

url="https://exercises-00.nw.r.appspot.com/api/v1"

body = {
    'time': '0a-10'
}

reservations = [
    {'date': '2024-02-13', 'time': '08-10'},
    {'date': '2024-02-14', 'time': '10-12'},
    {'date': '2024-03-13', 'time': '18-20'}
    #{'date': '2024-02-25', 'time': '14-16'},
    #{'date': '2024-02-26', 'time': '16-1a'},
    #{'date': '2024-02-19', 'time': '10-12'},
    #{'date': '2024-02-21', 'time': '10-12'},
    #{'date': '2024-03-22', 'time': '0a-10'},
    #{'date': '2024-03-23', 'time': '10-12'},
    #{'date': '2024-03-24', 'time': '12-14'},
    #{'date': '2024-02-14', 'time': '0a-10'},
    #{'date': '2024-04-22', 'time': '10-12'}
]

#print("POST WITH BODY TO api/v1/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/2024-02-13'")
#resp = requests.post(url+'/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', json=reservations)
#print(resp)
print("GET TO api/v1/2024-02-22")
resp = requests.get(url+'/2024-02-22')
print(resp.text)

#print("GET TO api/v1/dump")
#resp = requests.get(url+"/dump")
#print(resp.text)