import random
import requests
import time
import re
import json
import sys

G_PROXIES = []

SESSION_IDS = []
USER_AGENT = ['Instagram 9.5.1 (iPhone9,2; iOS 10_0_2; en_US; en-US; scale=2.61; 1080x1920) AppleWebKit/420+',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 123.1.0.26.115 (iPhone11,8; iOS 13_3; en_US; en-US; scale=2.00; 828x1792; 190542906)',
              'Mozilla/5.0 (Linux; Android 8.1.0; motorola one Build/OPKS28.63-18-3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 Instagram 72.0.0.21.98 Android (27/8.1.0; 320dpi; 720x1362; motorola; motorola one; deen_sprout; qcom; pt_BR; 132081645)'
              ]
TAG = "fitness"
MIN_FOLLOWERS = 10


if (len(sys.argv) > 1):
    TAG = sys.argv[1]

URL_API_END = "?__a=1"
URL_BASE = "https://www.instagram.com/"
URL_TAG = URL_BASE + "explore/tags/" + TAG
URL_PIC = URL_BASE + "p/"
REGEX_EMAIL = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
HAS_NEXT_PAGE = True
END = ""
CURRENT = 0

def get_random_agent():
    all_user_agents = USER_AGENT
    u_agent = all_user_agents[random.randint(0, len(all_user_agents) - 1)]
    return u_agent


def get_random_session():
    all_session_ids = SESSION_IDS
    session_id = all_session_ids[random.randint(0, len(all_session_ids) - 1)]
    return session_id


def get_random_proxy():
    proxies = G_PROXIES
    r_proxy = proxies[random.randint(0, len(proxies) - 1)]
    proxy = {'http': r_proxy, 'https': r_proxy}
    return proxy


def get_tag_posts(end):
    try:
        proxy = get_random_proxy()
        r_tag_posts = requests.get(
            URL_TAG + URL_API_END + '&max_id=' + str(end))
    except:
        print("error proxy")
        print(proxy)
        return 0
    if "html" in r_tag_posts.headers['Content-Type']:
        return 0
    all_posts = r_tag_posts.json()[
        'graphql']['hashtag']['edge_hashtag_to_media']['edges']
    end_cursor = r_tag_posts.json()[
        'graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    has_next_page = r_tag_posts.json()[
        'graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
    return {'all_posts': all_posts, 'end_cursor': end_cursor, 'has_next_page': has_next_page}

def get_user_infos(id):
    proxy = get_random_proxy()
    try:
        user_infos = requests.get("https://i.instagram.com/api/v1/users/" + str(id) + "/info/", cookies={
            'sessionid': get_random_session()}, headers={'User-Agent': get_random_agent()})
    except:
        print("error proxy")
        print(proxy)
        return 0
    if "json" in user_infos.headers['Content-Type'] == False:
        return 0
    return json.loads(user_infos.content.decode('utf-8'))['user']
    
while True:
   try:
      f = open(str(TAG) + ".csv", "a+")
      print(TAG)
      while HAS_NEXT_PAGE:
         time.sleep(random.randint(6, 12))
         posts = get_tag_posts(END)
         if posts == 0:
            continue
         HAS_NEXT_PAGE = posts['has_next_page']
         END = posts['end_cursor']
         for i in range(0, len(posts['all_posts']) - 1):
            CURRENT += 1
            username_id = posts['all_posts'][i]['node']['owner']['id']
            time.sleep(random.randint(6, 13))
            username_infos = get_user_infos(username_id)
            if username_infos == 0 or username_id == 0:
                  continue
            if username_infos['follower_count'] > MIN_FOLLOWERS:
                  email_bio = re.findall(
                     REGEX_EMAIL, username_infos['biography'])
                  if "public_email" in username_infos and len(username_infos['public_email']) > 1:
                     print(username_infos['public_email'])
                     f.write(username_infos['username'] + ";%d;" %
                              username_infos['follower_count'] + username_infos['public_email'] + '\n')
                  if email_bio:
                     print(email_bio)
                     f.write(username_infos['username'] + ";%d;" %
                              username_infos['follower_count'] + ';'.join(email_bio) + '\n')
      f.close()
   except Exception as e:
      print(e)
