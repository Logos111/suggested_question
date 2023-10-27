import sys
import pandas as pd
import json
import os
import time
from question_search import (
    get_new_pull_questions,
    get_normal_question_match,
    get_action_question,
    read_json,
    get_context_question,
)


def get_suggested_questions(
    convert_text: str = "",
    user_info: dict = {},
    intention_recognition: dict = {},
):
    if user_info.get("number"):
        number = user_info.get("number")
    else:
        number = 20
    intention_1 = intention_recognition.get("intention_1")
    intention_2 = intention_recognition.get("intention_2")
    slot = intention_recognition.get("slot")
    question_list = []
    file_name1 = "question_template1.json"
    file_name2 = "question_template2.json"
    question_temp1 = read_json(file_name1)
    question_temp2 = read_json(file_name2)

    # 判断是否新会话
    if not convert_text:
        question_list = get_new_pull_questions(question_temp2, user_info, number)
    else:
        if not slot:
            slot = {"base": "1"}
        if intention_1 == "商品":
            question_list = get_context_question(question_temp1, slot, number)
        elif intention_1 == "内容":
            question_list = get_context_question(question_temp1, slot, number)
        elif intention_1 == "知识":
            question_list = get_context_question(question_temp1, slot, number)
        elif intention_1 == "活动" and intention_2:
            question_list = get_action_question(
                question_temp1, slot, intention_2, number
            )
        elif intention_1 == "售后":
            pass
        else:
            question_list = get_context_question(question_temp1, slot, number)

    return question_list


###
if __name__ == "__main__":
    convert_text = ""
    user_info = {
        "tags": 1,
        "act": 1,
        "gender": "男",
        "labels": [
            {"label_name": "近1年肌肤护理类偏好品牌", "label_value": "兰蔻"},
            {"label_name": "最近消费品牌", "label_value": "欧莱雅"},
            {"label_name": "近1年偏好category三级品类", "label_value": "面膜"},
            {"label_name": "近1年平均客单价", "label_value": "200"},
            {"label_name": "敏感肌人群", "label_value": "是"},
        ],
    }
    # intention_recognition = {}
    intention_recognition = {"slot": {"brand": ["欧莱雅", "lancom"], "product": "面膜"}}
    t1 = time.time()
    question_list = get_suggested_questions(
        convert_text=convert_text,
        user_info=user_info,
        intention_recognition=intention_recognition,
    )
    t2 = time.time()
    print(question_list)
    print(t2 - t1)
