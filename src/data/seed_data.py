from dotenv import load_dotenv
import os
import requests

from pathlib import Path
from urllib.parse import unquote

import pandas as pd

from .g_sheets_db import GS_Client

project_root = Path(__file__).resolve().parents[1]
env_path = project_root / '.env'

client_id = os.getenv('WP_CLIENT_ID')
client_secret = os.getenv('WP_CLIENT_SECRET')
redirect_url = os.getenv('WP_REDIRECT_URL')
auth_code = os.getenv('WP_AUTH_CODE')
# auth_code = unquote(os.getenv("WP_AUTH_CODE"))
blog_id = os.getenv('WP_BLOG_ID')
access_token = os.getenv('WP_ACCESS_TOKEN')

def get_access_token():
    url = "https://public-api.wordpress.com/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_url,
        "grant_type": "authorization_code",
        "code": auth_code
    }
    
    res = requests.post(url, data=data)
    print(f"Status Code: {res.status_code}")

    try:
        # Parse JSON response
        response = res.json()
        print(f"Response JSON: {response}")

        if res.status_code == 200:
            print("✅ Access Token:", response.get("access_token"))
            print("🔄 Refresh Token:", response.get("refresh_token"))
            print("🔎 Scope:", response.get("scope"))

        else:
            print("Error:", response.get("error_description"))

    except Exception as e:
        # If JSON parsing fails, output raw response text
        print(f"Raw Response: {res.content.decode('utf-8')}")
        print(f"Error: {e}")

def fetch_posts():
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{blog_id}/posts/"
    headers = {"Authorization": f"Bearer {access_token}"}

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        posts = res.json().get('posts', [])
        print(f"✅ Fetched {len(posts)} posts")
        for post in posts[:5]:
            print(f"Title {post.get('title')}: URL {post.get('URL')}")
    else:
        print("Error fetching posts:", res.json())

def backlog_post_data():
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{blog_id}/posts/"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        posts = res.json()
        tracking_list = []
        # analytics_list = []
        # metadata_list = []
        content_list = []
        data_dict = {
            'tracking': None,
            'analytics': None,
            'metadata': None,
            'content': None
        }
        for idx, post in enumerate(posts['posts']):
                # print(post.keys())
                post = {k.lower(): v for k, v in post.items()}
                tracking_list.append([
                    post['id'],
                    post['site_id'],
                    post['date'],
                    # post['timestamp'],
                    post['title'],
                    post['url'],
                    post['global_id']
                    ])
                # analytics_list.append([
                #     post['ID'],
                #     post['author'],
                #     post['date'],
                #     post['title'],
                #     post['like_count'],
                #     post['is_reblogged'],
                #     post['tags'],
                #     post['categories']
                # ])
                #auto increment metadata table
                # metadata_list.append([
                #     post['ID'],
                #     post['URL'],
                #     # post['short_URL']
                #     # post['modified']
                #     post['slug'],
                #     post['guid'],
                #     post['status'],
                #     post['parent'],
                #     post['discussion'],
                #     post['likes_enabled'],
                #     post['sharing_enabled'],
                #     post['is_following'],
                #     # post['post_thumbnail'],
                #     post['format'],
                #     post['attachment_count']
                #     # post['attachment'],
                #     # post['metadata'],
                #     # post['meta']
                # ])
                content_list.append([
                    post['id'],
                    post['content'],
                    post['excerpt']
                ])
        data_dict['tracking'] = pd.DataFrame(tracking_list)
        # data_dict['analytics'] = analytics_list
        # data_dict['metadata'] = metadata_list
        data_dict['content'] = pd.DataFrame(content_list)
    return data_dict


if __name__ == '__main__':
    # get_access_token()
    # fetch_posts()
    # data_dict = fetch_all_post_data()
    # print(data_dict.keys())
    # data_dict = backlog_post_data()
    # gs_obj_tracking_data = GS_Client()
    # gs_obj_tracking_data.insert_data(spreadsheet_id=gs_obj_tracking_data.codeots_gdrive_dict['codeots_tracking_sheet_id'], 
    #                                 values=data_dict['tracking'].values.tolist(),
    #                                 start_range='A', end_range='F', 
    #                                 sheet_name='blog_tracking')
    v=5