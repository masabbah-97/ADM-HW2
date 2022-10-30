import datatable as dt
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def posts_df(df_posts_name,df_profiles_name,cols_posts,cols_profiles):
    #Read both posts and profiles csv files
    dt_posts = dt.fread(df_posts_name)
    dt_profiles = dt.fread(df_profiles_name)
    
    #convert the datatable to dataframes
    df_posts = dt_posts[:,cols_posts].to_pandas()
    df_profiles = dt_profiles[:,cols_profiles].to_pandas()
    
    #removing rows with invalid sids
    df_posts=df_posts[df_posts.sid_profile!=-1]
    df_profiles = df_profiles[df_profiles.sid!=-1]
    
    #dropping NA rows
    df_posts = df_posts.dropna()
    df_profiles = df_profiles.dropna()
    
    #joining the two dataframes
    df_joined = pd.merge(df_profiles,df_posts,left_on = 'sid', right_on = 'sid_profile',how = 'inner')
    
    return df_joined
    
    

    
def time_intervals_df(df_posts_name,df_profiles_name,cols_posts):
    #Read both posts and profiles csv files
    dt_posts = dt.fread(df_posts_name)
    dt_profiles = dt.fread(df_profiles_name)
    
    #convert the datatable to dataframes
    df_posts = dt_posts[:,cols_posts].to_pandas()
    df_profiles = dt_profiles[:,['sid','profile_id','following','followers']].to_pandas()
    
    #removing rows with invalid sids
    df_posts=df_posts[df_posts.sid_profile!=-1]
    df_profiles = df_profiles[df_profiles.sid!=-1]
    
    #dropping NA rows
    df_posts = df_posts.dropna()
    df_profiles = df_profiles.dropna()
    
    #getting the average time taken between posts
    df_dt_avg = df_posts.groupby('sid_profile').cts.agg( avg_time_diff= lambda group: group.sort_values().diff().mean(), number_of_posts = lambda group: group.count())
    
    #joining the two dataframes
    df_joined = pd.merge(df_profiles,df_dt_avg,left_on = 'sid', right_on = 'sid_profile')
    #removing accounts that posted only once
    df_joined = df_joined[df_joined.number_of_posts>1]
    
    return df_joined


def intervals(df_name):
    print('How many time intervals?')
    n = int(input())
    l=[]
    for i in range(n):
        li=[]
        s=(datetime.datetime.strptime(input(), '%H:%M:%S').time())
        f=(datetime.datetime.strptime(input(), '%H:%M:%S').time())

        li.append(s)
        li.append(f)
        l.append(li)
    
    def time_slots (x):
        for i in l:
            if i[0]<=x<=i[1]:
                return str(i[0])+'-'+str(i[1])
            else:

                continue
    d={}

    for chunk in pd.read_csv(df_name,sep='\t',usecols=['cts'],chunksize=10000000):
        chunk['cts']=pd.to_datetime(chunk['cts'],format='%Y-%m-%d %H:%M:%S.000').dt.time
        c = chunk.groupby('cts')['cts'].count()
        for j in c.items():
            if time_slots(j[0])!='No':
                if time_slots(j[0]) not in d :
                    d[(time_slots(j[0]))]=j[1]
                else:
                    d[(time_slots(j[0]))]+=j[1]
    key=None
    if key in d:    
        del d[key]
    d_ord=sorted(d.keys())
    new_d={}
    
    for i in d_ord:
        if i not in new_d:
            new_d[i]=d[i]

    
   

    x=list(new_d.keys())
    y=list(new_d.values())

    fig = plt.figure(figsize=(15,7))

    plt.bar(x,y,color='blue',width=0.6)
    plt.xticks(x)
    plt.xlabel('time intervals',color='green')
    plt.ylabel('amount of posts',color='green')
    plt.title("Posts' amount for time interval",color='red')
    plt.ticklabel_format(style='plain', axis='y')

    return (plt.show(),l)


def intervals_1(df_name,ind,y_axis, title):
    print('How many time intervals?')
    n = int(input())
    l=[]
    for i in range(n):
        li=[]
        s=(datetime.strptime(input(), '%H:%M:%S').time())
        f=(datetime.strptime(input(), '%H:%M:%S').time())

        li.append(s)
        li.append(f)
        l.append(li)
    
    def time_slots (x):
        for i in l:
            if i[0]<=x<=i[1]:
                return str(i[0])+'-'+str(i[1])
            else:

                continue
    d={}

    for chunk in (pd.read_csv(df_name,sep='\t',usecols=['cts',ind],chunksize=10000000)):
        chunk['cts']=pd.to_datetime(chunk['cts'],format='%Y-%m-%d %H:%M:%S.000').dt.time
        c = chunk.groupby('cts')[ind].sum()
        for j in c.items():
            if time_slots(j[0])!='No':
                if time_slots(j[0]) not in d :
                    d[(time_slots(j[0]))]=j[1]
                else:
                    d[(time_slots(j[0]))]+=j[1]
    key=None
    if key in d:
        del d[key]
    d_ord=sorted(d.keys())
    new_d={}

    for i in d_ord:
        if i not in new_d:
            new_d[i]=d[i]

    
   

    x=list(new_d.keys())
    y=list(new_d.values())

    fig = plt.figure(figsize=(15,7))

    plt.bar(x,y,color='blue',width=0.6)
    plt.xticks(x)
    plt.xlabel('time intervals',color='green')
    plt.ylabel(y_axis,color='green')
    plt.title(title,color='red')
    plt.ticklabel_format(style='plain', axis='y')

    return (plt.show())


    
    
    