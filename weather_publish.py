from bs4 import BeautifulSoup
import requests
import paho.mqtt.client as mqtt
import time
import re

class 설정자:
    def __init__(self,지역,온도,습도):
        self.지역 = 지역
        self.온도 = 온도
        self.습도 = 습도
    def 설정내용저장(self):
        print("현재 설정된 지역은 : {}\n현재 설정된 온도는 : {}\n현재 설정된 습도는 : {}".format(self.지역,self.온도,self.습도))
        return 날씨검색자(self.지역).설정지역()
    
        
class 날씨검색자:
    def __init__(self,지역):
        self.지역 = 지역
    def 설정지역(self):
        검색자 = self.지역 + '날씨'
        html = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + 검색자)
        soup = BeautifulSoup(html.text, 'html.parser')
        weather = soup.find('div', {'class':'status_wrap'})
        temp_str = str(weather.find('strong').get_text())
        water_str = str(weather.find('dl',{'class':'summary_list'}).get_text())
        temp = re.findall("-?\d+", temp_str)
        water = re.findall("-?\d+", water_str)
        return temp[0],water[1]
        
class 정보전달자:
    def __init__(self,설정지역,설정온도,설정습도,지역온도,지역습도):
        self.설정지역 = 설정지역
        self.설정온도 = 설정온도
        self.설정습도 = 설정습도
        self.지역온도 = 지역온도
        self.지역습도 = 지역습도

    def 정보게시(self):

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("connected OK")
            else:
                print("Bad connection Returned code=", rc)

        def on_disconnect(client, userdata, flags, rc=0):
            print(str(rc))

        def on_publish(client, userdata, mid):
            print("In on_pub callback mid= ", mid)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish

        전달정보 = self.설정지역 +","+ self.설정온도 +","+ self.설정습도 +","+ self.지역온도 +","+ self.지역습도
        client.connect('mqtt.eclipseprojects.io', 1883)
        client.loop_start()

        client.publish('common',전달정보, 1)
        print(전달정보)
        client.loop_stop()

        client.disconnect()
        

지역 = input("지역을 설정해주십시오 : ")
온도 = input("온도를 설정해주십시오 : ")
습도 = input("습도를 설정해주십시오 : ")
설정 = 설정자(지역,온도,습도)
날씨 = 설정.설정내용저장()
정보전달 = 정보전달자(지역, 온도, 습도, 날씨[0], 날씨[1])
while True:
    정보전달.정보게시()
    time.sleep(2)