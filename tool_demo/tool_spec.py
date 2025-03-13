# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具 获取班级学生ID的列表
    {
        "type": "function",
        "function": {
            "name": "get_class_students",
            "description": "获取班级学生ID的列表，当你想知道班级内有哪些学生时非常有用。",
            "parameters": {}  # 因为获取当前班级无需输入参数，因此parameters为空字典
        }
    },  
    # 工具 根据学生ID获取学生姓名
    {
        "type": "function",
        "function": {
            "name": "get_student_name",
            "description": "根据学生ID获取学生姓名，当你想查询学生姓名时非常有用。",
            "parameters": {  # 查询学生姓名时需要提供学生ID，因此参数设置为 student_id
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "string",
                        "description": "学生的唯一ID。"
                    }
                }
            },
            "required": [
                "student_id"
            ]
        }
    }, 
    # 工具 根据学生姓名获取学生ID
    {
        "type": "function",
        "function": {
            "name": "get_student_id",
            "description": "根据学生姓名获取学生ID，当用户问题中包含学生姓名时可能要根据学生姓名查询学生ID。",
            "parameters": {  # 查询学生ID时需要提供学生姓名，因此参数设置为 student_name
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "学生姓名。"
                    }
                }
            },
            "required": [
                "student_name"
            ]
        }
    }, 
    # 工具 获取班级课程ID的列表
    {
        "type": "function",
        "function": {
            "name": "get_class_courses",
            "description": "获取班级课程ID的列表，当你想知道班级内有哪些课程时非常有用。",
            "parameters": {}  # 因为获取当前班级无需输入参数，因此parameters为空字典
        }
    },  
    # 工具 根据课程ID获取单元ID的列表
    {
        "type": "function",
        "function": {
            "name": "get_course_units",
            "description": "根据课程ID获取单元ID的列表，当你想查询班级内有哪些单元时非常有用。",
            "parameters": {  # 查询课程下单元时需要提供课程ID，因此参数设置为 course_id
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "string",
                        "description": "课程的唯一ID。"
                    }
                }
            },
            "required": [
                "course_id"
            ]
        }
    }, 
    # 工具 根据单元ID获取活动ID的列表
    {
        "type": "function",
        "function": {
            "name": "get_unit_activities",
            "description": "根据单元ID获取活动ID的列表，当你想查询单元下有哪些活动时非常有用。",
            "parameters": {  # 查询单元下活动时需要提供单元ID，因此参数设置为 unit_id
                "type": "object",
                "properties": {
                    "unit_id": {
                        "type": "string",
                        "description": "单元的唯一ID。"
                    }
                }
            },
            "required": [
                "unit_id"
            ]
        }
    }, 
    # 工具 获取最近一次活动的活动ID
    {
        "type": "function",
        "function": {
            "name": "get_latest_activity_id",
            "description": "获取最近一次活动的活动ID，当你想知道班级内最后一次活动的相关信息时非常有用。",
            "parameters": {}  # 因为获取最近一次活动的活动ID无需输入参数，因此parameters为空字典
        }
    },  

    # 工具 根据活动ID获取所有学生的活动成绩
    {
        "type": "function",
        "function": {
            "name": "get_activity_scores",
            "description": "根据活动ID获取所有学生的活动成绩，当你想查询每个活动的参与学生及学生成绩时非常有用。",
            "parameters": {  # 查询某个活动的参与学生和他们的成绩时需要提供活动ID，因此参数设置为activity_id
                "type": "object",
                "properties": {
                    "activity_id": {
                        "type": "string",
                        "description": "活动ID。"
                    }
                }
            },
            "required": [
                "activity_id"
            ]
        }
    },
    # 工具 根据学生ID，快速查询学生参加的所有活动的ID列表
    {
        "type": "function",
        "function": {
            "name": "get_student_activities",
            "description": "根据学生ID，快速查询学生参加的所有活动的ID列表。",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "string",
                        "description": "学生ID。"
                    }
                }
            },
            "required": [
                "student_id"
            ]
        }
    }
]
