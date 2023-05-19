from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from .models import name

import pandas as pd
import numpy as np
from pathlib import Path

def index(request):
    return render(request, 'musical/index.html')

def ver1(request):
    return render(request, 'musical/ver1.html')

def ver2(request):
    return render(request, 'musical/ver2.html')

def post(request):

    if request.method == 'POST':
        username = request.POST.get('name')
        data={'user_name' : username}

    return render(request, 'musical/index_name.html', data)

# def post2(request):

#     if request.method == 'GET':
#         gender = request.GET.get('gender')
#         age = request.GET.get('old')
#         keyword = request.GET.getlist('keyword')
#         data={'gender' : gender,
#               'age' : age,
#               'keyword' : keyword}

#     return render(request, 'musical/results.html', data)

def calculate(df, gender, age, keyword, n=3):
    
    dic = {}
    
    if gender == '여성':
        idx = df.sort_values('female', ascending = False).index
    else:
        idx = df.sort_values('male', ascending = False).index
    for i in range(len(df)):
        dic[idx[i]] = (len(df)-1-i)/(len(df)-1)
        
    if age == '10대':
        idx = df.sort_values('10s', ascending = False).index
    elif age == '20대':
        idx = df.sort_values('20s', ascending = False).index
    elif age == '30대':
        idx = df.sort_values('30s', ascending = False).index
    elif age == '40대':
        idx = df.sort_values('40s', ascending = False).index
    else:
        idx = df.sort_values('50s', ascending = False).index
    
    for j in range(len(df)):
        dic[idx[j]] += (len(df)-1-j)/(len(df)-1)
        
    df_mini = pd.DataFrame(columns = df.columns[-30:-1], data=np.zeros(len(df)*29).reshape(len(df), 29))
    for x in keyword:
        df_mini[x] = 1
        
    df_copy = df.copy()
    df_copy['score_keyword'] = ((df_mini * df.iloc[:, -30:-1]).sum(axis=1))
    idx = df_copy.sort_values('score_keyword', ascending=False).index
    
    for k in range(len(df)):
        dic[idx[k]] += (len(df)-1-k)/(len(df)-1)
        
    sort_dic = sorted(dic, key=dic.get, reverse=True)
    result_df = df.iloc[sort_dic[:n]]
    
    return result_df

def musical_recommend(request):
    THIS_FOLDER = Path(__file__).parent.resolve()
    df = pd.read_csv(THIS_FOLDER/'전체뮤지컬_인코딩_imageurl추가.csv')
    
    if request.method == 'GET':
        gender = request.GET.get('gender')
        age = request.GET.get('old')
        keyword = request.GET.getlist('keyword')
    # user = name
        
    values_df = calculate(df, gender, age, keyword)
    data = {
        # 'username' : user,
        'gender' : gender,
        'age' : age,
        'keyword' : keyword,
        'title_1' : values_df.title.iloc[0],
        'img_url_1' : values_df.image_url.iloc[0], 
        'title_2' : values_df.title.iloc[1],
        'img_url_2' : values_df.image_url.iloc[1], 
        'title_3' : values_df.title.iloc[2],
        'img_url_3' : values_df.image_url.iloc[2], 
    }
    
    return render(request, 'musical/results.html', data)
        
    
        
        
    
    

    