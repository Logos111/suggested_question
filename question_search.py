import sys
import json
import random
import pymysql
import os
import sys
import logging

path = os.path.dirname(__file__)
sys.path.append(os.path.dirname(path))

from utils.MySQL import SqlConnect


def read_json(file_name):
    current_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_path)
    file_path_1 = os.path.join(current_directory, file_name)
    with open(file_path_1, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# 通过商品id查找商品信息
def search_goods_info(item_code):
    sql = SqlConnect(password="K8*Vi!6t&M^1L", host="localhost", database="demo")
    # cnx = pymysql.connect(
    #     user="root", password="K8*Vi!6t&M^1L", host="localhost", database="demo"
    # )
    # cursor = cnx.cursor()
    brand, category, effect = "", "", ""
    query = "select * from ITEM_INFO where id=" + item_code + " limit 1"
    # cursor.execute(query)
    # result = cursor.fetchall()
    result = sql.search(query)
    # 打印查询结果
    for row in result:
        brand = row[2]
        category = row[3]
        effect = random.choice(row[4].split("、"))
    goods_info = {"brand": brand, "category": category, "effect": effect}
    print(goods_info)
    # 关闭游标和数据库连接
    # cursor.close()
    # cnx.close()
    return goods_info


# 整理label的值和覆盖人数
def get_labels_list(labels, label_info):
    labels_list = []
    for label in labels:
        labelname = label["label_name"]
        labelvalue = label["label_value"]
        if labelname == "敏感肌人群":
            if labelvalue == "是":
                labelvalue = "敏感肌"
            else:
                continue
        if labelname in label_info:
            # 保存 标签类型，标签值，覆盖人数{"brand", "oulaiya", 200000}
            element = [
                label_info[labelname][0],
                labelvalue,
                label_info[labelname][1],
            ]
            labels_list.append(element)
    return labels_list


# 基数为10万在0.2-0.5之间为最合适
def is_suitable(a, b):
    def cmp(x):
        if x <= 20000000:
            y = 1
        elif x > 20000000 and x <= 50000000:
            y = 3
        else:
            y = 2
        return y

    if cmp(a) != cmp(b):
        return cmp(a) > cmp(b)
    else:
        return a > b


# 用于label值的添加，如果
def slot_add(slot1: dict, slot2: dict) -> dict:
    for key, value in slot1.items():
        if key in list(slot2.keys()):
            if isinstance(slot2[key], list):
                if isinstance(value, list):
                    slot2[key].extend(value)
                else:
                    slot2[key].append(value)
            else:
                if isinstance(value, list):
                    value.append(slot2[key])
                    slot2[key] = value
                else:
                    slot2[key] = list(slot2[key])
                    slot2[key].append(value)
        else:
            slot2.update({key: value})
    return slot2


# 将偏好中所有字段和标签填进字典
def add_all_label(label_list) -> dict:
    tempdict = {}
    for element in label_list:
        if element[0] not in list(tempdict.keys()):
            tempdict.update({element[0]: element[1]})
        else:
            newlist = [tempdict[element[0]]]
            newlist.append(element[1])
            tempdict[element[0]] = newlist
    return tempdict


# 从偏好中选择最合适的字段和标签
def choose_best_label(label_list) -> dict:
    tempdict = {}
    res = {}
    for element in label_list:
        if element[0] not in list(tempdict.keys()):
            tempdict.update({element[0]: [element[1], element[2]]})
        else:
            if is_suitable(element[2], tempdict[element[0]][1]):
                tempdict.update({element[0]: [element[1], element[2]]})
    for key, value in tempdict.items():
        res.update({key: value[0]})
    return res


def slot_fill(user_info):
    slot = {}
    slot["base"] = "1"
    # 性别字段
    if user_info.get("gender"):
        gender = user_info.get("gender")
        slot.update({"gender": gender})
        slot.update({"gender:" + gender: "1"})
    # 地点或门店字段
    if user_info.get("city"):
        position = user_info.get("city")
        slot.update({"position": position})
    # 会员卡字段
    if user_info.get("member_card_type"):
        member_card_type = user_info.get("member_card_type")
        if member_card_type != "非会员":
            slot.update({"member_card_type": member_card_type})
        else:
            slot.update({"member_card_type:" + member_card_type: "1"})
    # 年龄字段
    if user_info.get("age"):
        age = user_info.get("age")
        if age <= 18:
            slot.update({"age:少儿": "1"})
        elif age > 18 and age <= 35:
            slot.update({"age:青年": "1"})
        elif age > 35 and age <= 55:
            slot.update({"age:中年": "1"})
        elif age > 55:
            slot.update({"age:老年": "1"})
    # 用户标签字段
    if user_info.get("labels"):
        labels = user_info.get("labels")
        label_info = read_json("label.json")
        labels_list = get_labels_list(labels, label_info)
        print("labels_list:" + str(labels_list))
        label_dict = add_all_label(labels_list)
        print("label_dict" + str(label_dict))
        slot = slot_add(label_dict, slot)
    # 商品id字段
    if user_info.get("itemcode"):
        item_code = user_info.get("itemcode")
        goods_info = search_goods_info(item_code)
        slot.update(goods_info)
    return slot


# 商详页用户建议问题生成
"""
def get_new_detail_question(user_info: dict = {}, slot: dict = {}, question_temp=[]):
    tags = user_info["tags"]
    act = user_info["act"]
    # 获得商品信息
    # goods_info=get_goods_info(goods_id)
    # slot=slot_fill(tags,act,goods_info)
    question_list = get_normal_question_match(question_temp, slot, 4)
    return question_list
"""


# 排序方法
def sort_method(question_store, question_num):
    question_store = sorted(
        question_store, key=lambda x: list(x.values())[0], reverse=True
    )
    question_list = question_store[:question_num]
    question_list = [i["question"] for i in question_list]
    return question_list


# 概率选择方法
# question_store[{question:[""],priority:1},...]
def probabilities_choose_method(question_store, question_num):
    print(len(question_store))
    probabilities = [1 / 2 * i["priority"] ** 2 for i in question_store]
    probabilities = [i / sum(probabilities) for i in probabilities]
    print(probabilities)
    import numpy as np

    question_list = []
    while len(question_list) != question_num:
        question_set = np.random.choice(question_store, 1, True, probabilities)
        question = random.sample(list(question_set)[0]["question"], 1)[0]
        if question not in question_list:
            question_list.append(question)

    return question_list


# 新会话用户建议问题生成
def get_new_pull_questions(question_temp, user_info, question_num):
    slot = slot_fill(user_info)
    question_list = get_normal_question_match(
        question_temp, slot, question_num, probabilities_choose_method
    )

    return question_list


# 对话中建议问题生成
def get_context_question(question_temp, slot, question_num):
    question_list = get_normal_question_match(
        question_temp, slot, question_num, probabilities_choose_method
    )
    return question_list


# 活动建议问题
def get_action_question(question_temp, slot, intention_2, question_num):
    question_list = []
    if intention_2:
        slot["intent2:" + intention_2] = "1"
    question_list = get_normal_question_match(
        question_temp, slot, question_num, sort_method
    )
    return question_list


# 生成模板列表[["template"]], 当value是list时，一个模板列表会映射成多个模板列表
def question_generate(q_template, key, value) -> list:
    q_set = []
    if type(value) is str:
        q_set.extend(
            [question.replace("{" + key + "}", value) for question in q_template]
        )
    if type(value) is list:
        for val in value:
            q_set.extend(
                [question.replace("{" + key + "}", val) for question in q_template]
            )
    return q_set


# 生成问题集，当value有多个值时，映射会发散，每个组合会构成一个问题列表，所有列表构成一个问题集
def get_question_set(q_template, slot, pslot):
    question_template_list = [q_template]
    for key in pslot:
        value = slot[key]
        question_template_list = [
            question_generate(question_template, key, value)
            for question_template in question_template_list
        ]
    return question_template_list


def decouple_list(lst) -> list:
    decoupled_lst = []
    for item in lst:
        if isinstance(item, list):
            decoupled_lst.extend(item)
        else:
            decoupled_lst.append(item)
    return decoupled_lst


# 问题模板匹配
def get_normal_question_match(question_temp, slot, question_num, priority_method):
    keyslot = list(slot.keys())
    question_store = []
    question_list = []
    print(keyslot)
    for i in question_temp:
        pslot = i["pslot"].split(",")
        priority = len(pslot)
        if set(keyslot).issuperset(pslot):
            q_template = i["query"]
            question_set = []
            question_set = get_question_set(q_template, slot, pslot)
            for question in question_set:
                question_store.append({"question": question, "priority": priority})

    if len(decouple_list([i["question"] for i in question_store])) >= question_num:
        question_list = priority_method(question_store, question_num)
    else:
        question_list = [i["question"] for i in question_store]
        question_list = random.shuffle(decouple_list(question_list))
    return question_list
