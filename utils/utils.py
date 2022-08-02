import pandas as pd
import os
import sys
import urllib.request
from tqdm import tqdm
import json
import time
class DataUtils():

    def __init__(self,translator=None):
        
        self.translator=translator
    
    def load_data(self,path):
        '''
        read data file and returns dataframe
        '''
        if path.endswith('json'):
            df=pd.read_json(path)
        elif path.endswith('csv'):
            df=pd.read_csv(path)
        elif path.endswith('xlsx'):
            df=pd.read_excel(path)
        return df
    
    def save_data(self,df,path):
        '''
        save data file as (xlsx or csv or json) type
        return fname
        '''
        if path.endswith('json'):
            df.to_json(path)
        elif path.endswith('csv'):
            df.to_csv(path)
        elif path.endswith('xlsx'):
            df.to_excel(path)
        else:
            print('File Name Error')
        return path
    
    def clean(self,df,filter):
        df=df[df[filter]==1]
        return df

    def isInitialized(self):
        if self.translator==None:
            print('translator is not initialized')
            return False
        else:
            return True
    
    def translate_dataframe(self,df,column,target='en'):
        if not self.isInitialized: return None
        return self.translator.translate_dataframe(df,column,target)
    
    def translate(self,text,target='en'):
        if not self.isInitialized: return None
        return self.translator.translate(text,target)
    
    def translate_word(self,text,source='en',target='ko'):
        if not self.isInitialized: return None
        return self.translator.translate_word(text,source,target)
    
    def is_translated(self,df,column,target='en'):
        if not self.isInitialized: return None
        for ele in df[column]:
            source=self.translator.get_language_type(ele)
            if source != target: return False
        return True
    
    def topK(self,keywords,threshold=0.3,k=3):
        ret=[]
        print(type(keywords))
        keywords.sort(key=lambda x:x[1],reverse=True)
        for i in range(len(keywords)):
            if keywords[i][1] >=threshold:
                ret.append(keywords[i][0])
        return ret

