from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from . import __version__
from .settings import Settings

#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://google.com/ncr")
    driver.find_element(By.NAME, "q").send_keys("cheese" + Keys.RETURN)
    first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3>div")))
    print(first_result.get_attribute("textContent"))
  


class InstaBot:
    """Class to be instantiated to use the script"""

    def __init__(self, username = None, password = None, delay = 5):
        print("InstaBot Version: {}".format(__version__))

        self.browser = None
        self.delay = delay

        # choose environment over static typed credentials
        self.username = username
        self.password = password

        self.split_db = split_db
        if self.split_db:
            Settings.database_location = localize_path(
                "db", "instapy_{}.db".format(self.username)
            )

        self.want_check_browser = want_check_browser

        self.do_comment = False
        self.comment_percentage = 0
        self.comments = ["Cool!", "Nice!", "Looks good!"]
        self.photo_comments = []
        self.video_comments = []

        self.do_reply_to_comments = False
        self.reply_to_comments_percent = 0
        self.comment_replies = []
        self.photo_comment_replies = []
        self.video_comment_replies = []

        self.liked_img = 0
        self.already_liked = 0
        self.liked_comments = 0
        self.commented = 0
        self.replied_to_comments = 0
        self.followed = 0
        self.already_followed = 0
        self.unfollowed = 0
        self.followed_by = 0
        self.following_num = 0
        self.inap_img = 0
        self.not_valid_users = 0
        self.video_played = 0
        self.already_Visited = 0
        self.stories_watched = 0
        self.reels_watched = 0

        self.follow_times = 1
        self.share_times = 1
        self.comment_times = 1
        self.do_follow = False
        self.follow_percentage = 0
        self.dont_include = set()
        self.white_list = set()
        self.blacklist = {"enabled": "True", "campaign": ""}
        self.automatedFollowedPool = {"all": [], "eligible": []}
        self.do_like = False
        self.like_percentage = 0
        self.do_story = False
        self.story_percentage = 0
        self.story_simulate = False
        self.smart_hashtags = []
        self.smart_location_hashtags = []

        self.dont_like = ["sex", "nsfw"]
        self.mandatory_words = []
        self.ignore_if_contains = []
        self.ignore_users = []

        self.user_interact_amount = 0
        self.user_interact_media = None
        self.user_interact_percentage = 0
        self.user_interact_random = False
        self.dont_follow_inap_post = True

        self.use_clarifai = False
        self.clarifai_api_key = None
        self.clarifai_models = []
        self.clarifai_workflow = []
        self.clarifai_probability = 0.50
        self.clarifai_img_tags = []
        self.clarifai_img_tags_skip = []
        self.clarifai_full_match = False
        self.clarifai_check_video = False
        self.clarifai_proxy = None

        self.potency_ratio = None  # 1.3466
        self.delimit_by_numbers = None

        self.max_followers = None  # 90000
        self.max_following = None  # 66834
        self.min_followers = None  # 35
        self.min_following = None  # 27

        self.delimit_liking = False
        self.liking_approved = True
        self.max_likes = 1000
        self.min_likes = 0

        self.delimit_commenting = False
        self.commenting_approved = True
        self.max_comments = 35
        self.min_comments = 0
        self.comments_mandatory_words = []
        self.max_posts = None
        self.min_posts = None
        self.skip_business_categories = []
        self.skip_bio_keyword = []
        self.mandatory_bio_keywords = []
        self.dont_skip_business_categories = []
        self.skip_business = False
        self.skip_non_business = False
        self.skip_no_profile_pic = False
        self.skip_private = True
        self.skip_business_percentage = 100
        self.skip_no_profile_pic_percentage = 100
        self.skip_private_percentage = 100
        self.relationship_data = {username: {"all_following": [], "all_followers": []}}

        self.simulation = {"enabled": True, "percentage": 100}

        self.mandatory_language = False
        self.mandatory_character = []
        self.check_letters = {}

        # use this variable to terminate the nested loops after quotient
        # reaches
        self.quotient_breach = False
        # hold the consecutive jumps and set max of it used with QS to break
        # loops
        self.jumps = {
            "consequent": {"likes": 0, "comments": 0, "follows": 0, "unfollows": 0},
            "limit": {"likes": 7, "comments": 3, "follows": 5, "unfollows": 4},
        }

        self.allowed_pod_topics = [
            "general",
            "fashion",
            "food",
            "travel",
            "sports",
            "entertainment",
        ]
        self.allowed_pod_engagement_modes = ["no_comments", "light", "normal", "heavy"]

        # stores the features' name which are being used by other features
        self.internal_usage = {}

        self.aborting = False
        self.start_time = time.time()

        # proxy address
        self.proxy_address = proxy_address

        # assign logger
        self.show_logs = show_logs
        Settings.show_logs = show_logs or None
        self.multi_logs = multi_logs
        self.logfolder = get_logfolder(self.username, self.multi_logs)
        self.logger = self.get_instapy_logger(self.show_logs, log_handler)

        get_database(make=True)  # IMPORTANT: think twice before relocating

        if selenium_local_session:
            self.browser, err_msg = set_selenium_local_session(
                proxy_address,
                proxy_port,
                proxy_username,
                proxy_password,
                headless_browser,
                browser_profile_path,
                disable_image_load,
                page_delay,
                geckodriver_path,
                browser_executable_path,
                self.logger,
            )
            if len(err_msg) > 0:
                raise InstaPyError(err_msg)


