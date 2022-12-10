# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

st.title('PoroPermFlow:')
st.title('Permeameter Decay Curve')
st.markdown(r'''This short script is for the purposes of checking the pressure decay curve.  When the curve becomes linear, the experiment may be ended.''')

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file:
   st.write("Filename: ", uploaded_file.name)
df= pd.read_csv(uploaded_file, header=4, sep=';')
ds_samples= st.slider("How many data points shall be averaged?",value=20)
df= pd.DataFrame(df,index=range(100,len(df)-1)).reset_index(drop=True)
df['Press [bar]']= df['SN:353548 (S30X):P1 bar'].astype(float)
df['Time']= pd.to_datetime(df['Time SN:353548 (S30X):P1'], format='%d/%m/%Y %H:%M:%S %p.%f')
df['Time']= (df['Time']-df['Time'][0])
df['Time']= df['Time'].dt.total_seconds()
df_trim= df[['Time','Press [bar]']]
df_trim['Press [kPa]']= df_trim['Press [bar]']*100 
df_trim= df_trim.groupby(np.arange(len(df))//ds_samples).mean()

P_decay= []
for i in range(len(df_trim['Press [kPa]'])):
    if i==0:
        P_decay.append(0)
    else:
        dtime= (df_trim['Time'][i] - df_trim['Time'][i-1])
        dpress= (df_trim['Press [kPa]'][i] - df_trim['Press [kPa]'][i-1])
        P_decay.append(dpress/dtime)
with st.expander(r'''See Data'''):
    st.dataframe(df, width=10000)

with st.expander(r'''See Trimmed Data'''):
    st.dataframe(df_trim, width=10000)

df.rename(columns={ df.columns[7]: 'Amient Temperature [°C]' }, inplace = True)
Room_Temp= df['Amient Temperature [°C]'].astype(float)
Room_Press= df['SN:912972 (S30X):P1 bar'].astype(float)

col1, col2= st.columns(2)
col1.metric('Mean Temperature [°C]',  round(Room_Temp.mean(), 1))
col2.metric('Mean Atmospheric Pressure [kPa]', round((Room_Press.mean()*100), 3))

col3, col4, col5, col6, col7= st.columns(5)
col3.metric('Last 5 Presusre Decay Rates [kPa]', round(P_decay[-6],5))
col4.metric('fourth-to-last', round(P_decay[-4],5))
col5.metric('Third-to-last', round(P_decay[-3],5))
col6.metric('Second-to-last', round(P_decay[-2],5))
col7.metric('Last...', round(P_decay[-1],5))

fig,ax = plt.subplots()
ax.plot(df_trim['Time'], df_trim['Press [kPa]'], c='k');
ax.set_ylabel("Pressure [kPa]",color="black",fontsize=14)
ax2=ax.twinx()
ax2.plot(df_trim['Time'],P_decay, c='b')
ax2.set_ylabel("Press. Decay rate [kPa/s]",color="blue",fontsize=14)
ax.set_xlabel('Time [s]');
st.pyplot(fig)