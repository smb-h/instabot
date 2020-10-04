# InstaBot

InstaBot is a Python library for crawling Instagram using selenium


## About

1. There is 2 type of crawl that we can handle here.
   
    - crawl a user by username,
    - crawl by a tag
    

## Usage


1. Params
    
    | Params        | Info          |
    | ------------- | ------------- |
    | `-V` or `--version`  | Get version  |
    |`--help`  | help  |
    | `-P` or `--posts`  | Get posts detail  |
    | `-L` or `--likes`  | Get likes info  |
    | `-C` or `--comments`  | Get comments detail  |
    | `-S` or `--stories`  | Get stories  |
    | `-T` or `--tag`  | Get posts by tag  |
    | `-U` or `--username`  | Target username  |
    | `--max-likes`  | Number of maximum likes to crawl  |
    | `--max-comments`  | Number of maximum comments to crawl  |
    | `--max-posts`  | Number of maximum posts to crawl  |
    | `--tor-proxy`  | Use Tor proxy (follow the steps to config on ur machine)  |


> ***Note*** `-U` or `--username` parameter is required if u want to crawl a user.

> ***Note*** `--max-posts` parameter is required if u want to crawl by tag.

> ***Note*** that target user must be public or if it's private it must followed by ur authenticated user.

- To crawl based on a tag, set the tag parameter `--tag nature`

- To crawl based on a username, set the username parameter `--username emmawatson`

2. In static directory create `secret.txt` and set authentication credintials
    ```
    username = myusername
    password = mypassword
    ```

3. Data will store in `data` directory (`target_username.json` or `tag_name.json`)

4. Log will store in the current directory as `instagram.log`

5. Sample commands:
    ```
   $ python src.py --username emmawatson --posts --max-posts 20 --likes --max-likes 100 --comments --max-comments 100 --stories --tor-proxy
   $ python src.py --tag nature --posts --max-posts 40 --likes --max-likes 100 --comments --max-comments 100 --tor-proxy
   
    ```

### Use Tor proxy
Install Tor.

```shell
sudo apt-get update
sudo apt-get install tor
sudo /etc/init.d/tor restart
```

*Notice that the socks listener is on port 9050.*

Next, do the following:

- Enable the ControlPort listener for Tor to listen on port 9051, as this is the port to which Tor will listen for any communication from applications talking to the Tor controller.
- Hash a new password that prevents random access to the port by outside agents.
- Implement cookie authentication as well.

You can create a hashed password out of your password using:
	
```shell
tor --hash-password my_password
```
Now update ur password in `proxy.py`
```
c.authenticate(password = "my_password")
```

Then, update the /etc/tor/torrc with the port, hashed password, and cookie authentication.

```shell
sudo nano /etc/tor/torrc
```

```shell
ControlPort 9051
# hashed password below is obtained via `tor --hash-password my_password`
HashedControlPassword 16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF
CookieAuthentication 1
```
Restart Tor again to the configuration changes are applied.
	
```shell
sudo /etc/init.d/tor restart
```

Next, install `python-stem` which is a Python-based module used to interact with the Tor Controller, letting us send and receive commands to and from the Tor Control port programmatically.

```shell
sudo apt-get install python-stem
```

Tor itself is not a http proxy. So in order to get access to the Tor Network, use `privoxy` as an http-proxy though socks5.

Install `privoxy` via the following command:
	
```shell
sudo apt-get install privoxy
```
Now when u pass `--tor-proxy` to command it will use `proxy.py` and it will generate `proxy.log` that u can see what is happening in the process.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)




