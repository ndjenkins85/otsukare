import pandas as pd
from app import app
from flask import render_template

db = pd.read_excel("database.xlsx", encoding="utf8").set_index("ID")

@app.route('/<search>')
def search_database(search): 
    if search=="all":
        results = db.to_html()
    else:
        search_index_results = []

        for col in db.columns.values:
            if db[col].dtype=="object":
                cutdown = db[col].str.contains(search)
                cutdown = cutdown[cutdown==True]
                for indexes in cutdown.index.tolist():        
                    search_index_results.append(indexes)

        search_index_results = list(set(search_index_results))
    
        if len(search_index_results)==0:
            results = "No results found for %s" % search
        else:
            results = db.loc[search_index_results].to_html() 
            
    #results = {'this': results}
    return render_template('index.html',title='Home', searches=results)