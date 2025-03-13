from lms_data import student_name_mapping, class_course_mapping, course_unit_mapping, unit_activity_mapping, activity_student_score_mapping
import json

# 获取班级学生ID的列表
def get_class_students():
    # 从student_name_mapping中获取学生ID列表
    student_ids = list(student_name_mapping.keys())
    return json.dumps({"student_ids": student_ids})

# 根据学生ID获取学生姓名
def get_student_name(student_id):
    return student_name_mapping.get(student_id, "未知姓名")

# 根据学生姓名获取学生ID
def get_student_id(student_name):
    for k, v in student_name_mapping.items():
        if v == student_name:
            return k
    return "未知ID"


# 获取班级课程ID的列表
def get_class_courses():
    # 从class_course_mapping中获取班级下课程ID的列表
    course_ids = list(class_course_mapping.keys())
    return json.dumps({"course_ids": course_ids})

# 根据课程ID获取单元ID的列表
def get_course_units(course_id):
    # 从course_unit_mapping中获取课程下单元ID的列表
    units = course_unit_mapping.get(course_id, "未知单元")
    return json.dumps({"units": units})

# 根据单元ID获取活动ID的列表
def get_unit_activities(unit_id):
    # 从unit_activity_mapping中获取单元下活动ID的列表
    activities = unit_activity_mapping.get(unit_id, "未知活动")
    return json.dumps({"activities": activities})

# 获取最近一次活动的活动ID
def get_latest_activity_id():
    # 获取最近一次活动的活动ID
    latest_activity_id = "1012"
    return latest_activity_id

# 根据活动ID获取所有学生的活动成绩
def get_activity_scores(activity_id):
    # 从 activity_student_score_mapping 中获取所有学生的活动成绩
    if activity_id in activity_student_score_mapping:
        activity_scores = activity_student_score_mapping[activity_id]
    else:
        activity_scores = {}
        
    return json.dumps(activity_scores)  # 返回JSON对象


# 根据学生ID，快速查询学生参加的所有活动
def get_student_activities(student_id):
    student_id = str(student_id)
    activities = []
    for activity_id, score in activity_student_score_mapping.items():
        if student_id in score:
            activities.append(activity_id)
    return json.dumps({"activities": activities})