import time
from library.instabot import InstaBot

# Main
def main():
    # time elapsed
    start = time.time()

    # stinerisnes, manon.lantie_, ma_jid2670, clip_shad_1, me93525, baran_nikrah, t.e.x.t.gram
    bot = InstaBot(target_username = "manon.lantie_")
    bot.authenticate()
    # public_info = bot.get_user_public_info()
    # posts_data = bot.get_posts()
    # stories = bot.get_stories()
    # stories_highlights = bot.get_stories_highlights()
    # bot.store_data(user_public_info = public_info, stories = stories, stories_highlights = stories_highlights, posts_data = posts_data)

    # tag
    tag = "ایران"
    posts_by_tag_data = bot.get_posts_by_tag(tag, maximum = 2)
    bot.store_data(posts_by_tag_data = posts_by_tag_data, tag = tag)

    # close driver
    bot.close_driver()

    # logger
    # time elapsed
    bot.logger.info('time elapsed : ' + str(time.time() - start))



if __name__ == "__main__":
    main()



