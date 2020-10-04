import time
from library.instabot import InstaBot
import sys
import argparse


# Main
def main():

    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-P", "--posts", help="get posts", action="store_true")
    parser.add_argument("-L", "--likes", help="get likes", action="store_true")
    parser.add_argument("-C", "--comments", help="get comments", action="store_true")
    parser.add_argument("-S", "--stories", help="get stories", action="store_true")
    parser.add_argument("-T", "--tag", help="get posts by tag")
    parser.add_argument("-U", "--username", help="target username")
    parser.add_argument("--max-likes", help="maximum number of likes")
    parser.add_argument("--max-comments", help="maximum number of comments")
    parser.add_argument("--max-posts", help="maximum number of posts")
    parser.add_argument("--tor-proxy", help="use tor proxy", action="store_true")
    args = parser.parse_args()

    
    bot = InstaBot(target_username = args.username, posts_flag = args.posts, likes_flag = args.likes, comments_flag = args.comments, stories_flag = args.stories, target_tag = args.tag, max_likes = args.max_likes, max_comments = args.max_comments, max_posts = args.max_posts, tor_proxy = args.tor_proxy)
    bot.crawl()



if __name__ == "__main__":
    main()



