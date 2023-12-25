import arxiv
import concurrent.futures
from src.arxiv_utils.arxiv_api import arxiv_search_api, get_paper_code_url
from src.arxiv_utils.github_api import get_stars
from src.arxiv_utils.baidu_trans_api import baidu_trans


def process_paper(paper_result):
    code_url = paper_result["paper_code_url"]
    github_code_url = get_paper_code_url(code_url)
    if github_code_url:
        stars = get_stars(github_code_url)
    else:
        stars = None

    paper_abstract = paper_result["paper_abstract"]
    paper_abstract_zh = baidu_trans(paper_abstract)

    paper_url = paper_result["paper_url"] # 获取paper_url
    paper_url = "[`link`]({})".format(paper_url) # 获取paper_url

    github_code_url = "[`link`]({})".format(github_code_url) if github_code_url else None

    case_list = [
        paper_result["paper_title"],
        paper_result["paper_first_author"],
        paper_result["paper_abstract"],
        paper_abstract_zh,
        paper_url,
        github_code_url,
        stars,
        paper_result["paper_categories"],
        paper_result["paper_publish_time"]
    ]
    return case_list


def arxiv_search(query, search_type, sort_order, start_index, last_index):
    if search_type == "SubmittedDate":
        search_type = arxiv.SortCriterion.SubmittedDate
    elif search_type == "Relevance":
        search_type = arxiv.SortCriterion.Relevance
    elif search_type == "LastUpdatedDate":
        search_type = arxiv.SortCriterion.LastUpdatedDate
    else:
        search_type = arxiv.SortCriterion.SubmittedDate
    
    if sort_order == "DeScending":
        sort_order = arxiv.SortOrder.Descending
    elif sort_order == "Ascending":
        sort_order = arxiv.SortOrder.Ascending
    else:
        sort_order = arxiv.SortOrder.Descending

    start_index = int(start_index)
    last_index = int(last_index)

    paper_result_list = arxiv_search_api(query, sort_by=search_type, sort_order=sort_order, start_index=start_index, last_index=last_index)

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_paper = {executor.submit(process_paper, paper): paper for paper in paper_result_list}
        for future in concurrent.futures.as_completed(future_to_paper):
            paper = future_to_paper[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                print(f"Exception occurred: {e}")
    return results
