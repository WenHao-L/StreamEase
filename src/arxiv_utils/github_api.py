import requests


# 获取代码仓的star数
def get_stars(github_code_url):
    try:
        # 构建GitHub API的URL
        api_url = f"https://api.github.com/repos/{github_code_url.split('github.com/')[-1]}"
        
        # 发送GET请求到GitHub API
        response = requests.get(api_url)
        
        # 检查响应状态码
        if response.status_code == 200:
            # 解析JSON响应并获取star数
            data = response.json()
            stars = str(data['stargazers_count'])
            return stars
        else:
            return "NA"
    except:
        return "NA"