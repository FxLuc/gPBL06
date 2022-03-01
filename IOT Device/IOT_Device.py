import cv2
import RPi.GPIO as GPIO
import threading
import requests
import time
import json
###LED pin setting
country_LED=[18,23]
taiwan_city_LED=[27,22,10]
vietnam_city_LED=[9,11,5]
country=["Taiwan","Vietnam"]
taiwan_city=["Taipei","Taichung","Tainan"]
vietnam_city=["DaNang","Hanoi","Haiphong"]
###

###setting LED output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for i in country_LED:
    GPIO.setup(i , GPIO.OUT)

for i in taiwan_city_LED:
    GPIO.setup(i , GPIO.OUT)

for i in vietnam_city_LED:
    GPIO.setup(i , GPIO.OUT)
###
    
### gpbl2206 ip and port
get_url='http://160.16.84.67:50667'
post_url='http://160.16.84.67:50667/item/delivery'
###

###Json data type send id and nowIn
send_data={
    'id':'QRcode',
    'nowIn':'Japan'
    }
###

### timer
time_1 = time.time()
###

def getserver(url):### use get function
    x=requests.get(url)
    push(x.text)

def push(data): ### get something do what
    if data=="ture":
        print('ture')
    elif data=="false":
        print('false')
    else:
        print(data)
                
def post(url,data):### send data to server
    global time_1
    global requested
    if(time_2-time_1 >= 3): ### time2 -time1 if equl 3
        requested = (requests.post(url,data=data)).text ### get requested text
        json_request = json.loads(requested) ### json 
        time_1=time.time() ### time reset
        request_server(json_request) ### another function doing LED part and send package
        
def request_server(data):
    print("Conveyor belt is working ...")
    towhere = data["to"].split("_") ###data type is country_city use split get 2 function
    for j in range(len(country_LED)):
        if (towhere[0]==country[j]):
            print("The package arrived in : "+towhere[0])
            GPIO.output(country_LED[j], 1)
            time.sleep(3)
            GPIO.output(country_LED[j], 0)
            
    if (towhere[0]=="Taiwan"):
        for j in range(len(taiwan_city_LED)):
            if (towhere[1]==taiwan_city[j]):
                print("The package arrived in : "+towhere[1])
                GPIO.output(taiwan_city_LED[j], 1)
                time.sleep(3)
                GPIO.output(taiwan_city_LED[j], 0)
                
    if (towhere[0]=="Vietnam"):
        for j in range(len(vietnam_city_LED)):
            if (towhere[1]==vietnam_city[j]):
                print("The package arrived in : "+towhere[1])
                GPIO.output(vietnam_city_LED[j], 1)
                time.sleep(3)
                GPIO.output(vietnam_city_LED[j], 0)
                
            
    
cap = cv2.VideoCapture(0)

detector = cv2.QRCodeDetector()

while True:
    
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)

    ### scan QRcode
    if(bbox is not None):
        
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 255), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if data:
            send_data['id']=data
            time_2 = time.time()
            post(post_url,send_data)
    
    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        break
cap.release()
cv2.destroyAllWindows()
