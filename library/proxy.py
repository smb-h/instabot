import requests
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
import random, time
import urllib
import json
import logging.config
import sys

# signal TOR for a new connection 
# https://stackoverflow.com/questions/30286293/make-requests-using-python-over-tor
# https://jarroba.com/anonymous-scraping-by-tor-network/
# https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853


# Connection manager
class ConnectionManager:

    # initial
    def __init__(self):
        # logger
        self.logger = ConnectionManager.get_logger(level = logging.DEBUG, dest = "", verbose = 0)
        self.logger.info("initial connection manager...")
        self.headers = { 'User-Agent': UserAgent().random }
        self.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        # self.current_ip = self.get_request(url = "https://ident.me").text
        self.current_ip = self.get_request(url = "http://api.ipify.org").text
        self.get_connection_info(self.current_ip)

    # get request
    def get_request(self, url):
        rs = requests.get(url, proxies = self.proxies, headers = self.headers)
        time.sleep(4)
        return rs

    # get connection info
    def get_connection_info(self, ip):
        response = urllib.request.urlopen(f"http://ipinfo.io/{ip}/json")
        data = json.load(response)
        city = data['city']
        country = data['country']
        region = data['region']
        provider = data['org']
        self.logger.info(f"IP Address: {ip} \t City: {city} \t Region: {region} \t Country: {country} \t Provider: {provider}")

    # Renew connection
    def renew_connection(self):
        while True:
            with Controller.from_port(port = 9051) as c:
                # c.authenticate(password="password")
                c.authenticate(password = "SomeThingDunnoxD")
                c.signal(Signal.NEWNYM)

            wait = random.uniform(0, 5)
            self.logger.warning(f"Wait : {str(wait)}")
            time.sleep(wait)

            new_ip = self.get_request(url = 'https://api.ipify.org').text
            self.get_connection_info(new_ip)
            # check ip change 
            if self.current_ip != new_ip:
                break

    # logger
    @staticmethod
    def get_logger(level = logging.DEBUG, dest='', verbose = 0):
        """Returns a logger."""
        logger = logging.getLogger(__name__)

        dest +=  '/' if (dest !=  '') and dest[-1] != '/' else ''
        fh = logging.FileHandler(f'{dest}proxy.log', 'w')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        fh.setLevel(level)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        # warning, info, error
        sh_lvls = [logging.ERROR, logging.WARNING, logging.INFO]
        sh.setLevel(sh_lvls[verbose])
        logger.addHandler(sh)

        logger.setLevel(level)

        return logger




    




