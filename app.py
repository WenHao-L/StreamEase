import gradio as gr
from src.arxiv_utils.arxiv_search import arxiv_search


with gr.Blocks() as demo:
    # 设置标题
    gr.Markdown("<h1>StreamEase</h1>")

    # 设置tab选项卡
    with gr.Tab("Arxiv"):
        search_input = gr.Textbox(label="Search input")

        with gr.Row():
            search_type = gr.Dropdown(
                ["SubmittedDate", "Relevance", "LastUpdatedDate"], label="Search type", value="SubmittedDate", interactive=True, allow_custom_value=False
            )
            sort_order = gr.Dropdown(["Descending", "Ascending"], label="Sort order", value="Descending", interactive=True, allow_custom_value=False)
            start_index = gr.Number(label="Start index", value=0, step=10, minimum=0)
            last_index = gr.Number(label="Last index", value=10, step=10, minimum=0, maximum=200)
            search_button = gr.Button(variant="primary")

        search_output = gr.DataFrame(label='Search output',
                                     headers=["title", "author", "abstract", "abstract_zh", "paper_url", "code_url", "code_stars", "categories", "publish_time"],
                                     row_count=10,
                                     col_count=9,
                                     datatype=["str", "str", "str", "str", "markdown", "markdown", "str", "str", "str"],
                                     wrap=True)

        search_button.click(arxiv_search, inputs=[search_input, search_type, sort_order, start_index, last_index], outputs=search_output)

demo.launch()
