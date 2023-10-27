from turtle import onclick
import streamlit as st
import json
import os
import pandas as pd
import numpy as np

def read_json(file_name):
    current_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_path)
    file_path_1 = os.path.join(current_directory, file_name)
    with open(file_path_1, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


df = pd.read_json("streamlit_data.json")
df2 = pd.read_json("question_template2.json")
# data1 = read_json("question_template1.json")
# data2 = read_json("question_template_2")

st.markdown("Streamlit Demo")

# 设置网页标题
st.title("data1")



#加减开关
def click_add_open():
    st.session_state.added = True
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
#会话状态数据
if "data" not in st.session_state:
    st.session_state.data=df


st.dataframe(data=st.session_state.data)

def addq(df, line, newquery):
    df["query"][line].append(newquery)
    st.session_state.data=df

st.button("addquery", on_click=click_add_open)
if st.session_state.added == True:
    st.session_state.newquery = st.text_input("addquery")
    st.session_state.line = st.number_input(
        "insert_line", min_value=0, max_value=len(df), value=0, step=1
    )
    st.button("comfirm", on_click=addq(df, st.session_state.line, st.session_state.newquery))
    st.button("close", on_click=click_add_close)


st.button("deletequery", on_click=click_del_open)
if st.session_state.deled==True:
    # line = st.number_input("insert_line", min_value=0, max_value=len(df), value=0, step=1)
    option = st.selectbox("Choose delete query",np.ndarray(df["query"][1]))
    st.button("comfirm", on_click=click_del_close)
    st.button("close", on_click=click_del_close)




# 展示一级标题
st.title("data2")

# st.json(data2)
st.dataframe(data=df2)

if st.button("save"):
    jsondata = df.to_json(orient="records", force_ascii=False)
    with open("streamlit_data.json", "w", encoding="utf-8") as f:
        f.write(jsondata)
    st.write("already save")
