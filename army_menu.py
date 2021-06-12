import requests
import json
from collections import OrderedDict
def lambda_handler(event, context):
    file_data = OrderedDict()


    army_num = '7652'
    call_page = '1500'
    lis = 'https://openapi.mnd.go.kr/3331313332343635353437343432313337/json/DS_TB_MNDT_DATEBYMLSVC_'+army_num+'/1/'+call_page
    res = []
    res = requests.get(lis).json()
    #print(res['DS_TB_MNDT_DATEBYMLSVC_7652']['row'][0]['brst'])
    res1 = res['DS_TB_MNDT_DATEBYMLSVC_'+army_num]['row']
    lists = []
    lists2 = []
    for a in range(2020,2030):
        for b in range(1,13):
            for c in range(1,32):
                lists2.append(str(a)+str(b).zfill(2)+str(c).zfill(2))
                lists.append(str(a)+'-'+str(b).zfill(2)+'-'+str(c).zfill(2))
     #print(lists[0])
    dateslist = []
    for i in range(0,int(call_page)):
        if res1[i]['dates'] in lists:
            # print(i)
            dateslist.append(i)
        if res1[i]['dates'] in lists2:
            # print(i)
            dateslist.append(i)
            
    # print("길이"+str(len(dateslist)))

    for q in range(0,len(dateslist)-1):
        brsts=[]
        luncc=[]
        dinn=[]
    
        for jj in range(dateslist[q],dateslist[q+1]):
            if(res1[jj]['brst']!=''):
                brsts.append(res1[jj]['brst'])
            if(res1[jj]['lunc']!=''):
                luncc.append(res1[jj]['lunc'])
            if(res1[jj]['dinr']!=''):
                dinn.append(res1[jj]['dinr'])
            if(len(res1[dateslist[q]]['dates'])==8):
                res1[dateslist[q]]['dates'] = res1[dateslist[q]]['dates'][0:4]+'-'+res1[dateslist[q]]['dates'][4:6]+'-'+res1[dateslist[q]]['dates'][6:8]
        
        file_data[res1[dateslist[q]]['dates']] = {'brst':brsts,'lunc':luncc,'dinr':dinn}


    return(json.dumps(file_data,ensure_ascii=False,indent="\t"))



