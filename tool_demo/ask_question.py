from openai import OpenAI
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from tool_spec import tools
from tool_func import *

load_dotenv()


client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def get_response(messages):
    completion = client.chat.completions.create(
        model='qwen-max',   #实测 qwen-max 比 qwen-plus 效果更好
        messages=messages,
        temperature=0.01,
        top_p=0.95,
        stream=False,
        tools=tools
    )
    print("返回对象：")
    print(completion.choices[0].message.model_dump_json())
    print("\n")
    return completion


def ask_question(question):
    print('\n')
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个聪明的学生成绩诊断分析助手. "
                "能够调用函数查询班级内学生参加各项活动的成绩和排名，给出良好的学习建议"
                "请始终使用中文回答问题。"
                "班级、学生、课程、单元、活动、成绩、排名的关系如下："
                "班级包含多个学生，学生参加班级内的活动，活动有对应的成绩"
                "班级下有多门课程，课程下有多个单元、单元下有多个活动，每个活动都有部分学生参加，参加者有对应的成绩。"
                "学生总成绩是根据学生参加的所有活动的成绩计算得出的，要查询学生总成绩，需要查学生参加的所有活动。"
                # "要查询学生参加的所有活动，先查询班级下所有课程，再依次查每个课程下所有单元，再依次查每个单元下所有活动，再依次查每个活动的参与学生。"
                "单个课程的学生成绩是根据课程下所有活动的成绩计算得出的。"
                "当我问哪个学生时没参加某次活动这类查询人的问题时，都要将学生ID转换为学生姓名。"
                "你可以问我："
                "最近一次活动的参与人数"
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    # 模型的第一轮调用
    current_response = get_response(messages)
    round_number = 1

    # 从返回的结果中获取函数名称和入参
    function_name = current_response.choices[0].message.tool_calls[0].function.name
    arguments_string = current_response.choices[0].message.tool_calls[0].function.arguments

    # 使用json模块解析参数字符串
    arguments = json.loads(arguments_string)

    while current_response.choices[0].finish_reason == 'tool_calls':  # 循环直到模型判断无需调用工具
        assistant_output = current_response.choices[0].message
        finish_reason = current_response.choices[0].finish_reason
        print(f"\n大模型第 {round_number} 轮输出信息：{current_response}\n")
        messages.append(assistant_output)
        
        tool_info = {}       

        # 获取工具调用信息
        tool_call = assistant_output.tool_calls[0]
        func_name = tool_call.function.name
        
        # 设置工具信息
        tool_info = {"name": func_name, "role": "tool"}
        
        # 获取函数参数（如果有）
        print(tool_call.function.arguments)
        args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        
        # 动态调用对应的函数
        func = globals()[func_name]
        if args:
            tool_info['content'] = func(**args)
        else:
            tool_info['content'] = func()

        print(f"工具名称: {func_name}")
        print(f"工具参数: {args}")

        if tool_info['content'] is not None:
            print(f"工具输出信息：{tool_info['content']}\n")
            messages.append(tool_info)     

        # 模型的第N轮调用，最后轮对工具的输出进行总结
        current_response = get_response(messages)
        round_number += 1


    final_result = current_response.choices[0].message.content
    print(f"大模型第 {round_number} 轮输出信息：{current_response}\n")
    if(current_response is not None):
        print(final_result)
    else:
        final_result = "没有找到答案"

    return final_result



if __name__ == '__main__':
    
    # 测试一下本文件中的工具函数
    # print("班级内学生:" + get_class_students())
    # print("学生ID为1的姓名:" + get_student_name("1"))
    # print("学生张三的ID:" + get_student_id("张三"))  
    # print("班级内课程:" + get_class_courses())
    # print("课程ID为201的单元:" + get_course_units("201"))
    # print("单元ID为30001的活动:" + get_unit_activities("30001"))
    # print("最近一次活动的活动ID:" + get_latest_activity_id())
    # print("活动ID为1001的学生成绩:" + get_activity_scores("1001"))
    # print("ID为2的学生参加的所有活动:" + get_student_activities("2"))

    # 存储示例问题的数组
    example_questions = [
        "最近一次活动的参与人数",
        "哪个学生没参加最近一次活动",
        "哪个学生没参加1003这个活动",
        "活动1001的学生成绩情况",
        "班级内有哪些学生",
        "全班同学的语文成绩排名",
        "张三的总成绩",
        "张三的总成绩和排名情况",
        "哪个学生的成绩进步最大"
    ]

    # 打印所有示例问题
    print("\n可以尝试以下示例问题：")
    for i, q in enumerate(example_questions, 1):
        print(f"{i}. {q}")
    print()

    # 获取用户输入
    user_input = input('请输入问题编号(1-9)或直接输入完整问题：')
    
    # 尝试将输入转换为数字
    try:
        question_index = int(user_input) - 1  # 转换为0基数的索引
        if 0 <= question_index < len(example_questions):
            question = example_questions[question_index]
        else:
            question = user_input
    except ValueError:
        question = user_input

    print(f"\n您的问题是：{question}\n")
    ask_question(question)
