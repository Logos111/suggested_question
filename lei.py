import sys
import json
import random
import pymysql
import os
import sys
import logging


def read_json(file_name):
    current_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_path)
    file_path_1 = os.path.join(current_directory, file_name)
    with open(file_path_1, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


class Suggestion_Template:
    def __init__(self, template: dict):
        self.query_list = template["query"]
        self.pslot = template["pslot"].split(",")
        self.private = len(self.pslot)

    def instantiation(self, s_dict: dict):
        q_set = []
        for query in self.query_list:
            question = query
            for i in range(self.private):
                for key, value in s_dict.items():
                    question = question.replace("{" + key + "}", value)
            q_set.append(question)

        self.query_list = q_set
        return q_set

    def q_len(self):
        return len(self.query_list)


def get_exslot(pslot, slot: dict):
    res_dict = {
        key: slot[key] if isinstance(slot[key], list) else [slot[key]] for key in pslot
    }
    import itertools

    keys = res_dict.keys()
    values = res_dict.values()

    # 使用itertools的product函数计算笛卡尔积
    cartesian_product = list(itertools.product(*values))

    # 将结果转换为列表的字典
    result = [
        {key: value for key, value in zip(keys, product)}
        for product in cartesian_product
    ]

    print(result)
    return result


if __name__ == "__main__":
    q_template = read_json("question_template1.json")
    slot = {"brand": ["兰蔻", "欧莱雅"], "product": "面膜"}
    keyslot = list(slot.keys())
    question_list = []

    for i in q_template:
        pslot = i["pslot"].split(",")
        if set(keyslot).issuperset(pslot):
            exslots = get_exslot(pslot, slot)
            for exslot in exslots:
                Suggestion_set = Suggestion_Template(i)
                Suggestion_set.instantiation(exslot)
                question_list.append(Suggestion_set)

    print(question_list)
    for i in question_list:
        print(i.query_list[:])
