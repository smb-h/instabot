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
    | `-V` Or `--version`  | Get version  |
    |`--help`  | help  |
    | `-P` Or `--posts`  | Get posts detail  |
    | `-L` Or `--likes`  | Get likes info  |
    | `-C` Or `--comments`  | Get comments detail  |
    | `-S` Or `--stories`  | Get stories  |
    | `-T` Or `--tag`  | Get posts by tag  |
    | `-U` Or `--username`  | Target username  |
    | `--max-likes`  | Number of maximum likes to crawl  |
    | `--max-comments`  | Number of maximum comments to crawl  |
    | `--max-posts`  | Number of maximum posts to crawl  |


> ***Note*** `-U` Or `--username` parameter is required if u want to crawl a user.

> ***Note*** `--max-posts` parameter is required if u want to crawl by tag.

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

5. Sample commands:
    ```
   $ python src.py --username emmawatson --posts --max-posts 20 --likes --max-likes 100 --comments --max-comments 100 --stories
   $ python src.py --tag nature --posts --max-posts 40 --likes --max-likes 100 --comments --max-comments 100
   
    ```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)




