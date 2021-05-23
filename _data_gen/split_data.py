import pandas as pd
from datetime import datetime
import pytz
from collections import OrderedDict
import re
import numpy as np
import humanize
from nanoid import generate


def get_function_syntax(copyText, copy_id):
    return "(function(){ return copyToClipboard(\'" + copyText + "\', '" + copy_id + "');})()"



IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)

df = pd.read_csv('curr_time.csv', sep='|')
MISSING_INFO = ' Info Missing'
df.fillna(MISSING_INFO, inplace=True)

df['Availability Status'] = df['Availability Status'].str.strip()
for na in ['', 'Undetermined']:
    df.loc[df['Availability Status']==na] = MISSING_INFO.strip()

df.loc[df['Availability Status']=='Will be available soon'] = 'Available soon'



print(set(list(df['Availability Status'] )))
resource = 'res'
category_desc = OrderedDict({'Admission':"Hospital Beds", 'oxygen': "Oxygen supplies", 'blood': "Blood and Plasma",
                'test': "Covid Testing",  'tele': "Doctor Tele-consultation",'food': "Food", 'ambulance': "Ambulance",
                "Quarantine": "Quarantine & Home Care", "Medicine": "Medicine Delivery", "volunteer": "Volunteer" })
short_desc = OrderedDict({'Admission':"Hospital Beds",  'oxygen': "Oxygen",
                'test': "Covid Test", 'blood|plasma': "Blood and Plasma", 'tele': "Doctor", 'food': "Food", 'ambulance': "Ambulance",
                "Quarantine": "Quarantine & Home Care", "Medicine": "Medicine", "volunteer": "Volunteer"  })
# decide what are the resources


resources_all = set()
for i,row in df.iterrows():
    resources_all.add(str(row['Facility provided']).lower())

def genUrl(entity):
    s = re.sub(r"[^\w\s]", '', entity)
    # Replace all runs of whitespace with a single dash
    dis_link = re.sub(r"\s+", '-', s)
    return dis_link

def genDistrict(category, category_desc, districts, available_res):

    fin_str = f"---\nlayout: card\ntitle: {category_desc[category]}\npermalink: /{category}/\n---\n"
    # fin_str = fin_str + f'<h3> Available leads: {available_res}</h3>'
    # fin_str = fin_str + '<div align="center">\n <div class="btn-group">\n'
    fin_str = fin_str + '<div align="center">\n'

    #     <a href="{{ "/food/" | relative_url}}" >
    #     <div class="card">
    #         <h4><b>Food</b></h4>
    #     </div>
    # </a>
    for dis in districts:
        dis_link = genUrl(dis)
        # fin_str = fin_str + '<a href="{{ "/' + category+'/'+ dis_link + '" | relative_url}}" class="button"><button>' + dis +'</button></a>\n'
        # <a href="{{ "/Admission/Alipurduar" | relative_url}}" ><div class="card"><h4><b>Alipurduar</b></h4></div></a>

        #fin_str = fin_str + '<a href="{{ "/' + category+'/'+ dis_link + '" | relative_url}}" ><div class="card"><h4><b>' + dis +'</b></h4></div></a>\n'
        fin_str = fin_str + '<a href="{{ "/' + category + '/'+ dis_link + '" | relative_url}}" ><div class="card"><h4><b>' + dis + '</b></h4></div></a>\n'

    fin_str = fin_str + '<div style="margin-top: 20px; text-align: left; border: none;">\n'
    fin_str = fin_str + '\n</div>\n<div class="text_foot"> Data updated at: {:%d, %b %Y} </div>'.format(datetime_ist)
    fin_str = fin_str + '</div>'
    with open('res_'+category+'.markdown', 'w') as f:
        f.write(fin_str)




def getString(key, value):
    value = str(value).lower()
    if value.strip() in ['na', '', 'nan', 'unknown', 'not known', 'not available', MISSING_INFO.lower().strip()] :
        return ''
    return  f'<tr><th>{key}</th><th>{str(value).title()}</th></tr>\n'

# def gen_res_page(category, long_desc, short_desc, df, paginate=False):


#     if len(df) > 10:
#         print('paginate {}'.format(category))
#         avail_dist = []

#         for dist in df['District']:
#             avail_dist.add(dist)
#         dists = list(avail_dist).sort()
#         for dist in dists:
#             if 'kolkata' in dist.lower():
#                 continue
#             sub_df = df['District'].str.contains(dist, na=True, case=False)

#     else:
#         print(category, len(df))
# Malda,Uttar Dinajpur,Dakshin Dinajpur,Murshidabad,Birbhum,Hooghly,Paschim Burdwan (West Bardhaman),Purba Burdwan (Bardhaman),
# Alipurduar,Cooch Behar,Darjeeling,Jalpaiguri,Kalimpong,Howrah,Kolkata,Nadia,North 24 Parganas,South 24 Parganas,Bankura,Jhargram,
# Purulia,Purba Medinipur,Paschim Medinipur
all_districts = ["Alipurduar","Bankura","Birbhum","Cooch Behar","Dakshin Dinajpur","Darjeeling","Hooghly","Howrah","Jalpaiguri","Jhargram",\
"Kalimpong","Kolkata","Malda","Murshidabad","Nadia","North 24 Parganas","Paschim Medinipur",\
"Paschim Burdwan","Purba Burdwan","Purba Medinipur","Purulia",\
"South 24 Parganas", "Uttar Dinajpur"]

all_districts.sort()
for category in category_desc.keys():
    if category == 'blood':
        cat_str = 'blood|plasma'
    else:
        cat_str = category
    sub_df = df[df['Facility provided'].str.contains(cat_str, case=False)]


    # ['Facility provided', 'District', 'Name of the Organisation/Contact Person', 'Location', 'Contact number', 'Verification  Status', 'Verification time', 'Availability Status', 'Info Missing']
    # print(sub_df.columns)
    fin_sub_df = sub_df[['District','Name of the Organisation/Contact Person','Location','Contact number','Verification  Status','Verification time','Availability Status']].to_csv(sep='|')
    fin_sub_df = fin_sub_df.replace(',',' ')
    fin_sub_df = fin_sub_df.replace('|',',')
    with open('res'+'_'+category+'.csv', 'w') as f:
        f.write(fin_sub_df)

    available_districts = list()
    # render the markdown itself!


    available_res = len(sub_df[sub_df['Availability Status'] == 'Available'])
    for sel_district in all_districts:
        sel_str = [sel_district, MISSING_INFO]
        dis_sub_df = sub_df[sub_df['District'].str.contains('|'.join(sel_str), case=False)]
        if len(dis_sub_df) == 0:
            continue
        # sort by district and verified
        dis_sub_df = dis_sub_df.sort_values(["District", "Availability Status", "Verification  Status", "Verification time"], ascending = (False, True, False, False))


        dis_link = genUrl(sel_district)
        header = f"---\nlayout: card\ntitle: {category_desc[category]}\npermalink: /{category}/{dis_link}\n---\n"
        body = '\n <div style="margin-top: 20px; text-align: left; border: none;">\n'
        body = body + '<input type="text" id="myInput" onkeyup="filterSearch()" placeholder="Search..">\n'
        body = body +  '\n <br><br>\n<div class="text_foot"><h4> Data updated at: {:%d, %b %Y %H:%M}. DISCLAIMER: All of these resources provided on an “as and when basis” and “as in” based on a fact check done by volunteers who are dedicated to help individuals and families in such challenging times. By using these resources, you are agreeing that WBCAN, however, do not accept any responsibility or liability for the accuracy, content, completeness, legality or reliability of the information contained in any of these. </h4> </div></div>\n'.format(datetime_ist)
        body = body + '<div class="row">\n\t<div class="column">\n'

        # iterate over each row and generate one card
        req_cols = ['Name of the Organisation/Contact Person','District','Location','Contact number','Verification  Status','Verification time','Availability Status']
        for i,row in dis_sub_df.iterrows():
            if row['Availability Status'] == 'Available':
                card_class = 'card_av'
            else:
                card_class = 'card_nav'

            body = body + f'<div class="{card_class}">\n'
            copyText = ""
            if  str(row[req_cols[0]]).lower() not in  ['na', 'nan', 'unknown', 'not known', 'not available', MISSING_INFO.lower()]:
                body = body + f'<h3>{str(row[req_cols[0]]).title()}</h3>\n\n'
                copyText = copyText + f"Name: {str(row[req_cols[0]]).title()}, "
            body = body + '<div class="info"><table>\n'
            if category in ['oxygen', 'blood']:
                body = body + f'<tr><th>Resource</th><th>{row["Facility provided"].title()}</th></tr>\n'
                resource = row["Facility provided"].title()
                copyText += f"ResourceInfo: {resource}, "

            for c in req_cols[1:]:
                if c == 'Contact number':
                    contacts = str(row[c]).split(',')
                    body = body + f'<tr><th>{c}</th><th>'
                    for contact in contacts:
                        body = body + f'<a href="tel:{contact}">{contact}</a>'
                        copyText += f"Contact: {contact}, "
                    body = body + '</th></tr>\n'
                else:
                    body = body + getString(c, row[c]) #f'<tr><th>{c}</th><th>{row[c]}</th></tr>\n'
            copy_id = generate("abcdefghijklmnopqrstuvwxyz", 5)
            copy = f'<tr><th>Copy this Information</th><th><span id="{copy_id}" onclick="{get_function_syntax(copyText, copy_id)}" class="copy-to-clip-board">copy</span></th></tr>'
            body += copy
            body = body + '</table></div></div>\n'

        footer = '</div>\n </div>'

        with open('res'+'_'+category+'_'+sel_district+'.markdown', 'w') as f:
            f.write(header+body+footer)
        available_districts.append(sel_district)
    genDistrict(category, category_desc, available_districts, available_res)
    print(f'{category}/{available_districts}')



print(resources_all)

btns = ''
for k,v in short_desc.items():
    btns = btns + '<a href="{{ "/' + k + '/" | relative_url}}" class="button"><button>' + v +'</button></a>\n'
print(btns)
