import os
import pandas as pd
import pickle
feature={}
for i in os.listdir(r'.\feature'):
    path=os.path.join(r'.\feature',i)
    with open(path,encoding='utf-8') as f:   
        df=pd.read_table(f)
        df.to_csv(path.replace('.txt','.csv'))
    feature[i[:-4]]=df
    
with open('feature.pkl','wb') as f:   
    pickle.dump(feature,f)

with open('feature.pkl','rb') as f:   
    t=pickle.load(f)