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
        tempResDate=res1[i]['dates']
        if tempResDate in lists:
            # print(i)
            dateslist.append(i)
        if tempResDate in lists2:
            # print(i)
            dateslist.append(i)

    for q in range(0,len(dateslist)-1):
        brsts=[]
        brst_cal=[]
        luncc=[]
        dinn=[]
        cake=[]
        regex = "\(.*\)|\s-\s.*"

        dateslistQ=dateslist[q]
        dateslistQ1=dateslist[q+1]

        if(dateslistQ1-dateslistQ<15): 
            for jj in range(dateslistQ,dateslistQ1):
                res1jj=res1[jj]
                if(res1jj['brst']!=''):
                    if(res1jj['brst_cal'].find('k')==int('-1')):
                        if(res1jj['brst_cal'].find('*')!=int('-1')):
                            brsts.append(re.sub(regex,'',res1jj['brst'])+'('+res1jj['brst_cal'][2:]+' kcal)')
                        else:
                             brsts.append(re.sub(regex,'',res1jj['brst'])+'('+res1jj['brst_cal']+' kcal)')
                    else:
                        brsts.append(re.sub(regex,'',res1jj['brst'])+'('+res1jj['brst_cal']+')')

                if(res1jj['lunc']!=''):
                    if(res1jj['lunc_cal'].find('k')==int('-1')):
                        if(res1jj['lunc_cal'].find('*')!=int('-1')):
                            luncc.append(re.sub(regex,'',res1jj['lunc'])+'('+res1jj['lunc_cal'][2:]+' kcal)')
                        else:
                             luncc.append(re.sub(regex,'',res1jj['lunc'])+'('+res1jj['lunc_cal']+' kcal)')
                    else:
                        luncc.append(re.sub(regex,'',res1jj['lunc'])+'('+res1jj['lunc_cal']+')')


                if(res1jj['dinr']!=''):
                    if(res1jj['dinr_cal'].find('k')==int('-1')):
                        if(res1jj['dinr_cal'].find('*')!=int('-1')):
                            dinn.append(re.sub(regex,'',res1jj['dinr'])+'('+res1jj['dinr_cal'][2:]+' kcal)')
                        else:
                             dinn.append(re.sub(regex,'',res1jj['dinr'])+'('+res1jj['dinr_cal']+' kcal)')
                    else:
                        dinn.append(re.sub(regex,'',res1jj['dinr'])+'('+res1jj['dinr_cal']+')')

                if(res1jj['adspcfd']!='' and res1jj['adspcfd'].find('.')==int('-1')):
                    if(res1jj['adspcfd_cal'].find('k')==int('-1')):
                        if(res1jj['adspcfd_cal'].find('*')!=int('-1')):
                            cake.append(re.sub(regex,'',res1jj['adspcfd'])+'('+res1jj['adspcfd_cal'][2:]+' kcal)')
                        else:
                             cake.append(re.sub(regex,'',res1jj['adspcfd'])+'('+res1jj['adspcfd_cal']+' kcal)')
                    else:
                        cake.append(re.sub(regex,'',res1jj['adspcfd'])+'('+res1jj['adspcfd_cal']+')')



            if(len(res1[dateslistQ]['dates'])==8):
                res1[dateslistQ]['dates'] = res1[dateslistQ]['dates'][0:4]+'-'+res1[dateslistQ]['dates'][4:6]+'-'+res1[dateslistQ]['dates'][6:8]
            re_list=[]

            for fff in range(0,interval.days+1):
                tempDate=startDate+datetime.timedelta(days=fff)
                if(tempDate.isoformat() == res1[dateslistQ]['dates']):
                    datesplit = res1[dateslistQ]['dates'].split('-')
                    date_ko = datesplit[0]+'년 '+datesplit[1]+'월 '+datesplit[2]+'일'
                    dateweekday = weeklist[datetime.date(int(datesplit[0]),int(datesplit[1]),int(datesplit[2])).weekday()]
                    
                    checkDuplicate=False
                    for singleData in file_data:
                        if(singleData["date"]==date_ko):
                            singleData["brst"].extend(brsts)
                            singleData["lunc"].extend(luncc)
                            singleData["dinr"].extend(dinn)
                            singleData["cake"].extend(cake)
                            checkDuplicate=True
                            break
                    if not checkDuplicate:
                        file_data.append({'date':date_ko,'weekday':dateweekday,'brst':brsts,'lunc':luncc,'dinr':dinn,'cake':cake})
 
                    
    
    return {
        "body" : json.dumps(
             file_data
        ,ensure_ascii=False,indent="\t")
    }
