import requests
import arxiv


# 获取作者
def get_authors(authors, first_author = False):
    try:
        output = str()
        if first_author == False:
            output = ", ".join(str(author) for author in authors)
        else:
            output = str(authors[0])
        return output
    except:
        return

# 爬取arxiv
def arxiv_search_api(query, sort_by=arxiv.SortCriterion.SubmittedDate, sort_order=arxiv.SortOrder.Descending, start_index=0, last_index=10, page_size=10):
    base_url = "https://arxiv.paperswithcode.com/api/v0/papers/"
    paper_result_list = []

    client = arxiv.Client(page_size=page_size, delay_seconds=3)

    arxiv_search = arxiv.Search(
        query=query,
        max_results=last_index,
        sort_by=sort_by,
        sort_order=sort_order
    )

    results = client.results(arxiv_search, offset=start_index)
    for result in results:
        paper_id = result.get_short_id() # 文章id
        paper_title = result.title # 文章标题
        paper_url = result.entry_id # 文章url
        paper_code_url = base_url + paper_id # 代码url
        paper_abstract = result.summary.replace("\n", "") # 文章摘要需要剔除格式
        paper_first_author = get_authors(result.authors, first_author=True) # 文章的第一作者
        paper_categories = result.primary_category # 文章的分类
        paper_publish_time = result.published.date() # 文章的发布时间

        paper_result = {"paper_id": paper_id,
                        "paper_title": paper_title,
                        "paper_url": paper_url,
                        "paper_code_url": paper_code_url,
                        "paper_abstract": paper_abstract,
                        "paper_first_author": paper_first_author,
                        "paper_categories": paper_categories,
                        "paper_publish_time": paper_publish_time}
        paper_result_list.append(paper_result)
    return paper_result_list


# 获取代码链接
def get_paper_code_url(code_url):
    code_response = requests.get(code_url, verify=False).json()
    if "official" in code_response and code_response["official"]:
        github_code_url = code_response["official"]["url"]
        return github_code_url
    else:
        return