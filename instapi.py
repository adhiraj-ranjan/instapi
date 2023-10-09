import requests
from datetime import datetime
import random
import json
import sys
import os
import time
import pickle
from urllib3 import disable_warnings
import base64

disable_warnings()
error_codes = {201: "Created",
               204: "No Content",
               205: "Reset Content",
               206: "Partial Content",
               300: "Multiple Choices",
               301: "Moved Permanently",
               304: "Not Modified",
               307: "Temporary Redirect",
               400: "Bad Request",
               401: "Unauthorized",
               402: "Payment Required",
               403: "Forbidden",
               404: "Not Found",
               408: "Request Timed Out",
               410: "Gone",
               415: "Unsupported Media Type",
               429: "Too Many Requests",
               500: "Internal Server Error",
               503: "Service Unavailable",
               560: "Invalid public/private key"}

# get random user-agent


def randUserAgent():

    windows_versions = [
        'Windows NT 5.1',   # Windows XP
        'Windows NT 6.0',   # Windows Vista
        'Windows NT 6.1',   # Windows 7
        'Windows NT 6.2',   # Windows 8
        'Windows NT 6.3',   # Windows 8.1
        'Windows NT 10.0'   # Windows 10
    ]

    web_browsers = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',  # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',                              # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/83.0.478.37 Safari/537.36',   # Microsoft Edge
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',   # Chrome on 64-bit Windows
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'                                            # Internet Explorer
    ]

    windows_version = random.choice(windows_versions)
    user_agent = random.choice(web_browsers)

    return user_agent.replace('Windows NT 10.0', windows_version)


def printFunc(response, Text):
    if response.ok:
        print(f"> {Text} - true")
        return True
    else:
        print(f"> {Text} - false")
        print(response,  error_codes[response.status_code])
        print(response.text)
        return False


class instagramapi:
    def __init__(self, username=None, password=None, blockPrint=False):
        self.userName = username
        self.userPass = password
        self.userAgent = randUserAgent()
        self.loggedIn = False
        self.userID = None
        self.s = requests.Session()
        if blockPrint:
            sys.stdout = open(os.devnull, "w")

    def login(self, show_response=False):
        response = requests.get(
            'https://www.instagram.com/api/v1/web/login_page/', headers=self.__get_headers(check_logged_in=False, x_csrftoken='#'))
        if not response.ok:
            print("[ info ] Unable to connect to Instagram --ip ban")
            return False

        dateTime = int(datetime.now().timestamp())

        payload = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{self.userPass}',
            'username': self.userName,
            'queryParams': '{"next":"https://www.instagram.com/"}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
        }
        insta_loggedIn_response = self.s.post(
            "https://www.instagram.com/api/v1/web/accounts/login/ajax/", data=payload, headers=self.__get_headers(x_csrftoken=response.cookies.get_dict()["csrftoken"], check_logged_in=False)).json()
        
        try:
            if insta_loggedIn_response['status'] == 'ok':
                if 'user' in insta_loggedIn_response.keys():
                    if insta_loggedIn_response['user']:
                        pass
                    else:
                        print("[ % ] Login Failed <--Wrong Username-->")
                if insta_loggedIn_response['authenticated']:
                    if "userId" in insta_loggedIn_response:
                        self.userID = insta_loggedIn_response["userId"]

                    print("[ info ] logged in as " + self.userName)

                    self.loggedIn = True
                else:
                    print("[ % ] Login Failed <--Wrong Password-->")
            else:
                print("[ % ] Login Failed <--Unknown-->")
        except:
            print("[ % ] Login Failed <--Unknown-->")

            
        if show_response:
            print(insta_loggedIn_response)
        return insta_loggedIn_response

    def __get_headers(self,
                      host=None,
                      accept=None,
                      accept_language=None,
                      accept_encoding=None,
                      referer=None,
                      x_csrftoken=None,
                      x_requested_with=None,
                      connection=None,
                      user_agent=None,
                      addHeader=None,
                      content_type=None,
                      remove_header=[],
                      check_logged_in=True):


        if check_logged_in:
            if not self.loggedIn:
                print("[ info ] You are not logged in [ try login ]")
                print("[ info ] Exiting...")
                exit(0)

        if not host:
            host = "www.instagram.com"
        if not accept:
            accept = "*/*"
        if not accept_language:
            accept_language = "en-US,en;q=0.9"
        if not accept_encoding:
            accept_encoding = "gzip, deflate"
        if not referer:
            referer = f"https://www.instagram.com/{self.userName}/"
        if not x_csrftoken:
            x_csrftoken = self.s.cookies['csrftoken']
        if not x_requested_with:
            x_requested_with = "XMLHttpRequest"
        if not user_agent:
            user_agent = self.userAgent
        if not content_type:
            content_type ="application/x-www-form-urlencoded"

        headersformed = {
            'authority': host,
            'accept': accept,
            'accept-language': accept_language,
            'content-type': content_type,
            'origin': 'https://www.instagram.com',
            'referer': referer,
            'user-agent': user_agent,
            'x-asbd-id': '198387',
            'x-csrftoken': x_csrftoken,
            'x-ig-app-id': "936619743392459",
            'x-ig-www-claim': 'hmac.AR1a2eZl6dFg59QPQonxoSxRdrXuCEdIfeNNbiG6Tt_POL-J',
            'x-instagram-ajax': '1007399682',
            'x-requested-with': x_requested_with,
        }

        if connection:
            headersformed.update({"Connection": connection})

        if addHeader:
            headersformed.update(addHeader)

        if remove_header:
            for header in remove_header:
                del headersformed[header.lower()]

        return headersformed

    def set_proxy(self, proxy, username=None, password=None):
        # with authentication - proxy='127.0.0.1:80', username="username", password="password"
        # without authentiation - proxy='127.0.0.1:80'
        if username and password:
            proxies = {'http': f'http://{username}:{password}@{proxy}/',
                       'https': f'http://{username}:{password}@{proxy}/'}
        else:
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        print(proxies)
        self.s.proxies.update(proxies)
        print("proxy set!")

    def save_session(self, f_path=None):
        if not f_path:
            f_path = self.userName + ".cookie"
        data = [self.s.cookies.get_dict(), {
                                            'username': self.userName,
                                            'password': self.userPass,
                                            'userAgent': self.userAgent,
                                            'userid': self.userID
                                        }]
        configs = json.dumps(data)
        with open(f_path, 'wb') as f:
            f.write(str.encode(
                str(int.from_bytes(configs.encode('utf-8'), 'little'))))
        print(f'--> Cookies saved in file <{f_path}>')

    def load_session(self, filename):
        with open(filename, 'rb') as f:
            content = f.read()

        d_content = int(content.decode('utf-8'))
        configs = json.loads(d_content.to_bytes((d_content.bit_length() + 7) // 8, 'little').decode('utf-8'))
        
        # load cookie
        for cookie in configs[0].keys():
            self.s.cookies.set(cookie, configs[0][cookie], domain='.instagram.com')

        self.userAgent = configs[1]['userAgent']
        self.userID = configs[1]['userid']
        self.userName = configs[1]['username']
        self.userPass = configs[1]['password']
        profile = self.s.get(f"https://www.instagram.com/{self.userName}/", headers=self.__get_headers(check_logged_in=False))

        if profile.ok:
            try:
                self.userID = self.get_profile_data(self.userName, False)['data']['user']['id']
            except:
                print('--> [ account may have a checkpoint ]')
                return False
            print(f'--> Cookies loaded [ {self.userName} ]')
            self.loggedIn = True
            return True
        else:
            print('--> Cookies expired [ try to login ]')
            return False
        
    def load_cookie_json(self, cookies_file, userName, userPass, userAgent):
        with open(cookies_file) as f:
            cookies = json.load(f)

        # Set the cookies in the session
        for cookie in cookies:
            self.s.cookies.set(cookie['name'], cookie['value'], domain='.instagram.com')

        self.userName = userName
        self.userID = self.s.cookies.get_dict()['ds_user_id']
        self.userAgent = userAgent
        self.userPass = userPass
        
        profile = self.s.get(f"https://www.instagram.com/{self.userName}/", headers=self.__get_headers(check_logged_in=False))

        if profile.ok:
            try:
                self.userID = self.get_profile_data(self.userName, False)['data']['user']['id']
            except:
                print('--> [ account may have a checkpoint ]')
                return False
            print(f'--> Cookies loaded [ {self.userName} ]')
            self.loggedIn = True
            return True
        else:
            print('--> Cookies expired [ try to login ]')
            return False


    def get_profile_data(self, username, check_logged_in=True):
        params = {
            'username': username,
        }
        userJson = self.s.get('https://www.instagram.com/api/v1/users/web_profile_info/',
                              params=params, headers=self.__get_headers(check_logged_in=check_logged_in))
        if userJson.ok:
            return userJson.json()
        else:
            return printFunc(userJson, 'got profile data')
    
    def get_userid(self, username):
        profile_json = self.get_profile_data(username)
        if profile_json:
            return profile_json['data']['user']['id']
        else:
            return False
        
    def follow(self, userid):
        data = {
            'container_module': 'profile',
            'nav_chain': 'PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfileRoot:profilePage:2:unexpected',
            'user_id': f'{userid}',
        }
        response = self.s.post(f'https://www.instagram.com/api/v1/friendships/create/{userid}/', data=data, headers=self.__get_headers())
        return printFunc(response, f"user followed - {userid}")
    
    def unfollow(self, userid):
        data = {
            "container_module": "profile",
            "nav_chain": "PolarisProfileRoot:profilePage:2:topnav-link,PolarisProfileRoot:profilePage:3:unexpected",
            "user_id": f'{userid}',
        }
        response = self.s.post(f'https://www.instagram.com/api/v1/friendships/destroy/{userid}/', data=data, headers=self.__get_headers())
        return printFunc(response, f"user unfollowed - {userid}")
    
    def change_profile_picture(self, imagePath):
        if not os.path.isfile(imagePath):
            raise FileNotFoundError("Image file doesn't exist")
        
        headers = self.__get_headers(content_type='multipart/form-data; boundary=----WebKitFormBoundaryb2l4cYKBfPEUfavW', addHeader={"Content-Length": str(os.path.getsize(imagePath))})

        files = {'profile_pic': open(imagePath, 'rb')}
        values = {"Content-Disposition": "form-data", "name": "profile_pic", "filename":"profilepic.jpg", "Content-Type": "image/jpeg"}

        response = self.s.post('https://www.instagram.com/api/v1/web/accounts/web_change_profile_picture/', headers=headers, files=files, data=values)
        return printFunc(response, "profile picture changed")

    def remove_profile_picture(self):
        response = self.s.post('https://www.instagram.com/api/v1/web/accounts/web_change_profile_picture/', headers=self.__get_headers())
        return printFunc(response, "profile picture removed")
    
    def block(self, userid):
        response = self.s.post(f"https://www.instagram.com/api/v1/web/friendships/{userid}/block/", headers=self.__get_headers())
        return printFunc(response, "user blocked")

    def unblock(self, userid):
        response = self.s.post(f"https://www.instagram.com/api/v1/web/friendships/{userid}/unblock/", headers=self.__get_headers())
        return printFunc(response, "user unblocked")
    
    def set_account_private(self):
        data = {
            'is_private': 'true',
        }
        response = self.s.post('https://www.instagram.com/api/v1/web/accounts/set_private/', headers=self.__get_headers(), data=data)
        return printFunc(response, "is private")
    
    def set_account_public(self):
        data = {
            'is_private': 'false',
        }
        response = self.s.post('https://www.instagram.com/api/v1/web/accounts/set_private/', headers=self.__get_headers(), data=data)
        return printFunc(response, "is public")

    def get_user_following(self, userid, count=None, fetch_all=True):
        users = []
        params = {
            'count': '12',
        }
        url = f'https://www.instagram.com/api/v1/friendships/{userid}/following/'

        while True:
            response = self.s.get(url, params=params, headers=self.__get_headers())
            for user in response.json()['users']:
                users.append(user)

            if "next_max_id" in response.json():
                params["max_id"] = response.json()['next_max_id']
            else:
                break

            if count:
                if len(users) >= count:
                    users = users[:count]
                    break
            else:
                continue
        
        return users
    
    def get_self_following(self, count=None, fetch_all=True):
        return self.get_user_following(self.userID, count, fetch_all)

    def get_user_followers(self, userid, count=100, fetch_all=False):
        users = []
        params = {
            'count': '12',
            'search_surface': 'follow_list_page',
        }
        url = f"https://www.instagram.com/api/v1/friendships/{userid}/followers/"

        while True:
            response = self.s.get(url, params=params, headers=self.__get_headers())
            for user in response.json()['users']:
                users.append(user) 

            if "next_max_id" in response.json():
                params["max_id"] = response.json()['next_max_id']
            else:
                break

            if fetch_all:
                continue
            else:
                if len(users) >= count:
                    users = users[:count]
                    break

        return users

    def get_self_followers(self, count=100, fetch_all=False):
        return self.get_user_followers(self.userID, count, fetch_all)

    def shortcode_to_id(self, shortcode):
        code = ('A' * (12-len(shortcode)))+shortcode
        return int.from_bytes(base64.b64decode(code.encode(), b'-_'), 'big')

    def id_to_shortcode(self, media_id):
        return base64.b64encode(media_id.to_bytes(9, 'big'), b'-_').decode().replace('A', ' ').lstrip().replace(' ', 'A')

    def change_password(self, newPassword):
        dateTime = int(datetime.now().timestamp())
        payload = {'enc_old_password': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{self.userPass}',
                   'enc_new_password1': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{newPassword}',
                   'enc_new_password2': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{newPassword}',
                  }

        headers = self.__get_headers(referer="https://www.instagram.com/accounts/password/change/", connection="close")
        response = self.s.post("https://www.instagram.com/api/v1/web/accounts/password/change/", headers=headers, data=payload)
        if response.ok:
            self.userPass = newPassword
        return printFunc(response, 'password changed')

    def get_user_media(self, username, count=12, fetch_all=False):
        medias = []
        params = {
            'count': '12',
        }
        url = f"https://www.instagram.com/api/v1/feed/user/{username}/username"
        while True:
            response = self.s.get(url, params=params, headers=self.__get_headers())
            for media in response.json()['items']:
                medias.append(media)
            if "next_max_id" in response.json():
                params["max_id"] = response.json()['next_max_id']
            else:
                break

            if fetch_all:
                continue
            else:
                if len(medias) >= count:
                    medias = medias[:count]
                    break

        return medias

    def like(self, mediaid):
        response = self.s.post(f'https://www.instagram.com/api/v1/web/likes/{mediaid}/like/', headers=self.__get_headers())
        return printFunc(response, "liked")

    def unlike(self, mediaid):
        response = self.s.post(f'https://www.instagram.com/api/v1/web/likes/{mediaid}/unlike/', headers=self.__get_headers())
        return printFunc(response, "unliked")

    def comment(self, mediaid, text):
        data = {
            'comment_text': text,
        }
        response = self.s.post(f'https://www.instagram.com/api/v1/web/comments/{mediaid}/add/', data=data, headers=self.__get_headers())
        return printFunc(response, "commented")

    def __get_image_size(self, filePath):
        file = {"file": open(filePath, "rb")}
        response = requests.post('https://imagesize.itertools.repl.co/upload/',files=file)
        return response.json()['width'], response.json()['height']

    def g_get_image_size(self, filePath):
        file = {"file": open(filePath, "rb")}
        response = requests.post('https://imagesize.itertools.repl.co/upload/',files=file)
        return response.json()['width'], response.json()['height']

    def save_media(self, mediaid):
        response = self.s.post(f"https://www.instagram.com/api/v1/web/save/{mediaid}/save/", headers=self.__get_headers())
        return printFunc(response, f"saved")

    def unsave_media(self, mediaid):
        response = self.s.post(f"https://www.instagram.com/api/v1/web/save/{mediaid}/unsave/", headers=self.__get_headers())
        return printFunc(response, f"unsaved")

    def get_media_info(self, mediaid):
        response = self.s.get(f"https://www.instagram.com/api/v1/media/{mediaid}/info/", headers=self.__get_headers())
        if response.ok:
            return response.json()
        else:
            printFunc(response, "got media info")
    
    def delete_media(self, mediaid):
        response = self.s.post(f"https://www.instagram.com/api/v1/web/create/{mediaid}/delete/", headers=self.__get_headers())
        return printFunc(response, "media deleted")
    
    def upload_photo(self, imagePath, caption="", tag_users=None, disable_comments="0", img_dimen=None):
        # img dimen = ['height', 'width']
        if not os.path.exists(imagePath):
            print('Image do not Exist !')
            return False
        upload_id = str(int(time.time() * 1000))
        if not img_dimen:
            image_width, image_height = self.__get_image_size(imagePath)
        else:
            image_height, image_width = img_dimen[0], img_dimen[1]
        headers = self.__get_headers(host="i.instagram.com",content_type="image/jpeg", 
                                                        addHeader={
                                                            'X-Entity-Type': 'image/jpeg',
                                                            'X-Entity-Name': f'fb_uploader_{upload_id}',
                                                            'Offset': '0',
                                                            'X-Instagram-Rupload-Params': f'{{"media_type":1,"upload_id":"{upload_id}","upload_media_height":{image_height},"upload_media_width":{image_width}}}',
                                                            'X-Entity-Length': str(os.path.getsize(imagePath)),
                                                            })
        
        response = self.s.post(f"https://i.instagram.com/rupload_igphoto/fb_uploader_{upload_id}", data=open(imagePath, "rb"), headers=headers)

        if tag_users:
            users = '{"in":['
            for user in tag_users:
                users += f'{{"position":[{random.uniform(0.01, 0.97)},{random.uniform(0.01, 0.97)}],"user_id":"{self.get_userid(user)}"}}'
                users += ','
            users = users[:-1] + ']}'
        else:
            users = ""

        data = {
                'source_type': 'library',
                'caption': caption,
                'upload_id': upload_id,
                'disable_comments': disable_comments,
                'like_and_view_counts_disabled': '0',
                'igtv_share_preview_to_feed': '1',
                'is_unified_video': '1',
                'video_subtitles_enabled': '0',
                'disable_oa_reuse': 'false',
                'usertags': users
            }

        response = self.s.post("https://www.instagram.com/api/v1/media/configure/", data=data, headers=self.__get_headers())
        return printFunc(response, "image uploaded")

    def get_media_likers(self, shortcode, count=24, fetch_all=False):
        likers = []
        params = {
            'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
            'variables': f'{{"shortcode":"{shortcode}","include_reel":true,"first":24}}',
        }

        url = f"https://www.instagram.com/graphql/query/"
        
        while True:
            response = self.s.get(url, params=params, headers=self.__get_headers())
            for liker in response.json()['data']['shortcode_media']['edge_liked_by']['edges']:
                likers.append(liker)
            if response.json()["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["has_next_page"] is True:
                params["variables"] = f'{{"shortcode":"{shortcode}","include_reel":true,"first":12,"after":"{response.json()["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]}"}}'
            else:
                break

            if fetch_all:
                continue
            else:
                if len(likers) >= count:
                    likers = likers[:count]
                    break

        return likers

    def upload_reel(self, videoPath, imageCover, caption="", vDimension=['#height', '#width'], vDuration_ms=0):
        #vDimension = [height, width]
        upload_id = str(int(time.time() * 1000))
        headers = self.__get_headers(host="i.instagram.com",content_type="video/mp4", 
                                                        addHeader={
                                                            'X-Entity-Type': 'video/mp4',
                                                            'X-Entity-Name': f'feed_{upload_id}',
                                                            'Offset': '0',
                                                            'X-Instagram-Rupload-Params': f'{{"client-passthrough":"1","is_unified_video":false,"is_sidecar":"0","media_type":2,"for_album":false,"video_format":"video/mp4","upload_id":{upload_id},"upload_media_duration_ms":{vDuration_ms},"upload_media_height":{vDimension[0]},"upload_media_width":{vDimension[1]},"video_transform":"center_crop","is_igtv_video":false,"is_clips_video":true,"uses_original_audio":true,"audio_type":"original_sounds"}}',
                                                            'X-Entity-Length': str(os.path.getsize(videoPath)),
                                                            'Sec-Fetch-Dest': 'document',
                                                            })
        response = self.s.post(f"https://i.instagram.com/rupload_igvideo/feed_{upload_id}", data=open(videoPath, "rb"), headers=headers)
        headers = self.__get_headers(host="i.instagram.com",content_type="image/jpeg", 
                                                        addHeader={
                                                            'X-Entity-Type': 'image/jpeg',
                                                            'X-Entity-Name': f'feed_{upload_id}',
                                                            'Offset': '0',
                                                            'X-Instagram-Rupload-Params': f'{{"media_type":2,"upload_id":"{upload_id}","upload_media_height":{vDimension[0]},"upload_media_width":{vDimension[1]}}}',
                                                            'X-Entity-Length': str(os.path.getsize(imageCover)),
                                                            'Sec-Fetch-Dest': 'document',
                                                            })
        response = self.s.post(f"https://i.instagram.com/rupload_igphoto/feed_{upload_id}", data=open(imageCover, "rb"), headers=headers)
        
        data = {'upload_id': upload_id,
                'caption': caption,
                'usertags': '',
                'custom_accessibility_caption': '',
                'retry_timeout': '12',
                'clips_uses_original_audio': '1',
                'uses_original_audio': '1',
                'original_audio': '1',
                'audio': '1',
                'clips_audio': '1',
                'clips_with_audio': '1',
                'with_audio': '1',
                'enable_audio': '1',
                'clips_enable_audio': '1',
                'clips_audio_enable': '1',
                'audio_enable': '1',
                'audio_type': 'original_sounds',
                'clips_share_preview_to_feed': '1'}
        response = self.s.post("https://i.instagram.com/api/v1/media/configure_to_clips/", data=data, headers=self.__get_headers(host="i.instagram.com"))
        return printFunc(response, "reel_uploaded")

    def get_saved_medias(self, count=10, fetch_all=False):
        medias = []
        params = {
        }
        url = f"https://www.instagram.com/api/v1/feed/saved/posts/"

        while True:
            response = self.s.get(url, params=params, headers=self.__get_headers())
            for media in response.json()['items']:
                medias.append(media['media']) 

            if "next_max_id" in response.json():
                params["max_id"] = response.json()['next_max_id']
            else:
                break

            if fetch_all:
                continue
            else:
                if len(medias) >= count:
                    medias = medias[:count]
                    break

        return medias
    
    def logout(self):
        data = {
            'one_tap_app_login': '0',
            'user_id': self.userID,
        }

        response = self.s.post('https://www.instagram.com/api/v1/web/accounts/logout/ajax/', headers=self.__get_headers(), data=data)
        self.loggedIn = False
        printFunc(response, "logged out")

    def post_data(self, endpoint_url, payload_json={}, extra_headers={}): 
        response = self.s.post(endpoint_url, headers=self.__get_headers(addHeader=extra_headers, check_logged_in=False), data=payload_json)
        return response

    def get_data(self, endpoint_url, params={}, extra_headers={}):
        response = self.s.get(endpoint_url, params=params, headers=self.__get_headers(addHeader=extra_headers, check_logged_in=False))
        return response
    
    def solve_login_checkpoint(self, login_json_response):
        r = self.s.post(login_json_response['checkpoint_url'], data={"choice": "1"}, headers=self.__get_headers(check_logged_in=False))
        if printFunc(r, "otp sent"):
            response = self.s.post(login_json_response['checkpoint_url'], data={"code": int(input("Enter Code : "))}, headers=self.__get_headers(check_logged_in=False))

            if printFunc(response, "logged in"):
                self.loggedIn = True