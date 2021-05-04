import pandas as pd 
from datetime import datetime
import pytz 
from collections import OrderedDict

IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)

df = pd.read_csv('curr_time.csv', sep='|')
resource = 'res'
category_desc = OrderedDict({'bed':"Hospital Beds", 'oxygen': "Oxygen supplies", 'blood': "Blood Plasma", 
                'test': "Covid Testing",  'tele': "Doctor Tele-consultation",'food': "Food", 'ambulance': "Ambulance",  'tele': "Doctor Tele-consultation", })
short_desc = OrderedDict({'bed':"Hospital Beds",  'oxygen': "Oxygen", 
                'test': "Covid Test", 'blood': "Blood and Plasma", 'tele': "Doctor", 'food': "Food", 'ambulance': "Ambulance"})
# decide what are the resources 
resources_all = set()
for i,row in df.iterrows():
    resources_all.add(str(row['Facility provided']).lower())

def getString(key, value):
    value = str(value).lower()
    if value == 'na' or value == 'nan' or 'unknown' in value or value == '' or 'not available' in value:
        return ''
    return  f'<tr><th>{key}</th><th>{value}</th></tr>\n'

for category in category_desc.keys():
    sub_df = df[df['Facility provided'].str.contains(category, na=False, case=False)]
    
    if category == 'oxygen':
        # decide which districts have them 
        districts = set()
        for v in sub_df['District']:
            districts.add(v)
        print(districts)
        
    # sort by district and verified 
    sub_df = sub_df.sort_values(["District", "Verification  Status"], ascending = (False, True))

    # print(sub_df.columns)
    fin_sub_df = sub_df[['District','Name of the Organisation/Contact Person ','Location','Contact number ','Verification  Status','Verification time','Availability Status']].to_csv(sep='|')
    fin_sub_df = fin_sub_df.replace(',',' ')
    fin_sub_df = fin_sub_df.replace('|',',')
    with open('res'+'_'+category+'.csv', 'w') as f:
        f.write(fin_sub_df)

    # render the markdown itself! 

    header = f"---\nlayout: card\ntitle: {category_desc[category]}\npermalink: /{category}/\n---\n"
    body = '<div class="row">\n\t<div class="column">\n'
    # iterate over each row and generate one card 
    req_cols = ['Name of the Organisation/Contact Person ','District','Location','Contact number ','Verification  Status','Verification time','Availability Status']
    for i,row in sub_df.iterrows():
        body = body + '<div class="card">\n'
        if not ('nan' == str(row[req_cols[0]]).lower() or 'unknown' in str(row[req_cols[0]]).lower()):
            body = body + f'<h3>{str(row[req_cols[0]]).title()}</h3>\n\n'
        body = body + '<div class="info"><table>\n'
        if category == 'oxygen':
            body = body + f'<tr><th>Resource</th><th>{row["Facility provided"].title()}</th></tr>\n'

        for c in req_cols[1:]:
            if c == 'Contact number ':
                body = body + f'<tr><th>{c}</th><th><a href="tel:{row[c]}">{row[c]}</a></th></tr>\n'
            else:
                body = body + getString(c, row[c]) #f'<tr><th>{c}</th><th>{row[c]}</th></tr>\n'
        body = body + '</table></div></div>\n'


    footer = '</div>\n</div> <br><br>\n<h4> Data updated at: {} </h4>'.format(datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))

    with open('res'+'_'+category+'.markdown', 'w') as f:
        f.write(header+body+footer)

print(resources_all)

btns = ''
for k,v in short_desc.items():
    btns = btns + '<a href="{{ "/' + k + '/" | relative_url}}" class="button"><button>' + v +'</button></a>\n'
print(btns)



    
