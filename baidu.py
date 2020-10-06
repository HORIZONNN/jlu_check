import requests
from urllib.parse import urlencode


def get_file_list(access_token, cloud_file_path):

    ### baidunetdisk params
    baidu_link = "https://pan.baidu.com/rest/2.0/xpan/file?method=imagelist&"

    params = {
        'access_token' : None,
        'order' : 'name',
        'desc' : '0',
        'parent_path' : None
    }

    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    ### get baidunetdisk files
    temp_params = params 
    temp_params['access_token'] = access_token
    temp_params['parent_path'] = cloud_file_path

    url = baidu_link + urlencode(temp_params)

    results = requests.get(url, headers=headers)
    file_names = []
    if results.status_code == 200:
        for file_info in results.json().get('info'):
            file_names.append(file_info.get('server_filename'))

        return file_names
    else:
        print("failed to get baidunetdisk file list! response code:{}".format(results.status_code))
        return None

    


