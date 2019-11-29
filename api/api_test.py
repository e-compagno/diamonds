import requests
import json
url = 'http://127.0.0.1:5000/'
x0 = {
            'carat': [0.23],\
            'cut': ['Ideal'],\
            'color': ['E'],\
            'clarity': ['SI2'],\
            'depth': [61.5],\
            'table': [55.0],\
            'price': [326],\
            'x': [3.95],\
            'y': [3.98],\
            'z': [2.43]
        }

x = {'carat': '0.23', 'cut': 'Ideal','color': 'E', 'clarity': 'SI2','depth': '61.5','table': '55.0','price': '326','x': '3.95','y': '3.98','z': '2.43'}
data=json.dumps(x)
send_request=requests.post(url, data)
print(send_request.json())