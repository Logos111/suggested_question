from turtle import onclick
import streamlit as st
import json
import os
import pandas as pd
import numpy as np
import copy


df = pd.read_json("streamlit_data.json")
df2 = pd.read_json("question_template2.json")

st.markdown("Streamlit Demo")

# 设置网页标题
st.title("data1")


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


st.dataframe(data=st.session_state.data)


def add_query(newquery, line):
    # line = st.session_state.get("line")
    # newquery = copy.deepcopy(st.session_state.get("newquery"))
    st.session_state.data["query"][line].append(newquery)


def delete_query(newquery):
    st.session_state.data["query"][st.session_state.del_line].remove(newquery)


# 增加问题
st.button("addquery", on_click=click_add_open)
if st.session_state.added == True:
    newquery = st.text_input("addquery")
    line = st.number_input(
        "insert_line", min_value=0, max_value=len(df), value=0, step=1
    )
    st.button("comfirm", on_click=add_query, args=[newquery, line])
    st.button("close", on_click=click_add_open)

# 减少问题按钮及逻辑
st.button("deletequery", on_click=click_del_open)
if st.session_state.deled == True:
    st.session_state.del_line = st.number_input(
        "insert_line", min_value=0, max_value=len(df), value=0, step=1
    )
    if st.session_state.get("del_line"):
        option = st.selectbox(
            "Choose delete query",
            st.session_state.data["query"][st.session_state.del_line],
        )

        st.button("comfirm", on_click=delete_query, args=[option])
    st.button("close", on_click=click_del_close)


# 展示一级标题
st.title("data2")

# st.json(data2)
st.dataframe(data=df2)

if st.button("save"):
    jsondata = st.session_state.data.to_json(orient="records", force_ascii=False)
    with open("streamlit_data.json", "w", encoding="utf-8") as f:
        f.write(jsondata)
    st.write("already save")
