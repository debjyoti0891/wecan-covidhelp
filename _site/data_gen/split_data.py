import pandas as pd 
from datetime import datetime
import pytz 

IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)

df = pd.read_csv('curr_time.csv', sep='|')
resource = 'res'
categories = ['beds', 'oxygen', 'medicines', 'food']

for category in categories:
    sub_df = df[df['Facility provided'].str.contains(category, na=False, case=False)]
    
    # sort by district and verified 
    sub_df = sub_df.sort_values(["District", "Verification  Status"], ascending = (False, True))

    print(sub_df.columns)
    fin_sub_df = sub_df[['District','Name of the Organisation/Contact Person ','Location','Contact number ','Verification  Status','Verification time','Availability Status']].to_csv(sep='|')
    fin_sub_df = fin_sub_df.replace(',',' ')
    fin_sub_df = fin_sub_df.replace('|',',')
    with open('res'+'_'+category+'.csv', 'w') as f:
        f.write(fin_sub_df)

    # render the markdown itself! 

    header = f"---\nlayout: card\ntitle: {category}\npermalink: /{category}/\n---\n"
    body = '<div class="row">\n\t<div class="column">\n'
    # iterate over each row and generate one card 
    req_cols = ['Name of the Organisation/Contact Person ','District','Location','Contact number ','Verification  Status','Verification time','Availability Status']
    for i,row in sub_df.iterrows():
        body = body + '<div class="card">\n'
        body = body + f'<h3>{row[req_cols[0]]}</h3>\n\n'
        body = body + '<div class="info"><table>\n'
        for c in req_cols[1:]:
            body = body + f'<tr><th>{c}</th><th>{row[c]}</th></tr>\n'
        body = body + '</table></div></div>\n'


    footer = '</div>\n</div> <br><br>\n<h4> Data updated at: {} </h4>'.format(datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))

    with open('res'+'_'+category+'.markdown', 'w') as f:
        f.write(header+body+footer)


    
