from turtle import onclick
import streamlit as st
import json
import os
import pandas as pd
import numpy as np
import copy


df = pd.read_json("streamlit_data.json")
df2 = pd.read_json("question_template2.json")


# 加减开关
def click_add_open():
    st.session_state.added = not st.session_state.added


def click_add_close():
    st.session_state.added = False


def click_del_open():
    st.session_state.deled = True


def click_del_close():
    st.session_state.deled = False


if "added" not in st.session_state:
    st.session_state.added = False
if "deled" not in st.session_state:
    st.session_state.deled = False
# 会话状态数据
if "data" not in st.session_state:
    st.session_state.data = df


st.markdown("Streamlit Demo")
# 设置网页标题
st.title("对话过程建议问题模板")
st.markdown("这个数据用于匹配对话过程时的的建议问题")
st.dataframe(data=st.session_state.data)


def add_query(newquery, line):
    # line = st.session_state.get("line")
    # newquery = copy.deepcopy(st.session_state.get("newquery"))
    st.session_state.data["query"][line].append(newquery)


def delete_query(newquery):
    st.session_state.data["query"][st.session_state.del_line].remove(newquery)


# 增加问题
st.button("添加问题", on_click=click_add_open)
if st.session_state.added == True:
    st.markdown("输入问题模板和行数，将文本插入到问题集")
    newquery = st.text_input("请按照模板和槽位格式添加问题模板")
    line = st.number_input("输入行数", min_value=0, max_value=len(df), value=0, step=1)
    st.button("确认", on_click=add_query, args=[newquery, line])
    st.button("关闭", on_click=click_add_open)

# 减少问题按钮及逻辑
st.button("删除问题", on_click=click_del_open)
if st.session_state.deled == True:
    st.session_state.del_line = st.number_input(
        "输入行数", min_value=0, max_value=len(df), value=0, step=1
    )
    if st.session_state.get("del_line"):
        option = st.selectbox(
            "请选择想删除的问题",
            st.session_state.data["query"][st.session_state.del_line],
        )

        st.button("确认", on_click=delete_query, args=[option])
    st.button("关闭", on_click=click_del_close)


# 展示一级标题
st.title("新会话建议问题模板")
st.markdown("这个数据用于匹配新会话创建时的的建议问题")


# 加减开关
def click_add_open2():
    st.session_state.added2 = not st.session_state.added2


def click_add_close2():
    st.session_state.added2 = False


def click_del_open2():
    st.session_state.deled2 = True


def click_del_close2():
    st.session_state.deled2 = False


if "added2" not in st.session_state:
    st.session_state.added2 = False
if "deled2" not in st.session_state:
    st.session_state.deled2 = False
# 会话状态数据
if "data2" not in st.session_state:
    st.session_state.data2 = df2

st.dataframe(data=st.session_state.data2)


def add_query2(newquery, line):
    # line = st.session_state.get("line")
    # newquery = copy.deepcopy(st.session_state.get("newquery"))
    st.session_state.data2["query"][line].append(newquery)


def delete_query2(newquery):
    st.session_state.data2["query"][st.session_state.del_line2].remove(newquery)


# 增加问题
st.button("添加问题", on_click=click_add_open2)
if st.session_state.added2 == True:
    st.markdown("输入问题模板和行数，将文本插入到问题集")
    newquery2 = st.text_input("请按照模板和槽位格式添加问题模板")
    line2 = st.number_input("输入行数", min_value=0, max_value=len(df2), value=0, step=1)
    st.button("确认", on_click=add_query2, args=[newquery2, line2])
    st.button("关闭", on_click=click_add_open2)

# 减少问题按钮及逻辑
st.button("删除问题", on_click=click_del_open2)
if st.session_state.deled2 == True:
    st.session_state.del_line2 = st.number_input(
        "输入行数", min_value=0, max_value=len(df2), value=0, step=1
    )
    if st.session_state.get("del_line2"):
        option2 = st.selectbox(
            "请选择想删除的问题",
            st.session_state.data2["query"][st.session_state.del_line2],
        )

        st.button("确认", on_click=delete_query2, args=[option2])
    st.button("关闭", on_click=click_del_close2)


if st.button("保存"):
    jsondata1 = st.session_state.data.to_json(orient="records", force_ascii=False)
    jsondata2 = st.session_state.data2.to_json(orient="records", force_ascii=False)
    with open("streamlit_data1.json", "w", encoding="utf-8") as f:
        f.write(jsondata1)
    with open("streamlit_data2.json", "w", encoding="utf-8") as f:
        f.write(jsondata2)
    st.write("already save")
