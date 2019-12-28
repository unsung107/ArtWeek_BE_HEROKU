from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
import xml.etree.ElementTree as elemTree
from django.http import JsonResponse
from bs4 import BeautifulSoup
from decouple import config
from .models import *
from .serializers import *
import requests
import datetime

# Create your views here.
tables = {
    '오페라':'Classic',
    '클래식': 'Classic',
    '뮤지컬': 'Musical',
    '연극': 'Play',
    '복합':'Complex',
    '전시':'Exhibition',
    '콘서트': 'Concert'
}
genres = {
    'Musical' :Musical, 'Classic': Classic, 'Play' : Play, 'Complex' : Complex, 'Exhibition' : Exhibition, 'Concert' :Concert, 'Opera': Classic
}
def update(request, weeks):
    
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    afteryear = now + datetime.timedelta(weeks=weeks)
    afteryear = afteryear.strftime('%Y%m%d')


    KEY = config('KEY')
    base_url = 'http://kopis.or.kr/openApi/restful/'
    list_of_shows = f'{base_url}pblprfr?service={KEY}&stdate={nowDate}&eddate={afteryear}&cpage=1&rows=3000'
    response = requests.get(list_of_shows)
    result = response.text
    tree = elemTree.fromstring(result)
    ts = tree.findall('./db')
    today = str(datetime.date.today())
    cnt = 0
    for t in ts:
        try:
            eventID = t.find('mt20id').text
            type = t.find('genrenm').text
            show_url = f'{base_url}pblprfr/{eventID}?service={KEY}'
            detail_response = requests.get(show_url)
            detail_result = detail_response.text
            detail_tree = elemTree.fromstring(detail_result)
            detail_ts = detail_tree.find('./db')
            if tables.get(type) != None:
                table = tables[type]
            else:
                continue
            if table == 'Classic':
                temp = Classic()
                if Classic.objects.filter(eventID=f'{eventID}'):
                    temp = get_object_or_404(Classic, eventID = eventID)
                    temp.createdAt = now
                    temp.eventStatus = detail_ts.find('prfstate').text
                    temp.save()
                    print('넘어갑니다')
                    continue
            elif table == 'Musical':
                temp = Musical()
                if Musical.objects.filter(eventID=f'{eventID}'):
                    temp = get_object_or_404(Musical, eventID = eventID)
                    temp.createdAt = now
                    temp.eventStatus = detail_ts.find('prfstate').text
                    temp.save()
                    print('넘어갑니다')
                    continue
            elif table == 'Play':
                temp = Play()
                if Play.objects.filter(eventID=f'{eventID}'):
                    temp = get_object_or_404(Play, eventID = eventID)
                    temp.createdAt = now
                    temp.eventStatus = detail_ts.find('prfstate').text
                    temp.save()
                    print('넘어갑니다')
                    continue
            elif table == 'Complex':
                temp = Complex()
                if Complex.objects.filter(eventID=f'{eventID}'):
                    temp = get_object_or_404(Complex, eventID = eventID)
                    temp.createdAt = now
                    temp.eventStatus = detail_ts.find('prfstate').text
                    temp.save()
                    print('넘어갑니다')
                    continue
            elif table == 'Exhibition':
                temp = Exhibition()
                if Exhibition.objects.filter(eventID=f'{eventID}'):
                    temp = get_object_or_404(Exhibition, eventID = eventID)
                    temp.createdAt = now

                    temp.eventStatus = detail_ts.find('prfstate').text
                    temp.save()
                    print('넘어갑니다')
                    continue
            elif table == 'Concert':
                temp = Concert()
                if Concert.objects.filter(eventID=f'{eventID}'):
                    temp = get_object_or_404(Concert, eventID = eventID)
                    temp.createdAt = now
                    temp.eventStatus = detail_ts.find('prfstate').text
                    temp.save()
                    print('넘어갑니다')
                    continue
            title = t.find('prfnm').text
            temp.eventID = t.find('mt20id').text
            temp.title = t.find('prfnm').text
            temp.startDate = t.find('prfpdfrom').text.replace('.', '-')
            temp.endDate = t.find('prfpdto').text.replace('.', '-')
            temp.location = t.find('fcltynm').text
            temp.imgUrl = t.find('poster').text
            temp.type = t.find('genrenm').text
            temp.createdAt = now

            locationID = detail_ts.find('mt10id').text
            temp.locationID = detail_ts.find('mt10id').text
            temp.eventStatus = detail_ts.find('prfstate').text
            temp.performer = detail_ts.find('prfcast').text
            temp.director = detail_ts.find('prfcrew').text
            temp.fee = detail_ts.find('pcseguidance').text
            temp.age = detail_ts.find('prfage').text
            temp.timeTable = detail_ts.find('dtguidance').text

            place_url = f'{base_url}prfplc/{locationID}?service={KEY}'
            place_response = requests.get(place_url)
            place_result = place_response.text
            place_tree = elemTree.fromstring(place_result)
            place_ts = place_tree.find('./db')
            address = place_ts.find('adres').text
            temp.address = place_ts.find('adres').text
            if not ('인천' in address or '서울' in address or '경기' in address): 
                continue
            temp.latitude = place_ts.find('la').text
            temp.longitude = place_ts.find('lo').text
            

            t_url = f'http://www.kopis.or.kr/por/db/pblprfr/pblprfrView.do?menuId=MNU_00020&mt20Id={eventID}'
        
            ticketUrl = ''
            response = requests.get(t_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.select('.layerPopCon .btnType01 .btnType01_wrap a'):
                ticketUrl += link.get('href') + ','
            
            if ticketUrl:
                ticketUrl = list(ticketUrl)
                ticketUrl = ticketUrl[:-1]
                temp.ticketUrl = ''.join(ticketUrl)
            temp.save()
            cnt += 1
            print(title, address, type, temp.startDate, temp.endDate)
        except:
            print('error')
            continue

    KEY2 = config('KEY2')
    base_url = 'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/'
    list_of_shows = f'{base_url}realm?serviceKey={KEY2}&stdate={nowDate}&eddate={afteryear}&cpage=1&rows=3000&realmCode=D000'
    response = requests.get(list_of_shows)
    result = response.text
    tree = elemTree.fromstring(result)
    ts = tree.findall('./msgBody/perforList')

    for t in ts:
        try:
            temp = Exhibition()
            eventID = t.find('seq').text
            temp.eventID = t.find('seq').text
            startDate = t.find('startDate').text
            temp.startDate = datetime.date(int(startDate[:4]), int(startDate[4:6]), int(startDate[6:]))
            endDate = t.find('endDate').text
            temp.endDate = datetime.date(int(endDate[:4]), int(endDate[4:6]), int(endDate[6:]))
            if Exhibition.objects.filter(eventID=f'{eventID}'):
                temp = get_object_or_404(Exhibition, eventID = eventID)
                temp.createdAt = now
                temp.eventStatus = '전시 중' if (temp.startDate) < datetime.date.today() < (temp.endDate) else '전시 종료' if (temp.endDate) < datetime.date.today() else '전시 예정'
                temp.save()
                print('넘어갑니다')
                continue            
            temp.title = t.find('title').text
            temp.location = t.find('place').text
            temp.imgUrl = t.find('thumbnail').text
            temp.type = '전시'
            temp.createdAt = now

            show_url = f'{base_url}d/?seq={eventID}&serviceKey={KEY2}'

            detail_response = requests.get(show_url)
            detail_result = detail_response.text
            detail_tree = elemTree.fromstring(detail_result)
            detail_ts = detail_tree.find('./msgBody/perforInfo')
            address = detail_ts.find('placeAddr').text
            # print(address)
            temp.address = detail_ts.find('placeAddr').text
            if address != None and not ('인천' in temp.address or '서울' in temp.address or '경기' in temp.address): 
                continue
            if address == None:
                temp.address = ' '
            temp.eventStatus = '전시 중' if (temp.startDate) < datetime.date.today() < (temp.endDate) else '전시 종료' if (temp.endDate) < datetime.date.today() else '전시 예정'
            temp.performer = ' '
            temp.director = ' '
            temp.fee = detail_ts.find('price').text
            temp.age = ' '
            temp.timeTable = ' '
            temp.latitude = detail_ts.find('gpsX').text
            temp.longitude = detail_ts.find('gpsY').text
            temp.locationID = detail_ts.find('placeSeq').text
            temp.save()
            cnt += 1
            print(title, address, type)
        except:
            print('error')
            continue
    return JsonResponse({'cnt': cnt})


@api_view(['POST'])
def getArt(request):


    result = {}
    cnt = 0

    for genre, genreModel in genres.items():
        if request.data.get(genre) == None:
            continue
        for art in genreModel.objects.all():
            
            if genre == 'Musical':
                serializer = Musicalserializer(instance=art)            
            elif genre == 'Classic':
                serializer = Classicserializer(instance=art)  
            elif genre == 'Concert':
                serializer = Concertserializer(instance=art)  
            elif genre == 'Play':
                serializer = Playserializer(instance=art)  
            elif genre == 'Complex':
                serializer = Complexserializer(instance=art)  
            elif genre == 'Exhibition':
                serializer = Exhibitionserializer(instance=art)  
            temp = serializer.data.copy()
            flag = 0
            for key, value in request.data.items():
                if key in genres.keys():
                    continue
                if key == 'address':
                    if value not in temp["address"]:
                        flag = 1
                elif key == 'title':
                    if value not in temp["title"]:
                        flag = 1
                elif key == 'startDate':
                    if datetime.date(int(value[:4]), int(value[4:6]), int(value[6:])) > datetime.date(int(temp['endDate'][:4]), int(temp['endDate'][5:7]), int(temp["endDate"][8:])):
                        flag = 1
                        break
                elif key == 'endDate':
                    if datetime.date(int(value[:4]), int(value[4:6]), int(value[6:])) < datetime.date(int(temp['startDate'][:4]), int(temp['startDate'][5:7]), int(temp["startDate"][8:])):
                        flag = 1
                        break
                elif key == 'location':
                    if value not in temp["location"]:
                        flag = 1
                        break
                elif key == 'eventStatus':
                    if value not in temp["eventStatus"]:
                        flag = 1
                        break
                elif key == 'performer':
                    if value not in temp["performer"]:
                        flag = 1
                        break
                elif key == 'director':
                    if value not in temp["director"]:
                        flag = 1
                        break
                elif key == 'latitude':
                    if abs(int(value) - int(temp['latitude']) > 0.05):
                        flag = 1
                        break
                elif key == 'longitude':            
                    if abs(int(value) - int(temp['longitude']) > 0.05):
                        flag = 1
                        break
            if flag: continue
            temp["point"] = {}
            temp["point"]["point"] = {
                "latitude" : serializer.data["latitude"],
                "longitude" : serializer.data["longitude"]
            }
            result[cnt] = temp
            cnt += 1

    return JsonResponse(result)