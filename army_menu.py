import requests
import json
from collections import OrderedDict
import re

def lambda_handler(event, context):
    file_data = OrderedDict()


    army_num = '7369'
    call_page = '1000'
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

                lists.append(str(a)+'-'+str(b).zfill(2)+'-'+str(c).zfill(2))
                lists2.append(str(a)+str(b).zfill(2)+str(c).zfill(2))
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
    #adspcfd
    for q in range(0,len(dateslist)-1):
        brsts=[]
        brst_cal=[]
        luncc=[]
        dinn=[]
        cake=[]
        regex = "\(.*\)|\s-\s.*"

    #re.sub(regex, '', text)
        if(dateslist[q+1]-dateslist[q]<15):
            for jj in range(dateslist[q],dateslist[q+1]):
                if(res1[jj]['brst']!=''):
                    if(res1[jj]['brst_cal'].find('k')==int('-1')):
                        if(res1[jj]['brst_cal'].find('*')!=int('-1')):
                            brsts.append(re.sub(regex,'',res1[jj]['brst'])+'('+res1[jj]['brst_cal'][2:]+' kcal)')
                        else:
                             brsts.append(re.sub(regex,'',res1[jj]['brst'])+'('+res1[jj]['brst_cal']+' kcal)')
                    else:
                        brsts.append(re.sub(regex,'',res1[jj]['brst'])+'('+res1[jj]['brst_cal']+')')

                if(res1[jj]['lunc']!=''):
                    if(res1[jj]['lunc_cal'].find('k')==int('-1')):
                        if(res1[jj]['lunc_cal'].find('*')!=int('-1')):
                            luncc.append(re.sub(regex,'',res1[jj]['lunc'])+'('+res1[jj]['lunc_cal'][2:]+' kcal)')
                        else:
                             luncc.append(re.sub(regex,'',res1[jj]['lunc'])+'('+res1[jj]['lunc_cal']+' kcal)')
                    else:
                        luncc.append(re.sub(regex,'',res1[jj]['lunc'])+'('+res1[jj]['lunc_cal']+')')


                if(res1[jj]['dinr']!=''):
                    if(res1[jj]['dinr_cal'].find('k')==int('-1')):
                        if(res1[jj]['dinr_cal'].find('*')!=int('-1')):
                            dinn.append(re.sub(regex,'',res1[jj]['dinr'])+'('+res1[jj]['dinr_cal'][2:]+' kcal)')
                        else:
                             dinn.append(re.sub(regex,'',res1[jj]['dinr'])+'('+res1[jj]['dinr_cal']+' kcal)')
                    else:
                        dinn.append(re.sub(regex,'',res1[jj]['dinr'])+'('+res1[jj]['dinr_cal']+')')

                if(res1[jj]['adspcfd']!='' and res1[jj]['adspcfd'].find('.')==int('-1')):
                    if(res1[jj]['adspcfd_cal'].find('k')==int('-1')):
                        if(res1[jj]['adspcfd_cal'].find('*')!=int('-1')):
                            cake.append(re.sub(regex,'',res1[jj]['adspcfd'])+'('+res1[jj]['adspcfd_cal'][2:]+' kcal)')
                        else:
                             cake.append(re.sub(regex,'',res1[jj]['adspcfd'])+'('+res1[jj]['adspcfd_cal']+' kcal)')
                    else:
                        cake.append(re.sub(regex,'',res1[jj]['adspcfd'])+'('+res1[jj]['adspcfd_cal']+')')



            if(len(res1[dateslist[q]]['dates'])==8):
                res1[dateslist[q]]['dates'] = res1[dateslist[q]]['dates'][0:4]+'-'+res1[dateslist[q]]['dates'][4:6]+'-'+res1[dateslist[q]]['dates'][6:8]

            file_data[res1[dateslist[q]]['dates']] = {'brst':brsts,'lunc':luncc,'dinr':dinn,'cake':cake}



    print(json.dumps(file_data,ensure_ascii=False,indent="\t"))





