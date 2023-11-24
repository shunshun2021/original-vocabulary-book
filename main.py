import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.callbacks import get_openai_callback

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import streamlit as st
import requests
import json

page = st.sidebar.selectbox('Choose your page', ['registration', 'list'])


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []

def select_model():
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-4"

    return ChatOpenAI(temperature=0, model_name=model_name)

def build_prompt(content, n_chars=300):
    return f"""英単語「{content}」を覚えるために以下の4つの情報をこの順にJSONで出力してください.
    {content}の日本語訳、{content}を使った簡単な英語の例文、その例文の日本語訳、単語の由来.
    以下の形式でデータを出力してください.
    "japanese":<japanese>,
    "sample_sentence":<sample_sentence>,
    "sample_senetnce_in_japanese":<sample_japanese>,
    "origin":<origin(日本語)>
    """


def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost


### 登録ページ ###
if page == 'registration':
    init_messages()
    llm=select_model()

    st.title('新しい英単語を覚えよう！🤗')
    with st.form(key='registration'):
        content: str = st.text_input('覚えたい英単語を入力してください', max_chars=100)
        data = {
                #'content': content
                'word': content
        }
        example_sentence = st.checkbox(label="例文を作成し、語源の説明を追加する")        
        submit_button = st.form_submit_button(label='登録')

        if submit_button:
            if example_sentence:
                # 例文、その日本語訳、語源の説明、を ChatGPT API を利用して生成する
                prompt = build_prompt(content)
                st.session_state.messages.append(HumanMessage(content=prompt))
                with st.spinner("ChatGPT is typing ..."):
                    answer, cost = get_answer(llm, st.session_state.messages)
                st.session_state.costs.append(cost)

                if answer:
                    st.markdown("## 以下の内容で登録しました.")
                    outputs = answer.split(",")
                    for output in outputs:
                        output_1, output_2 = output.split(":")
                        output_1_2 = output_1.split("\"")[1]
                        output_2_2 = output_2.split("\"")[1]
                        st.write(output_2_2)
                        data[output_1_2]=output_2_2
                

            url = 'http://127.0.0.1:8000/memos'
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            st.write(data)
            if res.status_code == 200:
                st.success('メモ登録完了')


    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


elif page == 'list':
    st.title('単語一覧画面')
    res = requests.get('http://127.0.0.1:8000/memos')
    records = res.json()
    for record in records:
        #st.subheader('・' + record.get('sample_sentence'))
        st.subheader('・' + record["word"])
        st.write('訳：'+record["japanese"])
        st.write('例文：'+record["sample_sentence"])
        st.write('('+record["sample_sentence_in_japanese"]+")")
        st.write('語の由来：'+record["origin"])