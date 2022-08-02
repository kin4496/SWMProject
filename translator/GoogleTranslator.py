from googletrans import Translator
from tqdm import tqdm

class GoogleTranslator():
    def __init__(self,client_id,client_secret):
        self.client_id=client_id
        self.client_secret=client_secret
        self.translator=Translator()

    def translate(self,text,dest='en'):
        if text == None:
            return ''
        lang_text=text
        if len(text) >30:
            lang_text=text[:30]
        try:
            source=self.get_language_type(lang_text)
            if source==dest : return text
            text=self.translator.translate(text,dest=dest).text
        except:
            text='error'
        return text
    
    def translate_dataframe(self,df,column='lyric',dest='en'):
        ret=[]
        for text in tqdm(df[column]):
            translated_text=self.translate(text,dest)
            ret.append(translated_text)
        df[column]=ret
        return df

    def get_language_type(self,lyric):
        return self.translator.detect(lyric).lang