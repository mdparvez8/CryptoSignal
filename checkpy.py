#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import datetime as dt
import numpy as np


# In[2]:


from sqlalchemy import create_engine


# In[3]:


engine=create_engine('sqlite:///cryptoDB.db')


# In[4]:


symbols=pd.read_sql('SELECT name FROM sqlite_master WHERE type="table"',engine).name.to_list()


# In[5]:


symbols


# In[6]:


st.title('welcome to the live ta platform')


# In[53]:


def applytechnicals(df):
    df['SMA7']=df.c.rolling(7).mean()
    df['SMA25']=df.c.rolling(25).mean()
    df.dropna(inplace=True)
    


# In[66]:


def qry(symbol):
    now=dt.datetime.utcnow()
    before=now-dt.timedelta(minutes=43200)
    qry_str=f"""SELECT E,c FROM '{symbol}' WHERE E>='{before}'"""
    df=pd.read_sql(qry_str,engine)
    df.E=pd.to_datetime(df.E)
    df=df.set_index('E')
    df=df.resample('5Min').last()
    applytechnicals(df)
    df['position']=np.where(df['SMA7']>df['SMA25'],1,0)
    return df


# In[67]:


def check():
    for symbol in symbols:
        if len(qry(symbol).position)>1:
            if qry(symbol).position[-1] and qry(symbol).position.diff()[-1]:
                st.write(symbol)


# In[68]:


st.button('Get Live SMA_Crossover',on_click=check())


# In[69]:


# qry('BTCUSDT')


# In[ ]:





# In[ ]:





# In[ ]:




