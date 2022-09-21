# -*- coding: utf-8 -*-
import streamlit as st
import sys
import csv
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pickle
# # 外部pyファイル
sys.path.append('../functions/')
import scrape_user_comment
import analyze_user
import analyze_text_janome
import collections

# --------functions---------

def func_user_analysis(username):
	scrape_user_comment.scrape(username,3)#コメントのスクレイピング
	comments_user = analyze_user.analyze_usr(username)#感情値の算出
	df_user = pd.read_table('../result/'+username, names=["id","url","title","comment"],usecols=["title","comment"])
	# 各列の幅を'px'や'em'単位で微調整する
	gridoptions = func_aggrids_user(df_user)
	table = AgGrid(df_user,	gridOptions=gridoptions,fit_columns_on_grid_load=True)

	st.write('感情語の割合: '+str(comments_user[0])+' ポジティブな語の割合: '+str(comments_user[1])+' ネガティブな語の割合: '+str(comments_user[2]))
	# st.write("ワードランキング:"+str(comments_user[3]))


def func_dataframe(url,opt):#感情割合の算出（描画含む）とユーザ，コメントリストの構築
	result_bookmark = analyze_bookmark_janome.analyze_b(url,opt)
	print(result_bookmark)
	result_abst = '感情語の割合: '+str(result_bookmark[0])+' ポジティブな語の割合: '+str(result_bookmark[1])+' ネガティブな語の割合: '+str(result_bookmark[2])
	df_baseline = pd.DataFrame({
		"User":result_bookmark[3].keys(),
		"Comment":result_bookmark[3].values()
		})
	st.write(result_abst)
	return(df_baseline)


def func_aggrids_bookmarks(df):   # st_aggridを使ってデータの設定をする
	data_view = GridOptionsBuilder.from_dataframe(df)
	data_view.configure_pagination(enabled=True)
	data_view.configure_default_column(editable=False,groupable=True,autoHeight=True, wrapText=True)
	data_view.configure_selection(selection_mode='single',use_checkbox=True)
	gridoptions = data_view.build()
	return(gridoptions)

def func_aggrids_user(df):
	data_view = GridOptionsBuilder.from_dataframe(df)
	data_view.configure_pagination(enabled=True)
	data_view.configure_default_column(editable=False,groupable=True,autoHeight=True, wrapText=True)
	gridoptions = data_view.build()
	return(gridoptions)

# -----------------


kijilist = pd.read_csv('../data_kiji/kijilist.csv', header=0)
sentdata = pd.read_csv('../data_kiji/list_sentdata.csv', header=0,dtype=str)
target_kiji = kijilist[kijilist['uri']=="https://gigazine.net/news/20220901-midjourney-win-fine-arts-competition/"]
target_sentdata = sentdata[sentdata['title'].isin(target_kiji['title'])]
title = target_kiji["title"].tolist()[0]


with st.expander(title):
	sent = target_sentdata[target_sentdata["title"] == title]
	st.write(target_kiji["content"].tolist()[0])
	# sentidata_kiji = analyze_text_janome.analyze(line.content)
	st.text('感情語の割合: '+sent.sent_total.values+
		' ポジティブな語の割合: '+sent.sent_p.values+
		' ネガティブな語の割合: '+sent.sent_n.values)
	with open('../data_kiji/'+str(title), "rb") as comments:
		commentlist = pickle.load(comments)
		# for key,value in zip(commentlist.keys(),commentlist.values()):
			# st.write(key+":"+value)
		df_commentlist = pd.DataFrame({
			"User":commentlist.keys(),
			"Comment":commentlist.values()
		})
		# sentidata_comment = analyze_text_janome.analyze(list(df_commentlist["Comment"]))
		# st.write('感情語の割合: '+str(sentidata_comment[0])+' ポジティブな語の割合: '+str(sentidata_comment[1])+' ネガティブな語の割合: '+str(sentidata_comment[2]))

		gridoptions = func_aggrids_bookmarks(df_commentlist)
		table = AgGrid(df_commentlist,	gridOptions=gridoptions,
										fit_columns_on_grid_load=True,
										data_return_mode=DataReturnMode.AS_INPUT,
										update_mode=GridUpdateMode.SELECTION_CHANGED)


if table:
	selected_rows = table["selected_rows"]
	if selected_rows:
		st.write("ユーザー名:"+table["selected_rows"][0]["User"]+"のコメントリスト")
		selected_user = str(selected_rows[0]["User"])
		func_user_analysis(selected_user)