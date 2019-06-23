
# coding: utf-8

# In[5]:

import pandas as pd
from flask import Flask
app = Flask(__name__)


# In[6]:

#search = u'\u5b66'


# In[7]:

db = pd.read_excel("database.xlsx", encoding="utf8").set_index("ID")
#db["Kanji"].str.contains(search)


# In[8]:

@app.route('/<search>')
def search_database(search): 
    if search=="all":
        return db.to_html()
        
    search_index_results = []

    for col in db.columns.values:
        if db[col].dtype=="object":
            cutdown = db[col].str.contains(search)
            cutdown = cutdown[cutdown==True]
            for indexes in cutdown.index.tolist():        
                search_index_results.append(indexes)

    search_index_results = list(set(search_index_results))

    if len(search_index_results)==0:
        return "No results found for %s" % search
    else:
        return db.loc[search_index_results].to_html()


# In[ ]:

if __name__== '__main__':
    app.run()

