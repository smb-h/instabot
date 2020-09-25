from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import requests
import json


# InstaBot
class InstaBot:
    # initial
    def __init__(self, target_username):
        # initiate browser
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.instagram.com")
        time.sleep(5)

        self.username = "smb__h"
        self.password = "3!M>Z*(VhZkB"
        self.target_username = target_username

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

        time.sleep(5)

        # save info alert
        try:
            driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/div/div/button").click()
            time.sleep(2)
        except NoSuchElementException:
            print("There is no (Save info!) alert")

        # notification popup
        try:
            driver.find_element_by_tag_name("body").find_element_by_xpath("//div[4]/div/div/div/div[3]/button[2]").click()
            time.sleep(2) 
        except NoSuchElementException:
            print("There is no (Allow notification) alert")

    # inject jquery to driver
    def inject_jquery(self):
        driver = self.driver
        # jquery = requests.get("https://code.jquery.com/jquery-3.5.1.min.js").text
        with open('jquery-3.5.1.min.js', 'r') as jquery_js: 
            jquery = jquery_js.read()
            driver.execute_script(jquery)
            # driver.execute_script("$('body')")

    # get user public info
    def get_user_public_info(self):
        driver = self.driver
        driver.get("https://www.instagram.com" + "/" + self.target_username)
        time.sleep(2)
        # logged user info
        # driver.find_element_by_tag_name("main").find_element_by_xpath("//section/div[3]/div/div/div/a").click()
        
        # user info
        user_bio = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/div[2]").text
        posts_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/ul/li[1]/span/span").text.replace(",", "").replace(".", ""))
        followers_count = int(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/header/section/ul/li[2]/a/span").get_attribute("title").replace(",", "").replace(".", ""))
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
        
        # get post urls
        post_urls = []
        while len(post_urls) < self.posts_count:
            posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG a")
            for post in posts:
                post_url = post.get_attribute("href")
                if post_url not in post_urls:
                    post_urls.append(post_url)

            driver.execute_script("""$("html, body").animate({ scrollTop: $(document).height()-$(window).height() });""")
            time.sleep(5)

            if len(post_urls) == self.posts_count:
                break

        all_posts = []
        # get post detail
        for url in post_urls:
            post_data = self.get_post_detail(url)
            all_posts.append(post_data)


        return all_posts

    # get post detail
    def get_post_detail(self, url):
        driver = self.driver
        driver.get(url)
        time.sleep(5)
           
        # if not post_media:
        #     post_media = [(driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[2]/div/div/div").get_attribute('innerHTML').split("src")[-1])[2:-2].replace("amp;", "")]
        # print(post_media)


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
        # if multiple use functions
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
        post_content = driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/div/ul/div/li/div/div/div/span").text

        # load all comments
        while True:
            try:
                driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/div/ul/li/div/button").click()
                time.sleep(2)
            except NoSuchElementException:
                break
        comments = {}
        loaded_comments = driver.find_element_by_tag_name("main").find_elements_by_xpath("//div/div/article/div[3]/div/ul/ul")
        for cm_section in loaded_comments:
            cm_by_user = cm_section.text.split("\n")[0]
            cm_content = cm_section.text.split("\n")[1]
            comments[cm_by_user] = cm_content

        # likes
        likes = []
        driver.find_element_by_tag_name("main").find_element_by_xpath("//div/div/article/div[3]/section[2]/div/div/button").click()
        time.sleep(3)
        # load all likes
        likes_section_height = 356
        max_likes_section_height = 356
        self.inject_jquery()
        while True:
            # extract
            like_div_sections = driver.find_element_by_tag_name("body").find_elements_by_xpath("//div[4]/div/div/div[2]/div/div/div")
            for div in like_div_sections:
                tmp = div.text.split("\n")[0]
                if tmp not in likes:
                    likes.append(tmp)
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

        return({
            "url": url,
            "post_media": post_media,
            "post_content": post_content,
            "likes": likes,
            "comments": comments
        })

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
        self.driver.close()

    def store_data(self, user_public_info = None, posts_data = None):
        print(user_public_info)
        print(posts_data)
        json_data = {
            "user_public_info": user_public_info,
            "posts": posts_data,
        }
        with open('data/{}.json'.format(self.target_username), 'w', encoding='utf8') as outfile:
            json.dump(json_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

# search_field = driver.find_element_by_tag_name("body").find_element_by_xpath("//div/section/nav/div[2]/div/div/div[2]/input")
# search_field.clear()
# search_field.send_keys(search_param)
# time.sleep(5)
# driver.find_element_by_tag_name("body").find_element_by_xpath("//div/section/nav/div[2]/div/div/div[2]/input")
# time.sleep(3)


# Main
def main():
    # stinerisnes, manon.lantie_, ma_jid2670, clip_shad_1
    bot = InstaBot(target_username = "anali_0018")
    bot.authenticate()
    bot.inject_jquery()
    public_info = bot.get_user_public_info()
    bot.inject_jquery()
    posts_data = bot.get_posts()
    bot.store_data(public_info, posts_data)


    bot.close_driver()



if __name__ == "__main__":
    main()



