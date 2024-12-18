import requests, json
from environs import Env
import logging


env = Env()
env.read_env()  # Charger le fichier .env

API_KEY = env.str("API_KEY")
DOMAIN = env.str("DOMAIN")

rrset_name = "@"
rrset_type = "A"
url = f"https://api.gandi.net/v5/livedns/domains/{DOMAIN}/records/{rrset_name}/{rrset_type}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_gandip():
    """Get the current IP adress register in gandi DNS

    Raises:
        Exception: if fail raise an exeption

    Returns:
        _type_: the ip adress currently register in the gandi DNS
    """
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        gandip = response.json()["rrset_values"][0]
        print(f"GandIP est : {gandip}")

        return gandip
    
    else:
        raise Exception("Can't reach Gandi API")

def get_extip():
    """Get the dynamic ip of the device

    Raises:
        Exception: if the site ipify can't be reach raise exeption

    Returns:
        _type_: the wan public ip of the device
    """
    ip_wan = requests.get('https://api.ipify.org')

    if ip_wan.status_code == 200:
        ip_wan = ip_wan.content.decode('utf8')
        print(f'WanIP est  : {ip_wan}')

        return ip_wan
    
    else:
        raise Exception("Can't reach ipify")
    

if __name__ == '__main__':
    gandip = get_gandip()
    extip = get_extip()


    logging.basicConfig(filename="./out.log",
                    filemode='a',
                    format='%(asctime)s, %(name)s %(message)s',
                    datefmt='%Y-%m-%d : %H:%M',
                    level=logging.INFO)

    if gandip == extip:
        print("All good, no need to change")
    else:
        data = {
            "rrset_values": [f"{extip}"],
        }

        response = requests.put(url, data=json.dumps(data), headers=headers)
        if response.status_code == 201 :
            print("All good, l'ip est update")
            logging.info(f"changement ip : {gandip} --> {extip}")
        else:
            print("Erreur au moment de l'update")

        print(response.json())
