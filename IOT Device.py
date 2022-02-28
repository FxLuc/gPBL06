
import cv2
import threading
import requests
import time
import json
get_url='http://160.16.84.67:50667'
post_url='http://160.16.84.67:50667/item/delivery'
send_data={
    'id':'QRcode',
    'nowIn':'Japan'
    }
time_1 = time.time()
def getserver(url):
    x=requests.get(url)
    #print(x.text)
    push(x.text)

def push(data):
    if data=="ture":
        print('ture')
    elif data=="false":
        print('false')
    else:
        print(data)
def post(url,data):
    global time_1
    global requested
    if(time_2-time_1 >= 3):
        requested = (requests.post(url,data=data)).text
        #print(requested)
        json_request=json.loads(requested)
        #print(type(a))
        #print(requested.text)
        time_1=time.time()
        #return(requested.text)
        request_server(json_request)
    
def request_server(data):
    print("Conveyor belt is working ...")
    towhere = data["to"].split("_")
    #print(towhere)
    for i in range (len(towhere)):
        time.sleep(3)
        print("The package arrived in : "+towhere[i])
    #data_to()
    
#def data_to():
    
cap = cv2.VideoCapture(0)

detector = cv2.QRCodeDetector()

while True:
    
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    ###getserver(get_url)
    
    if(bbox is not None):
        
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 255), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if data:
            #print("data found: ", data)
            send_data['id']=data
            time_2 = time.time()
            post(post_url,send_data)
            #print('a1 is :'+a1.text)
            
    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        break
cap.release()
cv2.destroyAllWindows()
