# BeBr2-Legal-Search

## 简介

本仓库是2022-2023年春季学期《搜索引擎技术基础》大作业选题一：司法搜索引擎的一个实现。

使用python的flask构建后端，vue构建前端，实现了用户友好的关键词检索、类案检索等必做功能，以及精细化检索、高亮、标签显示、查询补全、相似案例推荐等选做功能。

## 代码结构

`reports`文件夹是实验报告

`search`文件夹是核心算法实现

`flask`文件夹是后端

`bebr2-legal`文件夹是前端

`data`文件夹是预处理前后的所有文件，其中，`index`储存whoosh索引，`processed`储存xml提取后的json文件，`Legal_data`是助教提供的原xml文件，`tokenizer`和`lawformer`是NLP模型相关，`vector_index`储存faiss建立的稠密向量索引。

其他本项目的详细说明（包括模块实现、Demo展示等）见实验报告。

## 如何运行

### python依赖

```
elasticsearch==8.8.0
faiss==1.5.3
faiss_cpu==1.7.4
jieba==0.42.1
numpy==1.21.6
tqdm==4.64.1
Whoosh==2.7.4
Flask==2.2.4
transformers==4.28.0
```

### Elastic search启动

启动Elastic search服务。

### 预处理

首先，需要在`./process/`文件夹下依次运行：

```
python extract_xml.py
python get_index.py
python get_es_index.py
python get_vector_index.py
python law_words.py
python get_database.py
```

### 前端运行

在`bebr2-legal`文件夹下：

```
npm install
npm run serve
```

注意其中使用了一些CDN资源，请在联网状态下启动。

### 后端运行

在`flask`文件夹下，可以修改`config.py`自定义配置，最后运行：

```
flask run --port 8000
```

启动后端。注意，如果所有配置都启动，比较耗内存，我16GB的电脑多开了很多虚存勉强能跑得动。