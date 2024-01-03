import gradio as gr
from src.arxiv_utils.arxiv_search import arxiv_search


def main():
    with gr.Blocks(title="StreamEase") as demo:
        # 设置标题
        title_html = f"<h1 align=\"center\">StreamEase</h1>"
        gr.HTML(title_html)

        # Arxiv论文检索
        with gr.Tab("Arxiv"):
            with gr.Row(equal_height=False):
                # 存储历史记录
                history = gr.State([])

                # 创建Chatbot
                arxiv_value = [(
                "【Arxiv论文检索】简介",
                """**【Arxiv论文检索】** 返回论文标题、作者、发表时间、分类、论文链接、代码链接、代码仓star数、中英文摘要\n
                使用方法：
                1、选择搜索排序方式，[SubmittedDate|Relevance|LastUpdatedDate] 分别代表 [论文提交日期|相关性|论文最近更新日期]
                2、选择索引，根据索引范围返回结果（Start index ~ Last index）
                3、输入检索关键词，推荐以英文关键词检索，词组用英文双引号括起来，不同词或词组中间用 [AND|OR|ANDNOT] 连接
                例如："medical image segmentation" AND prostate
                """
                )]
                with gr.Column(scale=5):
                    chatbot = gr.Chatbot(arxiv_value, elem_id="chatbot", height=800)

                with gr.Column(scale=2):
                    # 检索排序方式
                    sort_results_by = gr.Dropdown(
                        ["SubmittedDate(newest first)", "SubmittedDate(oldest first)",
                        "Relevance(newest first)", "Relevance(oldest first)",
                        "LastUpdatedDate(newest first)", "LastUpdatedDate(oldest first)"],
                        label="Sort results by", value="SubmittedDate(newest first)",
                        interactive=True, allow_custom_value=False
                    )

                    # 检索索引
                    with gr.Row():
                        start_index = gr.Number(label="Start index", value=0, minimum=0, maximum=200, step=5)
                        last_index = gr.Number(label="Last index", value=5, minimum=0, maximum=200, step=5)

                    # 检索输入
                    search_input = gr.Textbox(label="Search input")

                    # 检索启动按钮
                    search_button = gr.Button(variant="primary")

            # 检索启动按钮关联
            search_button.click(arxiv_search, inputs=[search_input, history, sort_results_by, start_index, last_index], outputs=[chatbot, history])

        # 文档助手
        with gr.Tab("docs"):
            pass
    demo.launch()


if __name__ == "__main__":
    main()