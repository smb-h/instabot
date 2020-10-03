from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import requests
import json
import logging.config
import sys
import os
from .proxy import ConnectionManager


# InstaBot
class InstaBot:
    # initial
    def __init__(self, target_username = None, posts_flag = True, likes_flag = False, comments_flag = False, stories_flag = False, target_tag = None, max_likes = None, max_comments = None, max_posts = None):
        # logger
        self.logger = InstaBot.get_logger(level = logging.DEBUG, dest = "", verbose = 0)

        # initiate browser
        opts = Options()
        opts.headless = True
        assert opts.headless
        self.logger.info("initial browser...")
        # proxy config
        # cm = ConnectionManager()
        # cm.renew_connection()
        # profile = webdriver.FirefoxProfile()
        # profile.set_preference("network.proxy.type", 1)
        # profile.set_preference("network.proxy.socks", '127.0.0.1')
        # profile.set_preference("network.proxy.socks_port", 9050)
        # profile.set_preference("network.proxy.socks_remote_dns", False)
        # profile.update_preferences()

        # proxy
        # self.driver = webdriver.Firefox(firefox_profile = profile)
        # headless
        self.driver = webdriver.Firefox(options = opts)
        # normal
        # self.driver = webdriver.Firefox()
        # full options
        # self.driver = webdriver.Firefox(firefox_profile = profile, options = opts)
        self.navigate_webdriver("https://www.instagram.com")

        # read username, password from file
        with open("static/secret.txt", "r") as file:
            file = file.readlines()
            self.username = file[0].strip().split("=")[1].strip()
            self.password = file[1].strip().split("=")[1].strip()

        self.posts_flag = posts_flag
        self.max_posts = int(max_posts) if max_posts else None
        self.target_username = target_username
        self.likes_flag = likes_flag
        self.max_likes = int(max_likes) if max_likes else None
        self.comments_flag = comments_flag
        self.max_comments = int(max_comments) if max_comments else None
        self.target_tag = target_tag
        self.stories_flag = stories_flag

    # navigate webdriver
    def navigate_webdriver(self, path):
        driver = self.driver
        self.logger.info("navigate to " + path)
        driver.get(path)
        self.inject_jquery()
        time.sleep(6)

    # refresh webdriver
    def refresh_webdriver(self):
        driver = self.driver
        self.logger.info("refresh page")
        driver.refresh()
        self.inject_jquery()
        time.sleep(10)
    
    # authenticate
    def authenticate(self, username = None, password = None):
        driver = self.driver
        username = self.username
        password = self.password
        # login
        username_field = driver.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys(username)

        password_field = driver.find_element_by_name("password")
        password_field.clear()
        password_field.send_keys(password)

        password_field.send_keys(Keys.RETURN)

        self.logger.info("login as " + self.username)

        time.sleep(5)

        # save info alert
        try:
            driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/div/div/button").click()
            time.sleep(2)
        except NoSuchElementException:
            # print("There is no (Save info!) alert")
            self.logger.warning("there is no save info alert!")

        # notification popup
        try:
            driver.find_element_by_tag_name("body").find_element_by_xpath("//div[4]/div/div/div/div[3]/button[2]").click()
            time.sleep(2) 
        except NoSuchElementException:
            # print("There is no (Allow notification) alert")
            self.logger.warning("there is no allow notification alert!")

    # inject jquery to driver
    def inject_jquery(self):
        driver = self.driver
        # jquery = requests.get("https://code.jquery.com/jquery-3.5.1.min.js").text
        with open('static/jquery-3.5.1.min.js', 'r') as jquery_js: 
            jquery = jquery_js.read()
            driver.execute_script(jquery)
            # driver.execute_script("$('body')")
        self.logger.info("inject jquery")

    # get user public info
    def get_user_public_info(self):
        self.logger.info("get public info")
        driver = self.driver
        self.navigate_webdriver("https://www.instagram.com" + "/" + self.target_username)

        # logged user info
        # driver.find_element_by_tag_name("main").find_element_by_xpath("//section/div[3]/div/div/div/a").click()
        
        # user info
        retry_prompt = 0
        while retry_prompt < 5:
            try:
                user_bio = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/div[2]").text
                posts_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/ul/li[1]/span/span").text.replace(",", "").replace(".", ""))
                followers_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/ul/li[2]/a/span").get_attribute("title").replace(",", "").replace(".", ""))
                break
            except:
                self.refresh_webdriver()
                retry_prompt += 1

        try:
            following_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/ul/li[3]/a/span").get_attribute("title").replace(",", "").replace(".", ""))
        except:
            following_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/ul/li[3]/a/span").text.replace(",", "").replace(".", ""))

        time.sleep(5)

        self.user_bio = user_bio
        self.posts_count = posts_count
        self.followers_count = followers_count
        self.following_count = following_count

        return({
            "user_bio": user_bio,
            "posts_count": posts_count,
            "followers_count": followers_count,
            "following_count": following_count
        })

    # get user followers
    def get_user_followers(self):
        self.logger.info("gather user followers")
        followers_count = self.followers_count
        # list of followers
        if followers_count:
            user_followers = []
            driver.find_element_by_tag_name("main").find_element_by_xpath("//header/section/ul/li[2]/a").click()
            time.sleep(1)
            followers_section = driver.find_element_by_tag_name("body").find_elements_by_xpath("//div[4]/div/div/div[2]/ul/div/li")
            # load all followings
            while len(followers_section) < followers_count:
                driver.execute_script("$('.isgrP').animate({ scrollTop: $('.isgrP').prop('scrollHeight')}, 100);")
                followers_section = driver.find_element_by_tag_name("body").find_elements_by_xpath("//div[4]/div/div/div[2]/ul/div/li")
                time.sleep(2)
            for e in followers_section:
                user_followers.append({
                    "username": e.text.split()[0],
                    "subtitle": e.text.split()[1],
                })
            return(user_followers)

    # get user followings
    def get_user_followings(self):
        self.logger.info("gather user followings")
        following_count = self.following_count
        # list of following
        if following_count:
            user_followings = []
            driver.find_element_by_tag_name("main").find_element_by_xpath("//header/section/ul/li[3]/a").click()
            time.sleep(1)
            following_section = driver.find_element_by_tag_name("body").find_elements_by_xpath("//div[4]/div/div/div[2]/ul/div/li")
            # load all followings
            while len(following_section) < following_count:
                driver.execute_script("$('.isgrP').animate({ scrollTop: $('.isgrP').prop('scrollHeight')}, 100);")
                following_section = driver.find_element_by_tag_name("body").find_elements_by_xpath("//div[4]/div/div/div[2]/ul/div/li")
                time.sleep(2)
        for e in following_section:
            user_followings.append({
                "username": e.text.split()[0],
                "subtitle": e.text.split()[1],
            })

    # get posts
    def get_posts(self):
        driver = self.driver
        self.logger.info("gather user posts")
        self.navigate_webdriver("https://www.instagram.com" + "/" + self.target_username)

        # get post urls
        posts_data = {}
        # scroll to posts
        driver.execute_script("""
            var y = $(window).scrollTop(); 
            $(window).scrollTop(y+350);
        """)

        try:
            # load all posts
            max_posts_section_height = 0
            retry_scroll = 0
            while True:
                # extract
                posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG")
                for post in posts:
                    post_url = post.find_element_by_tag_name("a").get_attribute("href") 
                    post_media = post.find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src")
                    post_views_count = 0
                    post_comments_count = 0
                    post_likes_count = 0

                    # break when it reaches maximum depth
                    if self.max_posts:
                        if len(posts_data) >= self.max_posts:
                            break

                    # hover element
                    if post_url not in posts_data.keys():
                        try:
                            hover = ActionChains(driver).move_to_element(post)
                            hover.perform()
                            time.sleep(1)
                        except MoveTargetOutOfBoundsException:
                            driver.execute_script("""
                                var y = $(window).scrollTop(); 
                                $(window).scrollTop(y+350);
                            """)
                            hover = ActionChains(driver).move_to_element(post)
                            hover.perform()
                            time.sleep(1)

                    # check either in div 2 or 3
                    # skip mini icon on top of post
                    try:
                        tmp = post.find_element_by_tag_name("a").find_element_by_xpath("//div[2]/ul/li/span")
                        is_iconed = False
                        skip_icon = "2"
                    except NoSuchElementException:
                        is_iconed = True
                        skip_icon = "3"
                    # gather like comment view data from hover
                    first_item = post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span")
                    try:
                        second_item = post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span")
                    except NoSuchElementException:
                        second_item = None
                    # first item
                    if "coreSpriteHeartSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span[2]").get_attribute("class"):
                        post_likes_count = first_item.text.replace(",", "")
                        if "m" in post_likes_count:
                            post_likes_count = post_likes_count.replace("m", "")
                            post_likes_count = int(float(post_likes_count) * 1000000)
                        elif "k" in post_likes_count:
                            post_likes_count = post_likes_count.replace("k", "")
                            post_likes_count = int(float(post_likes_count) * 1000)
                    elif "coreSpriteSpeechBubbleSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span[2]").get_attribute("class"):
                        post_comments_count = first_item.text.replace(",", "")
                        if "m" in post_comments_count:
                            post_comments_count = post_comments_count.replace("m", "")
                            post_comments_count = int(float(post_comments_count) * 1000000)
                        elif "k" in post_comments_count:
                            post_comments_count = post_comments_count.replace("k", "")
                            post_comments_count = int(float(post_comments_count) * 1000)
                    elif "coreSpritePlayIconSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span[2]").get_attribute("class"):
                        post_views_count = first_item.text.replace(",", "")
                        if "m" in post_views_count:
                            post_views_count = post_views_count.replace("m", "")
                            post_views_count = int(float(post_views_count) * 1000000)
                        elif "k" in post_views_count:
                            post_views_count = post_views_count.replace("k", "")
                            post_views_count = int(float(post_views_count) * 1000)

                    # second item
                    if second_item:
                        if "coreSpriteHeartSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span[2]").get_attribute("class"):
                            post_likes_count = second_item.text.replace(",", "")
                            post_likes_count = first_item.text.replace(",", "")
                            if "m" in post_likes_count:
                                post_likes_count = post_likes_count.replace("m", "")
                                post_likes_count = int(float(post_likes_count) * 1000000)
                            elif "k" in post_likes_count:
                                post_likes_count = post_likes_count.replace("k", "")
                                post_likes_count = int(float(post_likes_count) * 1000)
                        elif "coreSpriteSpeechBubbleSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span[2]").get_attribute("class"):
                            post_comments_count = second_item.text.replace(",", "")
                            if "m" in post_comments_count:
                                post_comments_count = post_comments_count.replace("m", "")
                                post_comments_count = int(float(post_comments_count) * 1000000)
                            elif "k" in post_comments_count:
                                post_comments_count = post_comments_count.replace("k", "")
                                post_comments_count = int(float(post_comments_count) * 1000)
                        elif "coreSpritePlayIconSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span[2]").get_attribute("class"):
                            post_views_count = second_item.text.replace(",", "")
                            if "m" in post_views_count:
                                post_views_count = post_views_count.replace("m", "")
                                post_views_count = int(float(post_views_count) * 1000000)
                            elif "k" in post_views_count:
                                post_views_count = post_views_count.replace("k", "")
                                post_views_count = int(float(post_views_count) * 1000)

                    if post_url not in posts_data.keys():
                        posts_data[post_url] = {
                            "url": post_url,
                            "media": post_media,
                            "likes_count": post_likes_count,
                            "comments_count": post_comments_count,
                            "views_count": post_views_count,
                        }

                    self.logger.info("load {0}/{1} posts".format(len(posts_data), self.max_posts))

                # break when it reaches maximum depth
                if self.max_posts:
                    if (len(posts_data) >= self.max_posts):
                        break

                # scroll
                # driver.execute_script("$('html, body').animate({ scrollTop: $('html, body').prop('scrollHeight')}, 350);")
                # time.sleep(5)

                posts_section_style = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div[3]/article/div/div").get_attribute("style")
                new_posts_section_height = int((posts_section_style.split(" ")[-1]).replace("px", ""). replace(";", ""))

                if new_posts_section_height > max_posts_section_height:
                    max_posts_section_height = new_posts_section_height
                    retry_scroll = 0
                elif retry_scroll >= 3:
                    break
                else:
                    retry_scroll += 1
        except NoSuchElementException:
            pass

        return posts_data

    # get likes detail
    def get_likes_detail(self):
        pass

    # get comments detail
    def get_comments_detail(self):
        pass

    # get post detail
    def get_post_detail(self, url):
        driver = self.driver
        self.navigate_webdriver(url)

        # post media
        post_media_type = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[2]/div")
        is_video = False
        is_multiple = False
        is_picture = False
        # detect multiple
        try:
            is_multiple = post_media_type.find_element_by_tag_name("li")
            is_multiple = True
        except NoSuchElementException:
            pass

        # detect media types
        try:
            is_picture = post_media_type.find_element_by_tag_name("img")
            is_picture = True
        except NoSuchElementException:
            pass
        try:
            is_video = post_media_type.find_element_by_tag_name("video")
            is_video = True
            is_picture = False
        except NoSuchElementException:
            pass

        post_media = []
        # if multiple 
        if is_multiple:
            while True:
                try:
                    if is_video:
                        available_vids = post_media_type.find_elements_by_tag_name("video")
                        for vid in available_vids:
                            vid_url = vid.get_attribute('poster').replace("amp;", "")
                            if vid_url not in post_media:
                                post_media.append(vid_url)
                    elif is_picture:
                        available_pics = post_media_type.find_elements_by_tag_name("img")
                        for pic in available_pics:
                            pic_url = pic.get_attribute('src').replace("amp;", "")
                            if pic_url not in post_media:
                                post_media.append(pic_url)
                except:
                    pass
                # click on next media
                try:
                    driver.find_element_by_class_name("coreSpriteRightChevron").click()
                    time.sleep(2)
                except NoSuchElementException:
                    # print("There is no other media!")
                    break  
        else:
            if is_video:
                tmp = post_media_type.find_element_by_tag_name("video").get_attribute('poster').replace("amp;", "")
                post_media.append(tmp)
            elif is_picture:
                tmp = post_media_type.find_element_by_tag_name("img").get_attribute('src').replace("amp;", "")
                post_media.append(tmp)

        # post content
        try:
            post_content = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/div/ul/div/li/div/div/div/span").text
        except NoSuchElementException:
            post_content = ""


        # comments
        # load all comments
        if self.comments_flag or self.max_comments:
            while True:
                try:
                    loaded_comments = driver.find_element_by_tag_name("main").find_elements_by_xpath("//div/div/article/div[3]/div/ul/ul")
                    if len(loaded_comments) >= self.max_comments:
                        break
                    driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/div/ul/li/div/button").click()
                    time.sleep(2)
                except NoSuchElementException:
                    break
        comments = {}
        try:
            loaded_comments = driver.find_element_by_tag_name("main").find_elements_by_xpath("//div/div/article/div[3]/div/ul/ul")
            for cm_section in loaded_comments:
                cm_by_user = cm_section.text.split("\n")[0]
                cm_content = cm_section.text.split("\n")[1]
                comments[cm_by_user] = cm_content
        except NoSuchElementException:
            pass
        # likes and views
        views = 0
        likes_count = 0
        likes = []

        try:
            driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/section[2]/div/span")
        except NoSuchElementException:
            is_video = False
            is_picture = True

        if is_video:
            views_button = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/section[2]/div/span")
            views = views_button.text.replace(",", "").replace(" views", "")
            views = int(views) if views else 0
            views_button.click()
            likes_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/section[2]/div/div/div[4]/span").text.replace(",", ""))
        elif is_picture:
            likes = []
            if self.likes_flag or self.max_likes:
                try:
                    driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/section[2]/div/div/button").click()
                    time.sleep(3)
                    # load all likes
                    likes_section_height = 356
                    max_likes_section_height = 356
                    while True:
                        # extract
                        like_div_sections = driver.find_element_by_tag_name("body").find_elements_by_xpath("//div[4]/div/div/div[2]/div/div/div")
                        for div in like_div_sections:
                            tmp = div.text.split("\n")[0]
                            if tmp not in likes:
                                likes.append(tmp)
                            # break on max depth
                            if self.max_likes:
                                if len(likes) >= self.max_likes:
                                    break
                        # break on max depth
                        if self.max_likes:
                            if len(likes) >= self.max_likes:
                                break
                        # scroll
                        driver.execute_script("$('.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd div').animate({ scrollTop: $('.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd div').prop('scrollHeight')}, 100);")
                        time.sleep(3)

                        likes_section_style = driver.find_element_by_tag_name("body").find_element_by_xpath("//div[4]/div/div/div[2]/div/div").get_attribute("style")
                        new_likes_section_height = int((likes_section_style.split(" ")[-1]).replace("px", ""). replace(";", "")) + 356
                        if new_likes_section_height > max_likes_section_height:
                            max_likes_section_height = new_likes_section_height
                            # gather new data
                        else:
                            break
                except NoSuchElementException:
                    pass
        
        return({
            "url": url,
            "media": post_media,
            "content": post_content,
            "likes_count": len(likes) if likes else likes_count,
            "likes": likes,
            "views_count": views,
            "comments_count": len(comments),
            "comments": comments
        })

    # get highlight stories
    def get_stories_highlights(self):
        self.logger.info("get highlight stories")
        driver = self.driver
        self.navigate_webdriver("https://www.instagram.com" + "/" + self.target_username)

        stories = []
        # get list of highlight items
        try:
            highlight_section = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/div/div/div/ul")
            highlights = highlight_section.find_elements_by_css_selector("li.Ckrof")
            highlights[0].click()
            time.sleep(1)
            while True:
                try:
                    src = driver.find_element_by_tag_name("body").find_element_by_xpath("//div/section/div/div/section/div[2]/div/div/div/img").get_attribute("src")
                    if src not in stories:
                        stories.append(src)
                    time.sleep(2)
                except NoSuchElementException:
                    break
        except NoSuchElementException:
            return stories
        return stories

    # get stories
    def get_stories(self):
        self.logger.info("get stories")
        driver = self.driver
        self.navigate_webdriver("https://www.instagram.com" + "/" + self.target_username)

        # click on profile photo
        driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/div/div").click()
        time.sleep(3)
        media = []
        while True:
            try:
                driver.find_element_by_tag_name("body").find_element_by_xpath("//div/section/div/div/section/div[2]/div/div/div")
            except NoSuchElementException:
                break

            src = driver.find_element_by_tag_name("body").find_element_by_xpath("//div/section/div/div/section/div[2]/div/div/div/img").get_attribute("src")
            if src not in media:
                media.append(src)
            time.sleep(4)
        return media

    # get posts by tag
    def get_posts_by_tag(self):
        self.logger.info(f"get posts by tag #{self.target_tag}")
        driver = self.driver
        self.navigate_webdriver("https://www.instagram.com/explore/tags/" + self.target_tag)

        # get post urls
        posts_data = {}
        # scroll to posts
        driver.execute_script("""
            var y = $(window).scrollTop(); 
            $(window).scrollTop(y+350);
        """)

        try:
            # load all posts
            max_posts_section_height = 0
            retry_scroll = 0
            while True:
                # extract
                posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG")
                for post in posts:
                    post_url = post.find_element_by_tag_name("a").get_attribute("href") 
                    post_media = post.find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src")
                    post_views_count = 0
                    post_comments_count = 0
                    post_likes_count = 0

                    # break when it reaches maximum depth
                    if self.max_posts:
                        if len(posts_data) >= self.max_posts:
                            break

                    # hover element
                    if post_url not in posts_data.keys():
                        try:
                            hover = ActionChains(driver).move_to_element(post)
                            hover.perform()
                            time.sleep(1)
                        except MoveTargetOutOfBoundsException:
                            driver.execute_script("""
                                var y = $(window).scrollTop(); 
                                $(window).scrollTop(y+350);
                            """)
                            hover = ActionChains(driver).move_to_element(post)
                            hover.perform()
                            time.sleep(1)

                    # check either in div 2 or 3
                    # skip mini icon on top of post
                    try:
                        tmp = post.find_element_by_tag_name("a").find_element_by_xpath("//div[2]/ul/li/span")
                        is_iconed = False
                        skip_icon = "2"
                    except NoSuchElementException:
                        is_iconed = True
                        skip_icon = "3"
                    # gather like comment view data from hover
                    first_item = post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span")
                    try:
                        second_item = post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span")
                    except NoSuchElementException:
                        second_item = None
                    # first item
                    if "coreSpriteHeartSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span[2]").get_attribute("class"):
                        post_likes_count = first_item.text.replace(",", "")
                        if "m" in post_likes_count:
                            post_likes_count = post_likes_count.replace("m", "")
                            post_likes_count = int(float(post_likes_count) * 1000000)
                        elif "k" in post_likes_count:
                            post_likes_count = post_likes_count.replace("k", "")
                            post_likes_count = int(float(post_likes_count) * 1000)
                    elif "coreSpriteSpeechBubbleSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span[2]").get_attribute("class"):
                        post_comments_count = first_item.text.replace(",", "")
                        if "m" in post_comments_count:
                            post_comments_count = post_comments_count.replace("m", "")
                            post_comments_count = int(float(post_comments_count) * 1000000)
                        elif "k" in post_comments_count:
                            post_comments_count = post_comments_count.replace("k", "")
                            post_comments_count = int(float(post_comments_count) * 1000)
                    elif "coreSpritePlayIconSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li/span[2]").get_attribute("class"):
                        post_views_count = first_item.text.replace(",", "")
                        if "m" in post_views_count:
                            post_views_count = post_views_count.replace("m", "")
                            post_views_count = int(float(post_views_count) * 1000000)
                        elif "k" in post_views_count:
                            post_views_count = post_views_count.replace("k", "")
                            post_views_count = int(float(post_views_count) * 1000)

                    # second item
                    if second_item:
                        if "coreSpriteHeartSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span[2]").get_attribute("class"):
                            post_likes_count = second_item.text.replace(",", "")
                            post_likes_count = first_item.text.replace(",", "")
                            if "m" in post_likes_count:
                                post_likes_count = post_likes_count.replace("m", "")
                                post_likes_count = int(float(post_likes_count) * 1000000)
                            elif "k" in post_likes_count:
                                post_likes_count = post_likes_count.replace("k", "")
                                post_likes_count = int(float(post_likes_count) * 1000)
                        elif "coreSpriteSpeechBubbleSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span[2]").get_attribute("class"):
                            post_comments_count = second_item.text.replace(",", "")
                            if "m" in post_comments_count:
                                post_comments_count = post_comments_count.replace("m", "")
                                post_comments_count = int(float(post_comments_count) * 1000000)
                            elif "k" in post_comments_count:
                                post_comments_count = post_comments_count.replace("k", "")
                                post_comments_count = int(float(post_comments_count) * 1000)
                        elif "coreSpritePlayIconSmall" in post.find_element_by_tag_name("a").find_element_by_xpath(f"//div[{skip_icon}]/ul/li[2]/span[2]").get_attribute("class"):
                            post_views_count = second_item.text.replace(",", "")
                            if "m" in post_views_count:
                                post_views_count = post_views_count.replace("m", "")
                                post_views_count = int(float(post_views_count) * 1000000)
                            elif "k" in post_views_count:
                                post_views_count = post_views_count.replace("k", "")
                                post_views_count = int(float(post_views_count) * 1000)

                    if post_url not in posts_data.keys():
                        posts_data[post_url] = {
                            "url": post_url,
                            "media": post_media,
                            "likes_count": post_likes_count,
                            "comments_count": post_comments_count,
                            "views_count": post_views_count,
                        }

                    self.logger.info("load {0}/{1} posts".format(len(posts_data), self.max_posts))

                # break when it reaches maximum depth
                if self.max_posts:
                    if (len(posts_data) >= self.max_posts):
                        break

                # scroll
                # driver.execute_script("$('html, body').animate({ scrollTop: $('html, body').prop('scrollHeight')}, 350);")
                # time.sleep(5)

                posts_section_style = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div[3]/article/div/div").get_attribute("style")
                new_posts_section_height = int((posts_section_style.split(" ")[-1]).replace("px", ""). replace(";", ""))

                if new_posts_section_height > max_posts_section_height:
                    max_posts_section_height = new_posts_section_height
                    retry_scroll = 0
                elif retry_scroll >= 3:
                    break
                else:
                    retry_scroll += 1
        except NoSuchElementException:
            pass


        return posts_data

    # get posts by tag
    # def get_posts_by_tag(self):
    #     self.logger.info(f"get posts by tag #{self.target_tag}")
    #     driver = self.driver
    #     self.navigate_webdriver("https://www.instagram.com/explore/tags/" + self.target_tag)

    #     # get post urls
    #     post_urls = []

    #     try:
    #         # load all posts
    #         max_posts_section_height = 0
    #         retry_scroll = 0
    #         while True:
    #             # extract
    #             posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG")
    #             for post in posts:
    #                 post_url = post.find_element_by_tag_name("a").get_attribute("href") 

    #                 # break when it reaches maximum depth
    #                 if self.max_posts:
    #                     if len(post_urls) >= self.max_posts:
    #                         break

    #                 if post_url not in post_urls:
    #                     post_urls.append(post_url)

    #             # scroll
    #             driver.execute_script("$('html, body').animate({ scrollTop: $('html, body').prop('scrollHeight')}, 350);")
    #             time.sleep(5)

    #             self.logger.info("load {0}/{1} posts".format(len(post_urls), self.max_posts))

    #             posts_section_style = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div[3]/article/div/div").get_attribute("style")
    #             new_posts_section_height = int((posts_section_style.split(" ")[-1]).replace("px", ""). replace(";", ""))
    #             if new_posts_section_height > max_posts_section_height:
    #                 max_posts_section_height = new_posts_section_height
    #                 retry_scroll = 0
    #             elif retry_scroll >= 3:
    #                 break
    #             else:
    #                 retry_scroll += 1
    #     except NoSuchElementException:
    #         pass

    #     all_posts = []
    #     # get post detail
    #     for url in post_urls:
    #         self.logger.info("gather post data {0}/{1}".format((post_urls.index(url) + 1), len(post_urls)))
    #         post_data = self.get_post_detail(url)
    #         all_posts.append(post_data)

    #     return all_posts

    # scroll page
    def scroll(self):
        driver = self.driver
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

    # close web driver
    def close_driver(self):
        self.logger.info("closing driver!")
        self.driver.close()

    # store data
    def store_data(self, user_public_info = None, posts_data = None, stories = None, stories_highlights = None, posts_by_tag_data = None):
        self.logger.info("store data...")
        json_data = {
            "user_public_info": user_public_info,
            "stories": stories,
            "stories_highlights": stories_highlights,
            "posts": posts_data,
        }
        if not os.path.exists('data'):
            os.makedirs('data')
        if self.target_tag:
            with open('data/{}.json'.format(self.target_tag), 'w', encoding='utf8') as outfile:
                json.dump(json_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        else :
            with open('data/{}.json'.format(self.target_username), 'w', encoding='utf8') as outfile:
                json.dump(json_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

    # logger
    @staticmethod
    def get_logger(level = logging.DEBUG, dest='', verbose = 0):
        """Returns a logger."""
        logger = logging.getLogger(__name__)

        dest +=  '/' if (dest !=  '') and dest[-1] != '/' else ''
        fh = logging.FileHandler(dest + 'instagram.log', 'w')
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

    # crawl
    def crawl(self):
        # time elapsed
        start = time.time()
        # authenticate
        if self.username and self.password:
            self.authenticate()

        # get target username public info
        public_info = None
        if self.target_username:
            public_info = self.get_user_public_info()

        # get posts data
        posts_data = None
        if (self.posts_flag or self.max_posts) and self.target_username:
            posts_data = self.get_posts()
        
        # get stories data
        stories_data = None
        stories_highlights = None
        if self.stories_flag:
            stories_data = self.get_stories()
            stories_highlights = self.get_stories_highlights()
        
        # get posts by tag
        if self.target_tag and self.max_posts:
            posts_data = self.get_posts_by_tag()

        # get posts detail
        if (self.posts_flag or self.likes_flag or self.comments_flag or self.max_likes or self.max_posts) and (posts_data):
            post_urls = list(posts_data.keys())
            for url in post_urls:
                self.logger.info("gather post data {0}/{1} - {2}".format((post_urls.index(url) + 1), len(post_urls), url))
                post_data = self.get_post_detail(url)
                post_item = posts_data.get(url)
                post_item["media"] = post_data.get("media")
                post_item["content"] = post_data.get("content")
                if post_item["likes_count"] == 0:
                    post_item["likes_count"] = post_data.get("likes_count")
                post_item["likes"] = post_data.get("likes")
                # post_item["views_count"] = post_data.get("views_count")
                if post_item["comments_count"] == 0:
                    post_item["comments_count"] = post_data.get("comments_count")
                post_item["comments"] = post_data.get("comments")

        # store data
        self.store_data(user_public_info = public_info, stories = stories_data, stories_highlights = stories_highlights, posts_data = posts_data)

        # close driver
        self.close_driver()

        # logger
        # time elapsed
        self.logger.info('time elapsed : ' + str(time.time() - start))





