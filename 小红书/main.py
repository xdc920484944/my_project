# https://tophub.today/n/L4MdA5ldxD

import requests
import json
import time


# 笔记数，作者（ID，作者名称，关注量，粉丝量，获赞与收藏量，所有笔记数），笔记内容，评论用户ID，用户昵称，评论内容，评论时间，点赞量，展开折叠的二级评论（用户ID，用户昵称，评论内容，评论时间，点赞量）

# 单个作品数据
# 用户ID、用户名称，文章（发布时间，发布内容，ID），赞收评数量
def get_art():
    '''
    获取文章详情
    :return:
    '''
    url = 'https://edith.xiaohongshu.com/api/sns/v1/note/feed?note_id=6034d2a40000000021034590&page=1&num=5&fetch_mode=1&source=explore&ads_track_id='
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Plus Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(OPPO;OPPO R11 Plus) discover/6.72.0 NetType/WiFi',
        'X-B3-TraceId': '6666a977b9180500',
        'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1615364387&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1615365503&build=6720194&x_trace_page_current=explore_feed&lang=zh-Hans&channel=YingYongBao',
        'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbIpIME2fquAplAEWU/8cM+R',
        'xy-platform-info': 'platform=android&build=6720194&deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f',
        'Host': 'edith.xiaohongshu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'

    }
    r = requests.get(url=url, headers=headers)
    print(r.status_code)


# 获取作品评论
# 二级评论（用户ID，用户昵称，内容，时间）,评论（用户ID，用户昵称，内容，时间，点赞）
# def get_comment():
#     url = 'https://edith.xiaohongshu.com/api/sns/v5/note/comment/list?note_id=6034d2a40000000021034590&start=&num=15&show_priority_sub_comments=0&source=explore&top_comment_id='
#     headers = {
#         'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Plus Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(OPPO;OPPO R11 Plus) discover/6.72.0 NetType/WiFi',
#         'X-B3-TraceId': '1c1cb277be1d080f',
#         'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1615364387&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1615365503&build=6720194&x_trace_page_current=explore_feed&lang=zh-Hans&channel=YingYongBao',
#         'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbIpIME2fquAplAEWU/8cM+R',
#         'xy-platform-info': 'platform=android&build=6720194&deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f',
#         'Host': 'edith.xiaohongshu.com',
#         'Connection': 'Keep-Alive',
#         'Accept-Encoding': 'gzip'
#
#     }
#
#     r = requests.get(url=url, headers=headers)
#     print(r.status_code)
#     return r


# 用户信息 https://edith.xiaohongshu.com/api/sns/v3/user/info?user_id=5b40468ae8ac2b1a7eefb6b1
def get_user_information(userid):
    headers = {
        'X-B3-TraceId': '9898cc2a0b100400',
        'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1607927723&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1607930031&build=6720194&x_trace_page_current=user_fans_page&lang=zh-Hans&channel=YingYongBao',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(huawei;VOG-AL10) discover/6.72.0 NetType/WiFi',
        'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbId1luTYatqFPCmcHKqKddu',
        'xy-platform-info': 'platform=android&build=6720194&deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f',
        'Host': 'edith.xiaohongshu.com',
    }
    url = 'https://edith.xiaohongshu.com/api/sns/v3/user/info?user_id=5b40468ae8ac2b1a7eefb6b1'
    res = requests.get(url=url, headers=headers)
    print(res.text)


# 粉丝列表 https://www.xiaohongshu.com/api/sns/v1/user/5a1cead9db2e6001d996adf8/followers?start=用户id
def get_user_list():
    headers = {
        'X-B3-TraceId': '67672f8206180a0f',
        'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1607927723&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1607932083&build=6720194&x_trace_page_current=user_fans_page&lang=zh-Hans&channel=YingYongBao',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; VOG-AL10 Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(huawei;VOG-AL10) discover/6.72.0 NetType/WiFi',
        'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbIreHzD9PDjInVyZE4AKGDL',
        'xy-platform-info': 'platform=android&build=6720194&deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f',
        'Host': 'www.xiaohongshu.com'
    }
    url = 'https://www.xiaohongshu.com/api/sns/v1/user/5a1cead9db2e6001d996adf8/followers?start='
    res = requests.get(url=url, headers=headers)
    print(res.text)


def search_word(key_word, page):
    '''
    # https://edith.xiaohongshu.com/api/sns/v10/search/notes?keyword=科技&page=1&page_size=20&source=explore_feed&api_extra=&page_pos=0&pin_note_id=&allow_rewrite=1&geo=eyJsYXRpdHVkZSI6MjUuOTk3ODg1LCJsb25naXR1ZGUiOjEwNy41Njc2MzV9
    # https://edith.xiaohongshu.com/api/sns/v10/search/notes?keyword=科技&page=2&page_size=20&source=explore_feed&api_extra=&page_pos=22&pin_note_id=&allow_rewrite=1&geo=eyJsYXRpdHVkZSI6MjUuOTk3ODg1LCJsb25naXR1ZGUiOjEwNy41Njc2MzV9
    # https://edith.xiaohongshu.com/api/sns/v10/search/notes?keyword=科技&page=3&page_size=20&source=explore_feed&api_extra=&page_pos=42&pin_note_id=&allow_rewrite=1&geo=eyJsYXRpdHVkZSI6MjUuOTk3ODg1LCJsb25naXR1ZGUiOjEwNy41Njc2MzV9
    根据关键词获取数据
    :param key_word:str 关键词
    :param page:int 页数 从0开始
    :return:
    '''

    def filter_search_result(search_result):
        '''
        过滤提取搜索结果
        :param search_result: 搜索结果
        :return: list
        '''
        data = []
        for n in search_result['data']['items']:
            if n.get('note'):
                art = n['note']
                result = {}
                # note
                result['note_id'] = art.get('id')
                result['note_title'] = art.get('title')
                result['note_desc'] = art.get('desc')
                result['note_liked_count'] = art.get('liked_count')
                result['note_type'] = art.get('type')
                result['note_timestamp'] = art.get('timestamp')
                if result['note_type'] == 'video':
                    result['url'] = art.get('video_info').get('url')
                # user
                result['user_id'] = art.get('user').get('userid')
                result['user_nickname'] = art.get('user').get('nickname')
                data.append(result)
        return data

    url = 'https://edith.xiaohongshu.com/api/sns/v10/search/notes?' \
          'keyword={}&page={}&page_size=20&source=explore_feed&api_extra=&page_pos={}&' \
          'pin_note_id=&allow_rewrite=1&geo=eyJsYXRpdHVkZSI6MjUuOTk3ODg1LCJsb25naXR1ZGUiOjEwNy41Njc2MzV9'.format(
        key_word, page, page * 22)
    headers = {
        'X-B3-TraceId': '94944ba23b180100',
        'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1615511019&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1615511201&build=6720194&x_trace_page_current=search_result_notes&lang=zh-Hans&channel=YingYongBao',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Plus Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(OPPO;OPPO R11 Plus) discover/6.72.0 NetType/WiFi',
        'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbLocnHZVCSVlOS66QDYZ04o',
    }
    res = requests.get(url=url, headers=headers)
    if 200 <= res.status_code < 300:
        json_r = json.loads(res.text)
        result = filter_search_result(search_result=json_r)
        return result
    else:
        return None


def get_comment(note_id):
    '''
    获取评论
    # https://edith.xiaohongshu.com/api/sns/v5/note/comment/list?note_id=5ff2f7b1000000000100adb7&start=&num=20&show_priority_sub_comments=0&source=search&keyword=科技&searchId=2898w7izan9zketuro6ww&top_comment_id=
    # https://edith.xiaohongshu.com/api/sns/v5/note/comment/list?note_id=5ff2f7b1000000000100adb7&start=5ffaeca00000000001024982&num=10&show_priority_sub_comments=0&source=search&keyword=科技&searchId=2898w7izan9zketuro6ww&top_comment_id=
    # https://edith.xiaohongshu.com/api/sns/v5/note/comment/list?note_id=5ff2f7b1000000000100adb7&start=5ff5a26e000000000102bcf4&num=10&show_priority_sub_comments=0&source=search&keyword=科技&searchId=2898w7izan9zketuro6ww&top_comment_id=

    :param retry:
    :param note_id:文章id
    :return:
    '''

    def deal_comment(comment):
        '''
        处理单个评论
        :param comment:一个评论
        :return: dict
        '''
        one_comment_dict = {
            'content': comment.get('content'),
            'like_count': comment.get('like_count'),
            'time': comment.get('time'),
            'track_id': comment.get('track_id'),
            'sub_comment': [deal_comment(l) for l in comment.get('sub_comments')] if comment.get(
                'sub_comments') else [],
            'user_id': comment.get('user').get('userid'),
            'nickname': comment.get('user').get('nickname')
        }
        return one_comment_dict

    headers = {
        # 'X-B3-TraceId': 'd9d91e6e47150b0f',
        # 'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1615511019&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1615519442&build=6720194&x_trace_page_current=note_comment_page&lang=zh-Hans&channel=YingYongBao',
        # 'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Plus Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(OPPO;OPPO R11 Plus) discover/6.72.0 NetType/WiFi',
        # 'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbLzRF0s4ZqdXRjO783maHuZ',
        # 'xy-platform-info': 'platform=android&build=6720194&deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f',
        # 'Host': 'edith.xiaohongshu.com',
        # 'Connection': 'Keep-Alive',
        # 'Accept-Encoding': 'gzip'
        'X-B3-TraceId': '5c5c83e3351c0600',
        'xy-common-params': 'deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f&identifier_flag=2&tz=Asia%2FShanghai&fid=160791595610c18d8d91fc652ab176f6684a66c37fc2&app_id=ECFAAF01&device_fingerprint1=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&uis=light&launch_id=1615774662&project_id=ECFAAF&device_fingerprint=202012141119216795a2c98a54fc6bfdaa735ccf33c6f501db3d94c293bdf5&versionName=6.72.0&platform=android&sid=session.1607916729133564751495&t=1615775460&build=6720194&x_trace_page_current=note_comment_page&lang=zh-Hans&channel=YingYongBao',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Plus Build/NMF26X) Resolution/1600*900 Version/6.72.0 Build/6720194 Device/(OPPO;OPPO R11 Plus) discover/6.72.0 NetType/WiFi',
        'shield': 'XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJfuFXTalLlo3mm7FkH535/OYNz8N4ish+2Kc7RgxNR2COZ7Km2H0ygbJRlD2csXd5PAdli9CdftRf',
        'xy-platform-info': 'platform=android&build=6720194&deviceId=9c9f573c-136b-3bf5-959f-3f5639b4fb7f',
        'Host': 'edith.xiaohongshu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    num_dict = ['', '5ff3502b000000000102560b']  # 第0 50个
    result = []
    comment_count = None
    for code in num_dict:
        url = 'https://edith.xiaohongshu.com/api/sns/v5/note/comment/list?note_id={}&start={}&num=50&show_priority_sub_comments=0&source=search&keyword=科技&searchId=2898w7izan9zketuro6ww&top_comment_id=' \
            .format(note_id, code)
        res = requests.get(url=url, headers=headers)
        time.sleep(3)
        if 200 <= res.status_code < 300:
            comments = json.loads(res.text)
            if comment_count is None:
                comment_count = comments.get('data').get('comment_count_l1')
            comment_list = [deal_comment(c) for c in comments['data']['comments']]
            result += comment_list
        # else:
        #     res = requests.get(url=url, headers=headers)
    return result, comment_count


if __name__ == '__main__':
    d = search_word(key_word='科技', page=0)
    print(d)
    # for n in range(len(d[:5])):
    #     print(n)
    #     _id = d[n]['note_id']
    #     comm, count = get_comment(note_id=_id)
    #     d[n]['comments_count'] = count
    #     d[n]['comments'] = comm

