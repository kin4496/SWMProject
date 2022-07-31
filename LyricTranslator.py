import pandas as pd
from utils import DataUtils
from tqdm import tqdm
import os
client_ids=['NeJEvEYOm7UusbYNde7g','dI4S2Ce4DKqwtAuF9UFa','3dvhgNwB2eOv7Rn1EjUc','N9zG4hJ64gZVXHwSvdW4','rwIWa9m84NNmuojMrns9',
'OPAHlhQRIvqCnjjvsbWY','mfok7VE1Nrp9i5I0k2ji','gmrdtMvOW6As2URWydoy','pnARumQUw8Ii8J8EQVbt']
client_secrets=['zDSxzWN6E0','87h5IiBzFk','lssCxyatQN','b6FUtHRBrj','_HZjYPx83R','XuQeKyceQs','AUVl6hvg9J'
,'WkK27dGVFs','d19N90Jb1A']
path='datasets'
fname='meta_list.xlsx'
origin_path=os.path.join(path,fname)
translated_path=os.path.join(path,'en '+fname)

for client_id,client_secret in zip(client_ids,client_secrets):
    utils=DataUtils(client_id,client_secret)
    if os.path.isfile(translated_path):
        df=utils.load_data(translated_path)
    else:
        df=utils.load_data(origin_path)
        df=utils.clean(df,'has_lyric')
    if not utils.is_translated(df,'lyric'):
        df=utils.translate_dataframe(df,column='lyric')
        utils.save_data(df,translated_path)

client_id='A4Mceclx8PV864nLzpJA'
client_secret='gSGhYL3Roj'
utils=DataUtils(client_id,client_secret)

df=utils.load_data(translated_path)
df2=pd.read_json('datasets/meta_list.json')
df2=utils.clean(df2,'has_lyric')
data=[]
for translated,origin in zip(tqdm(df['lyric']),df2['lyric']):
    lang=utils.translator.get_language_type(origin)
    if lang=='en':
        data.append(origin)
    elif lang=='ko':
        data.append(translated)
    else:
        print(lang)
        data.append(translated)

df['lyric']=data
