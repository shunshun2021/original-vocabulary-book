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

page = st.sidebar.selectbox('Choose your page', ['registration', 'list','test'])


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

def build_prompt_test(word,content, n_chars=300):
    return f"""英単語 {word} の日本語訳として {content} は概ね正しいですか？
    正しければTrueのみを、そうでなければFalseのみを出力してください.
    """

def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost

def print_word(record):
    st.subheader('・' + record["word"])
    st.write('訳：'+record["japanese"])
    st.write('例文：'+record["sample_sentence"])
    st.write('('+record["sample_sentence_in_japanese"]+")")
    st.write('語の由来：'+record["origin"])


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
            #st.write(data)
            if res.status_code == 200:
                st.success('メモ登録完了')
            else:
                st.warning('出力に不具合がありました\nもう一度登録してください.')


    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


elif page == 'list':

    
    st.title('単語リスト')
    res = requests.get('http://127.0.0.1:8000/memos')
    records = res.json()
    elements = list(records)
    word_num = len(elements)


    # 現在のページ
    if "current_index" not in st.session_state:
        st.session_state["current_index"]=0

    # 1ページ当たりに表示する単語数
    if "word_per_page" not in st.session_state:
        st.session_state["word_per_page"]=1

    # プルダウンサイドバーに表示させる
    word_per_page = st.sidebar.selectbox(
        '1ページあたりの単語数はここで変更',
        (1,2,4,8))
    
    # 1ページあたりの単語数に変更があった場合
    if(word_per_page!=st.session_state["word_per_page"]):
        st.session_state["word_per_page"]=min(word_per_page,word_num)
        # ページindex は 0 に戻るようにする (後で元の単語が表示されていたページを表示できるようにするかも)
        st.session_state["current_index"] = 0
        current_index=0

    page_num = max(0,word_num-1)//word_per_page

    

    ### 以下, ページ表示に関する実装 ###
    # 現在の要素のインデックスを格納する変数
    current_index = st.session_state.get("current_index", 0)
    
    col = st.columns(3)
    prev=col[0].button('Previous')
    next=col[2].button('Next')

    # 前の要素に移動するボタン
    if prev and current_index > 0:
        current_index -= 1
        st.session_state["current_index"] = current_index
    # 次の要素に移動するボタン
    if next and current_index < page_num :
        current_index += 1
        st.session_state["current_index"] = current_index

    # 現在の位置を表示
    med = col[1].write("{:3d} / {:3d}".format(st.session_state.current_index+1,page_num+1))
    
    # 現在の要素を表示
    start=current_index*word_per_page
    for i in range(start, start+word_per_page):
        if(i<word_num):
            print_word(records[i])
        #print_word(records[current_index])


    # セッション状態を更新
    st.session_state["current_index"] = current_index


elif page=="test":
 
    init_messages()
    llm=select_model()

    res = requests.get('http://127.0.0.1:8000/memos')
    records = res.json()
    word=records[0]["word"]    

    st.title("単語理解度テスト")

    with st.form(key='registration'):
        content: str = st.text_input(f'{word} の日本語訳は?', max_chars=100)
        data = {
                'word': content
        }
        submit_button = st.form_submit_button(label='確認')

        if submit_button:
            prompt = build_prompt_test(word,content)
            st.session_state.messages.append(HumanMessage(content=prompt))
            with st.spinner("ChatGPT is judging ..."):
                answer, cost = get_answer(llm, st.session_state.messages)
            st.session_state.costs.append(cost)

            if answer:
                if answer=="True":
                    # ToDo
                    # 正解時
                    # 正答した英単語の 正解回数, 正解日時, 定着率 を更新する.
                    st.success("正解です!")
                else:
                    # ToDo
                    # 不正解時
                    # 単語を覚えるための情報(例文など)を表示する.
                    st.warning("不正解です")

        
    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
   