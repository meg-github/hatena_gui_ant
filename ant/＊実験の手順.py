# -*- coding: utf-8 -*-
import streamlit as st
import sys
import csv
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pickle
# # 外部pyファイル
from PIL import Image

#-----------関数----------------
markdown = '''
## はじめに
実験に参加していただき、ありがとうございます。\n
以下に実験の手順が記されておりますので、よくお読みいただいた上で参加してください。

## 実験手順
今から、あるニュース記事とその記事につけられたコメントについての質問を行います。
以下の手順に従って提示される内容を把握し、質問への回答を行ってください。

1. サイドバーから「タスク1」タブを押して開いてください。タブを開くと実験対象となるニュース記事のタイトルが表示されます。タイトルを押して、ニュース記事の内容と、その記事につけられたコメントを確認してください。画面の見方の詳細については、「タスク画面の説明」の項目を参照してください。
2. 「質問回答」タブを開いて、表示される質問にそって回答してください。回答内容はタブを切り替えても一時的に保存されます。必要に応じて適宜タブを切り替え、タスクの内容を確認しながら回答してください。入力が完了しましたら、「次へ」ボタンを押してください。
3. 「タスク2」タブを開いて、1.と同様に表示されるニュース記事を確認し、「質問回答」タブから回答してください。
4. 回答が全て終わりましたら、質問回答フォームの最下部にある「送信」を押して終了してください。

質問では、ニュース記事の内容に加えて、あなたが賛同できるコメントとその投稿者についての質問があります。各記事のコメントの中から賛同できるコメントを1件決めておいてください。

'''
st.markdown(markdown)


st.subheader("タスク画面の説明")
st.write("タブ：「タスク1」「タスク2」を開くと、以下のような画面が表示されます。"
"画面の構成は以下のようになっています。")
st.image("https://raw.githubusercontent.com/meg-github/hatena_gui_ant/main/ant/fig_exp2.png", caption='画面構成',use_column_width="auto")
"①：ニュース記事のタイトルです。クリックすることで記事内容を確認することができます。"
"②：ニュース記事の本文です。記事内容をお読みいただいた上で質問に回答してください。"
"③：ニュース記事につけられたコメントの一覧です。コメントは10件ずつ表示されています。左下の「＜」「＞」ボタンで11件目以降のコメントを見ることができます。"


st.image("https://raw.githubusercontent.com/meg-github/hatena_gui_ant/main/ant/fig_exp3.png", caption='投稿者の過去コメント参照時',use_column_width="auto")

"コメントの左側にあるチェックボックスをチェックすると、コメントを投稿したユーザーが過去に投稿したコメントと、過去に投稿されたコメントの感情的な傾向を確認することができます(表示されるまで少し時間がかかります)。気になるコメントについて適宜確認し、質問回答の際の参考にしてください。"

st.header("注意事項")
"実験は2つのタスクから構成されています。必ず2つとも回答してください。"
"質問の入力後は必ず「送信」ボタンを押してください。"