import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datatable as dt
from termcolor import colored
from datetime import datetime
import seaborn as sns


def clean_profiles(df_name):
    df = pd.read_csv('instagram_profiles.csv',sep='\t')
    df = df.drop(['firstname_lastname','description','url','cts'],axis=1)
    df = df.dropna(subset=['profile_id','profile_name'],thresh=2,axis=0)
    df_col=['following','followers','n_posts']
    for i in df_col:
        df[i].fillna(0,inplace=True)
    df = df.astype({'followers':'int','following':'int','n_posts':'int'})

    df.to_csv(r'C:\Users\matti\Desktop\ADM\HW2\new_profiles.csv',sep='\t')
    return df

def clean_locations(df_name):
    df = pd.read_csv(df_name,sep='\t')
    df = df.drop(df.iloc[:,3:22],axis=1)
    return df

##### [RQ2]

def n_posts(df_name):
    df_profiles=pd.read_csv(df_name,sep='\t',index_col=['profile_name'],usecols=['profile_name','n_posts'])
    d={}
    for i in enumerate(df_profiles.n_posts.sort_values(ascending=False).head(1500).items()):
        if i[0] not in d:
            d[i[0]]=i[1][1]

    # create data
    x=d.keys()
    y=d.values()

    fig=plt.figure(figsize=(20,7))
    # Same, but add a stronger line on top (edge)
    plt.fill_between( x, y, color="skyblue", alpha=0.2)
    plt.plot(x, y, color="Slateblue", alpha=0.6)
    # See the line plot function to learn how to customize the plt.plot function
    plt.ticklabel_format(style='plain', axis='x')
    plt.xlabel('number of profiles',color='green')
    plt.ylabel('number of posts',color='green')
    # Show the graph
    return (plt.show())


def posts_max_likes(df_name):
    top_rows=[]
    for chunk in (pd.read_csv(df_name, delimiter='\t',usecols=['post_id','numbr_likes'],
                          chunksize=10000000)):
        chunk=chunk.drop_duplicates(subset=['post_id'],keep=False)
        chunk=chunk.dropna()
        chunk = chunk.astype({'numbr_likes':'int'})
        top_rows.append(chunk[['post_id','numbr_likes']].sort_values(by='numbr_likes',ascending=False).head(1))
    for j in top_rows:
        print(j)

def post_max_least_comments(df_name):
    top_bottom_rows=[]
    top_rows=[]
    for chunk in (pd.read_csv(df_name, delimiter='\t',usecols=['post_id','number_comments'],
                          chunksize=10000000)):
        chunk=chunk.drop_duplicates(subset=['post_id'],keep=False)
        chunk=chunk.dropna()
        chunk = chunk.astype({'number_comments':'int'})
        top_rows.append(chunk.sort_values(by='number_comments',ascending=False).head(1))
        top_bottom_rows.append(chunk.sort_values(by='number_comments',ascending=True).head(1))
    print(colored('Posts which have the most number of comments','red'))
    for j in top_rows:
        print(j)
    
    print(colored('Posts which have least number of comments','red'))

    for j in top_bottom_rows:
        print(j)

    
def counter(df_name):
    counter_photo=0
    counter_both=0
    counter_videos=0
    for chunk in (pd.read_csv(df_name, delimiter='\t',usecols=['post_id','post_type'],chunksize = 10000000)):
        for j in chunk.post_type.items():
            if j[1]==1:
                counter_photo+=1
            elif j[1]==3:
                counter_both+=1
            elif j[1]==2:
                counter_videos+=1
    print('The number of posts with only photos is: ', counter_photo)
    print('The number of posts with only videos is: ', counter_videos)
    print('The number of posts with photos and videos is:', counter_both)

def is_business(df_name):
    df_profiles = pd.read_csv(df_name,sep='\t',usecols=['is_business_account'])
    T=(round(sum(df_profiles.is_business_account==True)/len(df_profiles.is_business_account)*100,2))
    F=(round(sum(df_profiles.is_business_account==False)/len(df_profiles.is_business_account)*100,2))
    UKN = round((df_profiles.is_business_account.isnull().sum())/len(df_profiles.is_business_account)*100,2)
    
    labels=['Business','not-business','unknown']
    sizes = [T,F,UKN]
    explode = [0,0.05,0.09]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,explode=explode,autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt.show()

def post_locations(df_name):
    a,b = 0,0
    for chunk in (pd.read_csv(df_name, delimiter='\t',usecols=['location_id'],chunksize=10000000)):
        a+=(chunk.location_id.isnull().sum())
        b += chunk.location_id.notnull().sum()
    print('The number of posts with tagged location are: ',b)
    print('The number of posts without tagged location are: ',a)
    
    labels= ['percentage of posts with location_id','percentage of posts with not-location_id']
    sizes = [b*100/(a+b),a*100/(a+b)]
    ax1=plt.subplot()
    ax1.pie(sizes, labels=labels,autopct='%1.1f%%',
        shadow=True, startangle=90,explode=[0,0.09])
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt.show()

### RQ3

def time_posts(df_name):
    t={}
    for j in range(0,24):
        t[j]=0
    for chunk in (pd.read_csv(df_name,delimiter='\t',usecols=['cts'],chunksize=10000000)):
        chunk['cts']=(pd.to_datetime(chunk['cts'],format='%Y-%m-%d %H:%M:%S.000').dt.hour)
        c = chunk.groupby('cts')['cts'].count()
        for j in c.items():
            if j[0] in t:
                t[j[0]]+=j[1]
    
    #### Let's plot it 
    
    x=list(t.keys())
    y=list(t.values())

    fig = plt.figure(figsize=(10,5))
 
    plt.bar(x,y,color='royalblue',width=0.6)
    plt.xticks(x)
    plt.xlabel('hours',color='green')
    plt.ylabel('number of posts',color='green')
    plt.title('Time in which users publish their posts',color='red')
    plt.ticklabel_format(style='plain', axis='y')
    
    return(plt.show())



def intervals(df_name):
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

    for chunk in (pd.read_csv(df_name,sep='\t',usecols=['cts'],chunksize=10000000)):
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

    return (plt.show())

### RQ4

def account_posts(df_post):
    n = 1
    print("what is the profile ID?")
    pid = float(input())
    df_posts = pd.read_csv(df_post, delimiter = '\t', usecols = [ 'profile_id', 'post_id'])
    d = {}
    for i in range(n):
        p_id = pid
        l = []
        for i,j in zip(df_posts.profile_id,df_posts.post_id):
            if p_id == i:
                l.append(j)
                if p_id not in d:
                    d[int(p_id)]=l
                else:
                    d[int(p_id)] = l

    return print(d)

def tuttipostxtopn(df_post, df_profiles):
    print('How many profile_id? ')
    n = int(input())
    df_profiles = pd.read_csv(df_profiles, sep = "\t")
    df_profiles_ord=df_profiles.sort_values(by='n_posts',ascending=False)
    topn=df_profiles_ord.head(n)
    dbis = {"ciao":""}
    dt_posts = dt.fread(df_post,columns={'post_id','profile_id'})
    df_posts = dt_posts.to_pandas()
    for pid in topn.profile_id:
        d = {}
        for i in range(n):
            p_id = pid
            l = []
            for i,j in zip(df_posts.profile_id,df_posts.post_id):
                if p_id == i:
                    l.append(j)
                    if p_id not in d:
                        d[int(p_id)]=l
                    else:
                        d[int(p_id)] = l
                    
            return print(d)
        
def likecom_top10(def_post, def_profiles):
    dt_posts = dt.fread(def_post,columns={"post_id","profile_id","numbr_likes", "number_comments"})
    post55 = dt_posts.to_pandas()
    
    post55 = post55.dropna()
    post55.numbr_likes = pd.to_numeric(post55.numbr_likes, errors ='coerce')
    post55.number_comments = pd.to_numeric(post55.number_comments, errors ='coerce')
    df_profiles = pd.read_csv(def_profiles, sep = "\t")
    
    top10forpost = df_profiles.sort_values(by=['n_posts'], ascending = False)
    top10forpost1 = top10forpost.head(10)
    
    df_merge0 = pd.merge(top10forpost1,post55,left_on = 'profile_id', right_on = 'profile_id', how = "inner")
    df_merge0bis = df_merge0[["profile_id", "profile_name", "n_posts", "post_id","numbr_likes", "number_comments"]]
    mergegroup0 = df_merge0bis.groupby(["profile_name","profile_id", "n_posts"])["numbr_likes", "number_comments"].mean()
    
    risultati0 = np.round(mergegroup0, decimals = 2)
    risultati0bis = risultati0.rename(columns={"numbr_likes": "Average number of likes", "number_comments": "Average number of comments"})
    a = risultati0bis[["Average number of likes", "Average number of comments"]].sort_values(by="n_posts", ascending = False)
    
    
    return display(a)

def top_10_intervals(df_post,df_profile):
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
    dt_posts = dt.fread(df_post,columns={'post_id','profile_id','cts','sid_profile'})
    df_posts = dt_posts.to_pandas()
    df_profiles=pd.read_csv(df_profile,sep='\t',usecols=['sid','profile_id','profile_name','n_posts'])
    top_10=df_profiles.sort_values(by='n_posts',ascending=False).head(10)
    df_merge=pd.merge(df_posts,top_10,left_on='sid_profile',right_on='sid',how='inner')
    def time_slots (x):
        for i in l:
            if i[0]<=x<=i[1]:
                return str(i[0])+'-'+str(i[1])
            else:

                continue
    d={}

    df_merge['cts']=pd.to_datetime(df_merge['cts'],format='%H:%M:%S').dt.time
    c = df_merge.groupby('cts')['cts'].count()
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

    (plt.show())

#### RQ5

def post_top10(def_profiles):
    df_profiles = pd.read_csv(def_profiles, sep = "\t")
    df_profiles_ordered = df_profiles.sort_values(by=['followers'], ascending = False)
    top10 = df_profiles_ordered.head(10)
    top10_posts = top10[["profile_name","n_posts"]]
    fig,ax = plt.subplots(figsize = (20,9))
    a = sns.barplot(x = top10.profile_name, y =top10.n_posts)
    b= a.set(xlabel = "Top 10 influencers (profiles with more followers)", ylabel = "Number of posts")
    return print(display(top10_posts), b)


def top1(def_profiles):
    df_profiles = pd.read_csv(def_profiles, sep = "\t")
    df_profiles_ordered = df_profiles.sort_values(by=['followers'], ascending = False)
    top_influencer = df_profiles_ordered.head(1)
    a = top_influencer[["profile_id", "profile_name", "following", "followers", "n_posts"]]
    return display(a)


def toplocations(def_post, def_profiles, def_locations):
    dt_posts = dt.fread(def_post,columns={'post_id','profile_id','location_id'})
    post53 = dt_posts.to_pandas()
    
    post53 = post53.dropna()
    df_profiles = pd.read_csv(def_profiles, sep = "\t")
    df_profiles_ordered = df_profiles.sort_values(by=['followers'], ascending = False)
    top10 = df_profiles_ordered.head(10)
    top10_posts = top10[["profile_name","n_posts"]]
    df_mergepost = pd.merge(top10,post53,left_on = 'profile_id', right_on = 'profile_id', how = "inner")
    df_locations = pd.read_csv(def_locations, sep = "\t")
    df_locations = df_locations.drop(df_locations.iloc[:,3:22], axis = 1)
    df_mergeloc = pd.merge(df_mergepost,df_locations,left_on = 'location_id', right_on = 'id', how = "inner")
    df_mergeloc = df_mergeloc[["profile_id", "profile_name", "n_posts", "post_id", "location_id", "name"]]
    df_mergeloc
    locationscount = df_mergeloc.name.value_counts()
    top10loc = locationscount.head(10)
    d = {}
    for i in top10loc.items():
        if i[0] not in d:
            d[i[0]] = i[1]


    x = list(d.keys())
    y = list(d.values())

    fig = plt.figure(figsize = (22,10))
    colors = ("red")
    plt.bar(x,y, color = colors, width = 0.6)
    plt.xlabel("most tagged locations for top 10 influencers")
    
    return (display(top10loc), plt.show())

def pic_video(def_post, def_profiles):
    dt_posts = dt.fread(def_post,columns={'post_id','profile_id','post_type'})
    post54 = dt_posts.to_pandas()
    
    df_profiles = pd.read_csv(def_profiles, sep = "\t")
    df_profiles_ordered = df_profiles.sort_values(by=['followers'], ascending = False)
    top10 = df_profiles_ordered.head(10)
    df_merge = pd.merge(top10,post54,left_on = 'profile_id', right_on = 'profile_id', how = "inner")
    mergegroup = df_merge.groupby(["post_type"])
    mergegroup_count = mergegroup.size().to_frame(name="Number of post").reset_index()
    a = mergegroup_count
    colors = sns.color_palette('bright')[0:5]
    plt.pie(mergegroup_count["Number of post"], labels = mergegroup_count["post_type"], colors = colors, autopct='%.0f%%')
    
    return (display(a), plt.show())
            

def like4followers(def_posts, def_profiles):
    
    dt_posts = dt.fread(def_posts,columns={'post_id','profile_id','numbr_likes','number_comments'})
    post55 = dt_posts.to_pandas()
    
    post55 = post55.dropna()
    post55.numbr_likes = pd.to_numeric(post55.numbr_likes, errors ='coerce')
    post55.number_comments = pd.to_numeric(post55.number_comments, errors ='coerce')
    
    dt_posts = dt.fread(def_posts,columns={'post_id','profile_id','post_type'})
    post54 = dt_posts.to_pandas()
    
    post54 = post54.dropna()
    df_profiles = pd.read_csv(def_profiles, sep = "\t")
    df_profiles_ordered = df_profiles.sort_values(by=['followers'], ascending = False)
    top10 = df_profiles_ordered.head(10)
    df_merge = pd.merge(top10,post54,left_on = 'profile_id', right_on = 'profile_id', how = "inner")
    df_merge2 = pd.merge(df_merge,post55,left_on = 'profile_id', right_on = 'profile_id', how = "inner")
    mergegroup2 = df_merge2.groupby(["post_type"])
    risultati = np.round(mergegroup2.mean(), decimals = 2)
    risultati2 = risultati.rename(columns={"numbr_likes": "Average number of likes", "number_comments": "Average number of comments"})
    a = display(risultati2[["Average number of likes", "Average number of comments"]])
    top10["followers"]
    mediafol = np.mean(top10["followers"])
    b = print("the average of followers for the top10 profile is:", mediafol)
    
    return a, b


### RQ6
def time_intervals(df_posts_name,df_profiles_name,cols_posts):
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

def RQ6_1(df_posts,df_profiles):
    df = time_intervals(df_posts,df_profiles,['sid_profile','cts','profile_id'])
    td_secs = df[['avg_time_diff']]/ np.timedelta64(1, 's')
    td_secs.sort_values('avg_time_diff')
    
    td_secs = td_secs[td_secs.avg_time_diff>0]
    td_secs = td_secs.sort_values('avg_time_diff')
    td_secs = td_secs.apply(np.log)
    
    
    df_sorted_by_count = df.sort_values('number_of_posts')
    avgTime = df['avg_time_diff'].mean()
    days=df['avg_time_diff'].mean().days
    mins = avgTime - datetime.timedelta(days=days)
    seconds = datetime.timedelta.total_seconds(mins)
    totalMinutes = seconds/60
    td = 'Days: '+ str(days) + ' and Minutes: '+ str (round(totalMinutes,2))
    
    df_sorted_by_count = df_sorted_by_count.reset_index()
    topThree = df_sorted_by_count[['followers','following','number_of_posts','profile_id']].tail(3)
    topThree=topThree.set_index('profile_id')
    topThree.plot(kind="bar",figsize=(10,6))
    plt.title("Users with largest number of posts")
    plt.xlabel("Profile ID")
    plt.ylabel("count")
    return(print(td),plt.show())


def intervals_RQ6(df_name,ind,y_label,title):
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

    
    h={}
    for chunk in (pd.read_csv(df_name,sep='\t',usecols=['cts',ind],chunksize=10000000)):
            chunk['cts']=pd.to_datetime(chunk['cts'],format='%Y-%m-%d %H:%M:%S.000').dt.time
            c = chunk.groupby('cts')[ind].sum()
            f= chunk.groupby('cts')[ind].count()
            for i,j in zip(c.items(),f.items()):
                if i[0] not in d:

                    if time_slots(i[0]) not in d :
                        d[(time_slots(i[0]))]=i[1]
                    else:
                        d[(time_slots(i[0]))]+=i[1]
                    if time_slots(j[0]) not in h :
                        h[(time_slots(j[0]))]=j[1]
                    else:
                        h[(time_slots(i[0]))]+=j[1]
    key=None
    if key in (d):
            del d[key]
    if key in h:
            del h[key]
    s={}
    for i,j in zip(d,h):
        s[i]=round(d[i]/h[j],1)
    d_ord=sorted(s.keys())
    new_d={}

    for i in d_ord:
            if i not in new_d:
                new_d[i]=s[i]


    
   

    x=list(new_d.keys())
    y=list(new_d.values())

    fig = plt.figure(figsize=(15,7))

    plt.bar(x,y,color='blue',width=0.6)
    plt.xticks(x)
    plt.xlabel('time intervals',color='green')
    plt.ylabel(y_label,color='green')
    plt.title(title,color='red')
    plt.ticklabel_format(style='plain', axis='y')

    return (plt.show(),s)

### RQ7

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

def prob_likes(df_posts,df_profiles):
    #Getting the dataframe ready
    df_merge = posts_df(df_posts,df_profiles,['numbr_likes','profile_id','sid_profile'],['sid','profile_id','followers'])
    df_prob = df_merge[df_merge.numbr_likes > (df_merge.followers)*0.2]
    prob = len(df_prob.index)/len(df_merge.index)
    print('The probability that a post receives more than 20% "likes" of the number of followers a user has is: ',round(prob*100,2),' %')
    
    
def prob_loc(df_posts,df_profiles,df_locations):
    #Creating the dataframe for the posts with locations
    df_merge = posts_df(df_posts,df_profiles,['profile_id','sid_profile','location_id'],['sid'])
    #Creating the dataframe for the locations
    df_locations = pd.read_csv(df_locations,sep='\t', usecols = ['name','id'])
    #cleaning the locations dataframe
    df_locations = df_locations.dropna()
    #merging both datasets to remove any posts with invalid locations
    df_merge_locations = pd.merge(df_merge,df_locations,left_on = 'location_id', right_on = 'id')
    #Getting the number of times a user posted from a locations
    df_gb = df_merge_locations.groupby( [ "name", "profile_id"] ).size().to_frame(name = 'visits').reset_index()
    prob = len(df_gb[df_gb.visits>1].index)/len(df_gb.index)
    print('The probability that a user returns to a site after having posted it in the past is: ', round(prob*100,2), ' %')



    
    
#### RQ8    

def like_comm(def_posts):
    dt_posts = dt.fread(def_posts,columns={'numbr_likes','number_comments'})
    df_posts = dt_posts.to_pandas()
    
    df_posts.numbr_likes = pd.to_numeric(df_posts.numbr_likes, errors ='coerce')
    df_posts.number_comments = pd.to_numeric(df_posts.number_comments, errors ='coerce')
    plt.figure(figsize = (10,5))
    c = df_posts[["numbr_likes", "number_comments"]].corr()
    sns.heatmap(c, cmap = "BrBG", annot = True)
    corrlikes = df_posts.numbr_likes.dropna()
    corrcomments = df_posts.number_comments.dropna()
    a = print(corrlikes.corr(corrcomments, method = "pearson"))
    b = sns.scatterplot(x="numbr_likes", y="number_comments", data=df_posts);
    # anche la scatterplot dimostra quanto non ci sia correlazione
    
    return a,b

def followers(df_name):
    df_profiles=pd.read_csv(df_name,sep='\t')
    followers = df_profiles.followers.dropna()
    followers2 = followers.apply(lambda x: x+1)
    followers2log = followers2.apply(np.log)
    figure, axes = plt.subplots(figsize = (10,5))
    sns.histplot(followers2log, bins = 50, color = "yellow")
    mean = followers.mean()
    mode = followers.mode()
    Q1 = followers.quantile(0.25)
    Q3 = followers.quantile(0.75)
    print("the average of followers for profile is:", mean)
    print("The mode of the distribution is:", mode)
    print("The first quantile of the distribution is:", Q1)
    print("The third quantile of the distribution is:", Q3)
    return plt.show()





    
