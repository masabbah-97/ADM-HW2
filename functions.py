import datatable as dt
import pandas as pd

def posts(df_posts_name,df_profiles_name,cols_posts,cols_profiles):
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
    df_joined = pd.merge(df_profiles,df_posts,left_on = 'sid', right_on = 'sid_profile')
    
    return df_joined
    
    

    
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


    
    
    
    