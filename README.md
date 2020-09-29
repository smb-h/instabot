# InstaBot

InstaBot is a Python library for crawling Instagram using selenium


## About

1. There is 2 type of crawl that we can handle here.
   
    - crawl a user by username,
    - crawl by a tag
    

## Usage


1. To crawl a username (posts, stories, comments, likes, ...) in `src.py` when we are creating instance of the bot set the target username 
    
    
    bot = InstaBot(target_username = "some_username")
    

> ***Note*** that target user must be public or if it's private it must followed by ur authenticated user.

- To crawl based on a tag, set the tag parameter in `src.py`

- So u can either crawl by a tag or a username

2. In static directory create `secret.txt` and set authentication credintials
    ```
    username = myusername
    password = mypassword
    ```

3. Data will store in `data` directory (`target_username.json` or `tag_name.json`)

4. Log will store in the current directory as `instagram.log`

5. Use `src.py` as sample to create ur own script based on ur needs.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)




