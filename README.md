# 概述

这是几个LLM编程的例子，建议先安装依赖库 pip install -r requirements.txt

#  prompt_demo

根据提示词生成回答问题，生成图片，以及OCR识别三个例子

#  tool_demo

演示Function Calling
call_func: 根据提示词让大模型调用工具回答问题，例如：strawberry中有多少个r，9.11和9.9，哪个小?
ask_question: 为班级AI评价做的一个小Demo，能回答关于LMS的一些问题，例如：哪个学生没参加最近一次活动，哪个学生的成绩进步最大

#  mcp_demo

server.py client.py 按照MCP协议实现了MCP服务器和客户端，运行mcp_client.py可以看到效果
mcp_server.py mcp_client.py mcp_agent.py 把MCP功能包装成agent    


#  rag_demo 

这是一个基于西游记白话文版本构建的 RAG_Agent (检索增强生成) 智能问答系统。该项目使用西游记白话文文本作为知识库，通过 RAG_AGENT 技术实现对西游记相关问题的智能回答。

## 数据集说明

本项目使用改编版《西游记》白话文作为基础数据集. 

## 功能特性

项目主要分为三个部分

- 文本预处理 (etl.py)
  - 文本清洗
  - 格式标准化
  - 批量处理文件

- 文本分块 (split_chunk.py) 
  - 按语义分块
  - 生成检索单元

- RAG 问答 (rag_agent.py)
  - 基于检索的问答系统
  - 智能理解西游记相关问题
  - 准确检索相关内容
  - 生成连贯答案


