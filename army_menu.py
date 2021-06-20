import requests
import json
from collections import OrderedDict
import re
import datetime
from datetime import date


def lambda_handler(event, context):
    start = event['queryStringParameters']['start'] 
    end=event['queryStringParameters']['end']
    army=event['queryStringParameters']['army']
    a='w'

    
    file_data =[]
    print(context)
    print(event)
    army_num = army   
    call_page = '10'
    lis = 'https://openapi.mnd.go.kr/3331313332343635353437343432313337/json/DS_TB_MNDT_DATEBYMLSVC_'+army_num+'/1/'+call_page
    res = []
    res = requests.get(lis).json()
    call_page = str(res['DS_TB_MNDT_DATEBYMLSVC_'+army_num]['list_total_count'])
    
    lis = 'https://openapi.mnd.go.kr/3331313332343635353437343432313337/json/DS_TB_MNDT_DATEBYMLSVC_'+army_num+'/1/'+call_page
    res = []
    res = requests.get(lis).json()
    weeklist=['월요일', '화요일', '수요일', '목요일', '금요일', '토요일','일요일']
    res1 = res['DS_TB_MNDT_DATEBYMLSVC_'+army_num]['row']
    lists = []
    lists2 = []
    startFract = start.split('-')
    endFract = end.split('-')
    startDate = date(int(startFract[0]),int(startFract[1]),int(startFract[2]))
    endDate = date(int(endFract[0]),int(endFract[1]),int(endFract[2]))
    interval = endDate - startDate
    for a in range(2020,2030):
        for b in range(1,13):
            for c in range(1,32):

                lists.append(str(a)+'-'+str(b).zfill(2)+'-'+str(c).zfill(2))
                lists2.append(str(a)+str(b).zfill(2)+str(c).zfill(2))


    dateslist = []
    for i in range(0,int(call_page)):
        if res1[i]['dates'] in lists:
            # print(i)
            dateslist.append(i)
        if res1[i]['dates'] in lists2:
            # print(i)
            dateslist.append(i)

    for q in range(0,len(dateslist)-1):
        brsts=[]
        brst_cal=[]
        luncc=[]
        dinn=[]
        cake=[]
        regex = "\(.*\)|\s-\s.*"


        if(dateslist[q+1]-dateslist[q]<9):
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
            re_list=[]

            for fff in range(0,interval.days+1):
                tempDate=startDate+datetime.timedelta(days=fff)
                if(tempDate.isoformat() == res1[dateslist[q]]['dates']):
                    datesplit = res1[dateslist[q]]['dates'].split('-')
                    dateweekday = weeklist[datetime.date(int(datesplit[0]),int(datesplit[1]),int(datesplit[2])).weekday()]
                    file_data.append({'date':res1[dateslist[q]]['dates'],'weekday':dateweekday,'brst':brsts,'lunc':luncc,'dinr':dinn,'cake':cake})
 
                    
    
    return {
        "body" : json.dumps(file_data,ensure_ascii=False,indent="\t")
    }
