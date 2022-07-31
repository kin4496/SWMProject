import requests as req
import re
import json
import urllib.request
import requests
from tqdm import tqdm
class Papago():
    def __init__(self,client_id,client_secret):
        self.url='https://papago.naver.com/apis/n2mt/translate'
        self.header={'Referer': 'http://labspace.naver.com/nmt/',
            'x-naver-client-id': 'labspace',
            'cookie':'NNB=HFP4MON5RKQGE; _gcl_au=1.1.110275602.1655204188; _fbp=fb.1.1655204188098.1366464527; _gac_UA-103600426-2=1.1655204188.CjwKCAjw46CVBhB1EiwAgy6M4p34M_vF0MW7kFf3nMtuEMPNKRhFXT_eWPr8NcPKhOURIYmWnHKaPhoC08YQAvD_BwE; NID_AUT=M9XvaaQ1tdVJgKtfqIefIWV+ARCt7IOzNP9LXDIlfS/CPb/sGNP5b8ECINoX3fox; NID_JKL=eFKrIxQm/o1jLZ1pLUpXB2JhkQy+JboFCtO/shK+kGE=; _ga_4BKHBFKFK0=GS1.1.1657351665.5.0.1657351665.0; _gid=GA1.2.269578730.1658572027; NDARK=N; papago_skin_locale=ko; _ga=GA1.2.973912021.1654689496; JSESSIONID=75110426BF5C6ABF3077C3ADF4148F00; NID_SES=AAABnfRW/SccbDmOvVfXgu/LTCLw4m08+fWO//YYqpHYXAnAS6Nd/3xlSSpHvHi64tqmiXPz1nZVSKzF8skNxfm31kQb+Se0pYMm6c6UgGMADRzLV+IL863uRhiMaa7zaPvgGcXKoi4MBBDDBZDDtD/ton5SBscCg2ghLacemkXU6uuBtVdRMcMv9Vi0MBRkVfK6TKVnPIMIOtmco2ZOBq7+MM3OMfNtdVtiKoHI/KpOu+mCP+BP2RDrSzDapcgJlSeiVGeO6+5ObIFGxvILCUBM8QSz0+wTY6us/ES2GNs5Y6Ax3x7lgeDkboKVVPj0lZplGmkpB7o7eYtbnxe4YUHhepMz0BbLO60gPaFDwlmDPKFh2LsMLeJYw3xBvTHvbhMps0AlOT6ryM8k7so+PnNnAIMSNr9icPobjZriachSzieYkFhrC2pJNm0IGGBDlVqnx3zfICj7IcZGmvMS6/fUHjyFdprJqm3fpNXSRLF3zVPAVbvHQNmPQAdMjFHGmHq7TnHS94tiOo3eHudDBdYWmbDuI9hN/A4KHB5vPNAODiim; _ga_7VKFYR6RV1=GS1.1.1658651446.13.0.1658651446.60',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36'}
        self.client_id=client_id
        self.client_secret=client_secret
        self.isActivate=True
    
    def translate_word(self,word,source='en',target='ko'):
        client_id=self.client_id
        client_secret=self.client_secret
        resCode=None
        try:
            encText = urllib.parse.quote(word)
            data = "source="+source+"&target="+target+"&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                res=response_body.decode('utf-8')
                res=json.loads(res)
                return res['message']['result']['translatedText']
        except:
            if resCode==None:
                self.isActivate=False
                print("Too many request")
            else:
                print('Response Error')
        return word

    def translate(self,text,target='en'):
        client_id=self.client_id
        client_secret=self.client_secret
        resCode=None
        try:
            source=self.get_language_type(text)
            if source == target: return text
            if source == None: return text
            encText = urllib.parse.quote(text)
            data = "source="+source+"&target="+target+"&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                res=response_body.decode('utf-8')
                res=json.loads(res)
                return res['message']['result']['translatedText']
        except:
            if resCode==None:
                self.isActivate=False
                print("Too many request")
            else:
                print('Response Error')
        return text
    
    def translate_dataframe(self,df,column,target='en'):
        ret=[None for i in range(len(df))]
        for idx,text in enumerate(tqdm(df[column])):
            if self.isActivate:
                translated_text=self.translate(text,target)
                ret[idx]=translated_text
            else:
                ret[idx]=text
        df[column]=ret
        return df
    
    def get_language_type(self,text):

        client_id=self.client_id
        client_secret=self.client_secret
        encQuery = urllib.parse.quote(text)
        data = "query=" + encQuery
        url = "https://openapi.naver.com/v1/papago/detectLangs"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            res=response_body.decode('utf-8')
            res=json.loads(res)
            return res['langCode']
        else:
            print("Error Code:" + rescode)
            return None
