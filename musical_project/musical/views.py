from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from .models import name

import pandas as pd
import numpy as np
from pathlib import Path
from numpy import dot
from numpy.linalg import norm

def index(request):
    return render(request, 'musical/index_ODHversion2.html')

def post(request):

    if request.method == 'POST':
        username = request.POST.get('name')
        data={'user_name' : username}

    return render(request, 'musical/index_name_ODHversion2.html', data)

# def post2(request):

#     if request.method == 'GET':
#         gender = request.GET.get('gender')
#         age = request.GET.get('old')
#         keyword = request.GET.getlist('keyword')
#         data={'gender' : gender,
#               'age' : age,
#               'keyword' : keyword}

#     return render(request, 'musical/results.html', data)

#def calculate(df, gender, age, keyword, n=3):
#    
#    dic = {}
#    
#    if gender == '여성':
#        idx = df.sort_values('female', ascending = False).index
#    else:
#        idx = df.sort_values('male', ascending = False).index
#    for i in range(len(df)):
#        dic[idx[i]] = (len(df)-1-i)/(len(df)-1)
#        
#    if age == '10대':
#        idx = df.sort_values('10s', ascending = False).index
#    elif age == '20대':
#        idx = df.sort_values('20s', ascending = False).index
#    elif age == '30대':
#        idx = df.sort_values('30s', ascending = False).index
#    elif age == '40대':
#        idx = df.sort_values('40s', ascending = False).index
#    else:
#        idx = df.sort_values('50s', ascending = False).index
#    
#    for j in range(len(df)):
#        dic[idx[j]] += (len(df)-1-j)/(len(df)-1)
#        
#    df_mini = pd.DataFrame(columns = df.columns[-30:-1], data=np.zeros(len(df)*29).reshape(len(df), 29))
#    for x in keyword:
#        df_mini[x] = 1
#        
#    df_copy = df.copy()
#    df_copy['score_keyword'] = ((df_mini * df.iloc[:, -30:-1]).sum(axis=1))
#    idx = df_copy.sort_values('score_keyword', ascending=False).index
#    
#    for k in range(len(df)):
#        dic[idx[k]] += (len(df)-1-k)/(len(df)-1)
#        
#    sort_dic = sorted(dic, key=dic.get, reverse=True)
#    result_df = df.iloc[sort_dic[:n]]
#    
#    return result_df

def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))

def normalization(df_input):
    return df_input.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=0)

def age_calculate(age):
    if age < 15:
        age_vec = [1, 0, 0, 0, 0]
    elif (age >= 15) and (age < 25):
        age_vec = [1-(age-15)/10, 1-(25-age)/10, 0, 0, 0]
    elif (age >= 25) and (age < 35):
        age_vec = [0, 1-(age-25)/10, 1-(35-age)/10, 0, 0]
    elif (age >= 35) and (age < 45):
        age_vec = [0, 0, 1-(age-35)/10, 1-(45-age)/10, 0]
    elif (age >= 45) and (age < 55):
        age_vec = [0, 0, 0, 1-(age-45)/10, 1-(55-age)/10]
    elif age >= 55:
        age_vec = [0, 0, 0, 0, 1]
        
    return age_vec

def vectorize(df, gender, age, keyword):
    vec = pd.DataFrame(columns=df.columns, data=(np.zeros(len(df.columns)).reshape(1, len(df.columns))))
    
    if gender == '여성':
        vec['female'] = 1
    elif gender == '남성':
        vec['male'] = 1
    
    vec.iloc[:, 2:7] = age_calculate(float(age))
    
    for x in keyword:
        vec[x] = 1
        
    return vec  
    
def calculate(df, gender, age, keyword, n=3):
    
    df_good = pd.concat([df.iloc[:, 6:13], df.iloc[:, 13:].drop(columns=['category', 'image_url'])], axis=1)
    df_good = normalization(df_good)
    df_good_cp = df_good.copy()
    df_good_cp['score'] = -1*np.ones(len(df_good_cp))
    
    input_vec = vectorize(df_good, gender, age, keyword)
        
    for i in range(len(df_good)):
        df_good_cp['score'][i] = cos_sim(input_vec, df_good.iloc[i])
        
    temp_df = df_good_cp.sort_values('score', ascending=False)[:n]
    result_idx = temp_df.index
    result_df = df.iloc[result_idx]
    
    return result_df

def musical_recommend(request):
    THIS_FOLDER = Path(__file__).parent.parent.resolve()
    df = pd.read_csv(THIS_FOLDER/'전체뮤지컬_인코딩_imageurl추가_id추가.csv')
    
    if request.method == 'GET':
        gender = request.GET.get('gender')
        age = request.GET.get('age')
        keyword = request.GET.getlist('keyword')
        
    values_df = calculate(df, gender, age, keyword)
    data = {
        # 'username' : user,
        'gender' : gender,
        'age' : age,
        'keyword' : keyword,
        'title_1' : values_df.title.iloc[0],
        'img_url_1' : values_df.image_url.iloc[0],
        'musical_id_1' : "img/"+(str(values_df.id.iloc[0])+".png"),
        'title_2' : values_df.title.iloc[1],
        'img_url_2' : values_df.image_url.iloc[1], 
        'musical_id_2' : "img/"+(str(values_df.id.iloc[1])+".png"),
        'title_3' : values_df.title.iloc[2],
        'img_url_3' : values_df.image_url.iloc[2], 
        'musical_id_3' : "img/"+(str(values_df.id.iloc[2])+".png"),
    }
    
    return render(request, 'musical/results_ODHversion.html', data)
        
    

        
    
    

    