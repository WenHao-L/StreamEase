# StreamEase

StreamEase 工具箱是一款提升工作效率的软件，目前支持 Arxiv 论文检索。

![Arxiv_1](./docs/img/Arxiv_1.png)

<!-- ![Arxiv_2](./docs/img/Arxiv_2.png) -->

## 功能

- ArXiv 论文检索

    - 提取论文标题、作者、发表时间、分类、论文链接、代码链接、代码仓star数、中英文摘要


## Quick Start

### API

- 百度翻译 API 获取

    注册 [百度翻译开放平台](https://api.fanyi.baidu.com/) 账号，申请通用文本翻译 API（高级版），每月有100万字符免费翻译
    
    替换 [config.py](./config.py) 中的 `BAIDU_APP_ID` 和 `BAIDU_APP_KEY`
    
    ```python
    BAIDU_APP_ID = ""
    BAIDU_APP_KEY = ""
    ```

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python app.py
```

## 使用方法

### Arxiv 论文检索

- 检索语法：(英文检索)

    - 单个关键词：[关键词]

        ```
        segmentation
        ```

    - 多个关键词：[关键词1] [布尔运算符] [关键词2] [布尔运算符] ...
    
        布尔运算符：`AND` 表示交集 (同时存在A和B)、`OR` 表示并集 (A或者B)、`ANDNOT` 表示差集 (A中不包含B)

        ```
        segmentation AND prostate
        segmentation OR classification
        segmentation ANDNOT U-Net
        ```

    - 词组：["词组"]，用英文双引号括起来

        ```
        "medical image segmentation"
        ```

    - 组合检索：[关键词 / "词组"] [布尔运算符] [关键词 / "词组"]

        ```
        "medical image segmentation" AND prostate
        ```

- 搜索排序

    - **Sort results by**：
    
        搜索排序方式，[`SubmittedDate` / `Relevance` / `LastUpdatedDate`]，分别代表 [`论文提交日期`|`相关性`|`论文最近更新日期`]
    
    
    - **Start index** & **Last index**

        检索结果的起始和结束索引
