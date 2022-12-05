import paho.mqtt.client as mqtt
import time

class 정보구독자:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self,client, userdata, flags, rc=0):
        print(str(rc))


    def on_subscribe(client, userdata, mid, granted_qos):
        print("subscribed: " + str(mid) + " " + str(granted_qos))
        
    def on_message(client, userdata, msg):
        구독정보 = msg.payload.decode("utf-8").split(",")
        날씨 = 날씨비교자(int(구독정보[1]),int(구독정보[2]),int(구독정보[3]),int(구독정보[4])).날씨비교()
        print(구독정보)
        
        

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.connect('mqtt.eclipseprojects.io', 1883)
    
    client.subscribe('common', 1)
    
    client.loop_forever()
    

class 날씨비교자:
    def __init__(self,설정온도,설정습도,지역온도,지역습도):
        self.설정온도 = 설정온도
        self.설정습도 = 설정습도
        self.지역온도 = 지역온도
        self.지역습도 = 지역습도
        

    def 날씨비교(self):
        if self.설정온도 == self.지역온도:
            온도 = 0
        elif self.설정온도 < self.지역온도:
            온도 = 1
        elif self.설정온도 > self.지역온도:
            온도 = 2

        if self.설정습도 == self.지역습도:
            습도 = 0
        elif self.설정습도 < self.지역습도:
            습도 = 1
        elif self.설정습도 > self.지역습도:
            습도 = 2
        
        실행자(온도,습도).실행()

class 실행자:
    def __init__(self,온도,습도):
        self.온도 = 온도
        self.습도 = 습도
        self.에어컨 = 0
        self.난방 = 0
        self.가습기 = 0
        self.제습기 = 0
    def 실행(self):
        if self.온도 == 0:
            print("현재온도 유지")
            print()
        elif self.온도 == 1:
            print("에어컨 가동")
            self.에어컨 = 1
            print()
        elif self.온도 == 2:
            print("난방 가동")
            self.난방 = 1
            print()

        if self.습도 == 0:
            print("현재습도 유지")
            print()
        elif self.습도 == 1:
            print("제습기 가동")
            print()
            self.제습기 = 1
        elif self.습도 == 2:
            print("가습기 가동")
            print()
            self.가습기 = 1

