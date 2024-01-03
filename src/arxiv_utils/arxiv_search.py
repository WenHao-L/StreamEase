import arxiv
import concurrent.futures
from src.arxiv_utils.arxiv_api import arxiv_search_api, get_paper_code_url
from src.arxiv_utils.github_api import get_stars
from src.arxiv_utils.baidu_trans_api import baidu_trans


def list2md(str_list):
    result = """
    **标题：{}**\n
    作者：{}
    发表时间：{}
    分类：{}
    论文链接：{}
    代码链接：{}
    代码仓star数：{}\n
    **中文摘要：**
    {}\n
    **英文摘要：**
    {}\n
    ---------------------------------\n
    """.format(str_list[0], str_list[1], str_list[2], str_list[3], str_list[4],
               str_list[5], str_list[6], str_list[7], str_list[8])
    return result


def post_processing(paper_result):
    code_url = paper_result["paper_code_url"]
    github_code_url = get_paper_code_url(code_url)
    if github_code_url:
        stars = get_stars(github_code_url)
    else:
        stars = "NA"

    paper_abstract = paper_result["paper_abstract"]
    paper_abstract_zh = baidu_trans(paper_abstract)

    paper_url = "[`link`]({})".format(paper_result["paper_url"])
    github_code_url = "[`link`]({})".format(github_code_url) if github_code_url != "NA" else "NA"

    str_list = [
        paper_result["paper_title"],
        paper_result["paper_authors"],
        paper_result["paper_publish_time"],
        paper_result["paper_categories"],
        paper_url,
        github_code_url,
        stars,
        paper_abstract_zh,
        paper_result["paper_abstract"],
    ]
    result = list2md(str_list)
    return result


def arxiv_search(query, history, sort_results_by, start_index, last_index):
    # 
    prompt = "【Arxiv论文检索】 检索关键词如下：\n"
    prompt_query = prompt + query
    history.append(prompt_query)

    if query == "":
        history.append("[Error] 检索输入不能为空，请重新输入")
        responses = [(u, b) for u, b in zip(history[::2], history[1::2])]
        return responses, history

    # 根据sort_results_by设置对应的检索排序方式
    if sort_results_by == "SubmittedDate(newest first)":
        sort_by = arxiv.SortCriterion.SubmittedDate
        sort_order = arxiv.SortOrder.Descending
    elif sort_results_by == "SubmittedDate(oldest first)":
        sort_by = arxiv.SortCriterion.SubmittedDate
        sort_order = arxiv.SortOrder.Ascending
    elif sort_results_by == "Relevance(newest first)":
        sort_by = arxiv.SortCriterion.Relevance
        sort_order = arxiv.SortOrder.Descending
    elif sort_results_by == "Relevance(oldest first)":
        sort_by = arxiv.SortCriterion.Relevance
        sort_order = arxiv.SortOrder.Ascending
    elif sort_results_by == "LastUpdatedDate(newest first)":
        sort_by = arxiv.SortCriterion.LastUpdatedDate
        sort_order = arxiv.SortOrder.Descending
    elif sort_results_by == "LastUpdatedDate(oldest first)":
        sort_by = arxiv.SortCriterion.LastUpdatedDate
        sort_order = arxiv.SortOrder.Ascending
    else:
        history.append("[Error] (Sort results by) 检索排序方式出错，请重新选择检索排序方式")
        responses = [(u, b) for u, b in zip(history[::2], history[1::2])]
        return responses, history


    # 转换start_index, last_index为int类型，并判断两者的大小
    start_index, last_index = int(start_index), int(last_index)
    if start_index >= last_index:
        history.append("[Error] 索引设置出错，Last index 必须大于 Start index")
        responses = [(u, b) for u, b in zip(history[::2], history[1::2])]
        return responses, history

    # 爬取arxiv
    paper_result_list = arxiv_search_api(query, sort_by=sort_by, sort_order=sort_order, start_index=start_index, last_index=last_index)
    if paper_result_list == []:
        history.append("[Warning] Arxiv网站爬取过于频繁，请稍后再试")
        responses = [(u, b) for u, b in zip(history[::2], history[1::2])]
        return responses, history

    # 多线程获取代码链接、github仓库star数以及对返回结果做格式转换
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_paper = {executor.submit(post_processing, paper): paper for paper in paper_result_list}
        for future in concurrent.futures.as_completed(future_to_paper):
            paper = future_to_paper[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                pass
    
    response = "".join(results)
    history.append(response)

    responses = [(u, b) for u, b in zip(history[::2], history[1::2])]
    return responses, history
