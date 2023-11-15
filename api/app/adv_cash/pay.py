import requests
import os
from dotenv import load_dotenv
import hashlib



load_dotenv()




tinkoff_url = os.getenv('TINKOFF')
terminal_key = os.getenv('T_TERMINAL')
password = os.getenv('T_PASSWORD')




def create_payment_session(amount, order_id, description):
    method_url = 'Init'
    url = tinkoff_url + method_url
    data = {
        "TerminalKey": terminal_key,
        "Amount": amount,
        "OrderId": order_id,
        "Description": description,
        "Password": password
    }
    headers = {"Content-Type": "application/json"}
    sorted_data = dict(sorted(data.items()))
    conc_values = "".join(map(str, sorted_data.values()))
    hash_obj = hashlib.sha256(conc_values.encode())
    hashed_value = hash_obj.hexdigest()
    data['Token'] = hashed_value
    
    response = requests.post(url=url, headers=headers, json=data)
    response_data = response.json()
    return response_data
    
    
    
