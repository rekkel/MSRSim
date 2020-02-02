from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import StringVar
from tkinter import Scale
import paho.mqtt.client as mqtt
import time

topic = "channels/7011886/data"
#mosquitto_sub -t "channels/7011886/data" -u "fpl" -P "1234567890"

#hostMQTT="192.168.2.15"

hostMQTT="192.168.1.135"
DEBUG = False

overzetverhouding_trafo = 10000 / 400


class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget


def end_prog():
    if (DEBUG): print("End Program")
    quit()

def on_connect(mqttc, obj, flags, rc):
	if (rc == 0):
		if (DEBUG): print("Connect to MQTT broker")

def on_disconnect(mqttc, obj, rc):
	if (rc == 1):
		connect_to_MQTT()
	if (DEBUG): print("rc="+ str(rc))

def on_publish(mqttc, obj, mid):
    if (DEBUG): print("mid: " + str(mid))
    pass

def on_subscribe(mqttc, obj, mid, granted_qos):
    if (DEBUG): print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    if (DEBUG): print(string)

def connect_to_MQTT():
	mqttConnect = 1
	while mqttConnect > 0:
		mqttConnect = mqttc.connect(hostMQTT, 1883, 60)
		if (DEBUG): print("Cannot connect to MQTT broker")
		time.sleep(5)
	return mqttConnect

def on_message(mqttc, obj, msg):
    if (DEBUG): print(str(msg.payload))
    trafo = ""
    procent = ""
    values = []
    payload = ""
    
    payload = str(msg.payload)[2:-1]
    values = payload.split(";")
    
    if (DEBUG): print(values)
    if (DEBUG): print(len(values))
    
    if (len(values) == 3):
        for index, value in enumerate(values):
            if (DEBUG): print( value )
            if (index == 1):
                trafo = value
            if (index == 2):
                procent = value

        update_trafo(trafo, procent)


mqttc = mqtt.Client()
mqttc.username_pw_set("fpl", password="1234567890")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log

is_mqttConnect = connect_to_MQTT()

mqttc.subscribe("channels/#", 0)

mqttc.loop_start()
#mqttc.loop_forever()


def send_value():
    if (DEBUG): print (scale1.get())
    toBroker =  "7011886;" + str(scale1.get()) + ";"  + str(scale2.get()) + ";"  + str(scale3.get()) + ";"  + str(scale4.get()) + ";"  + str(scale5.get()) + ";"  + str(scale6.get()) + ";" + str(var7.get())
    if (DEBUG): print(toBroker)
    if (is_mqttConnect == 0) :
        (rc, mid) = mqttc.publish(topic, toBroker, qos=2)
    else :
        if (DEBUG): print("MQTT error")
    
    button2['bg'] = 'lightgrey'


def update_10kV_stroom():
    var7.set( round(  ( scale1.get() + 
                        scale4.get() + 
                        scale2.get() + 
                        scale5.get() + 
                        scale3.get() + 
                        scale6.get() 
                      ) / 6 / overzetverhouding_trafo ,1 ))

def update_trafo(kva, procent):
    var8.set( kva)
    var9.set( procent)



def updateVal(val):
    var1.set(scale1.get())
    var2.set(scale2.get())
    var3.set(scale3.get())
    var4.set(scale4.get())
    var5.set(scale5.get())
    var6.set(scale6.get())
    button2['bg'] = 'yellow'
    update_10kV_stroom()
    


if __name__ == '__main__':

    IMAGE_PATH = 'MSR1.png'
    WIDTH, HEIGTH = 800,480
    FULLSCREEN = False
    
    root = tk.Tk()
    root.geometry('{}x{}'.format(WIDTH, HEIGTH))
    root.title("MSR Simulator")
    root.attributes('-fullscreen', FULLSCREEN)

    bkrgframe = BkgrFrame(root, IMAGE_PATH, WIDTH, HEIGTH)
    bkrgframe.pack()

    

    var1  = StringVar()
    var2  = StringVar()
    var3  = StringVar()
    var4  = StringVar()
    var5  = StringVar()
    var6  = StringVar()
    
    var7  = StringVar()
    var8  = StringVar()
    var9  = StringVar()
    
    OFFSET_SLIDER = 550


    # Put some tkinter widgets in the BkgrFrame.
    scale1 = bkrgframe.add(tk.Scale(root, from_=-20, to=125, orient=HORIZONTAL, command=updateVal, highlightbackground='black', fg='white',bg='black', width=8, length=170, showvalue=0 ), OFFSET_SLIDER , 150)
    scale2 = bkrgframe.add(tk.Scale(root, from_=-20, to=125, orient=HORIZONTAL, command=updateVal, highlightbackground='black', fg='white',bg='black', width=8, length=170, showvalue=0 ), OFFSET_SLIDER , 170)
    scale3 = bkrgframe.add(tk.Scale(root, from_=-20, to=125, orient=HORIZONTAL, command=updateVal, highlightbackground='black', fg='white',bg='black', width=8, length=170, showvalue=0 ), OFFSET_SLIDER , 190)
    scale4 = bkrgframe.add(tk.Scale(root, from_=-20, to=125, orient=HORIZONTAL, command=updateVal, highlightbackground='black', fg='white',bg='black', width=8, length=170, showvalue=0 ), OFFSET_SLIDER , 340)
    scale5 = bkrgframe.add(tk.Scale(root, from_=-20, to=125, orient=HORIZONTAL, command=updateVal, highlightbackground='black', fg='white',bg='black', width=8, length=170, showvalue=0 ), OFFSET_SLIDER , 360)
    scale6 = bkrgframe.add(tk.Scale(root, from_=-20, to=125, orient=HORIZONTAL, command=updateVal, highlightbackground='black', fg='white',bg='black', width=8, length=170, showvalue=0 ), OFFSET_SLIDER , 380)
    
    scale1.set(65)
    scale2.set(65)
    scale3.set(65)
    scale4.set(65)
    scale5.set(65)
    scale6.set(65)

   
    label1  = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="L1"), OFFSET_SLIDER - 25 , 147)
    label2  = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="L2"), OFFSET_SLIDER - 25 , 167)
    label3  = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="L3"), OFFSET_SLIDER - 25 , 187)
    label4  = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="L1"), OFFSET_SLIDER - 25 , 337)
    label5  = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="L2"), OFFSET_SLIDER - 25 , 357)
    label6  = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="L3"), OFFSET_SLIDER - 25 , 377)
    
    label7  = bkrgframe.add(tk.Label(root, textvariable=var1, fg='white',bg='black', text="65"), OFFSET_SLIDER + 180 , 147)
    label8  = bkrgframe.add(tk.Label(root, textvariable=var2, fg='white',bg='black', text="65"), OFFSET_SLIDER + 180 , 167)
    label9  = bkrgframe.add(tk.Label(root, textvariable=var3, fg='white',bg='black', text="65"), OFFSET_SLIDER + 180 , 187)
    label10 = bkrgframe.add(tk.Label(root, textvariable=var4, fg='white',bg='black', text="65"), OFFSET_SLIDER + 180 , 337)
    label11 = bkrgframe.add(tk.Label(root, textvariable=var5, fg='white',bg='black', text="65"), OFFSET_SLIDER + 180 , 357)
    label12 = bkrgframe.add(tk.Label(root, textvariable=var6, fg='white',bg='black', text="65"), OFFSET_SLIDER + 180 , 377)

    label13 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER + 210 , 147)
    label14 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER + 210 , 167)
    label15 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER + 210 , 187)
    label16 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER + 210 , 337)
    label17 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER + 210 , 357)
    label18 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER + 210 , 377)

    label19 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="A"), OFFSET_SLIDER - 220 , 320)
    I_10kV  = bkrgframe.add(tk.Label(root, textvariable=var7, fg='white',bg='black', text="0"), OFFSET_SLIDER - 240 , 320)
 
    label20 = bkrgframe.add(tk.Label(root, textvariable=var8, fg='white',bg='black', text="400", font=("Helvetica", 16)), OFFSET_SLIDER - 240 , 190)
    label21 = bkrgframe.add(tk.Label(root, textvariable=var9, fg='white',bg='black', text="50", font=("Helvetica", 16)), OFFSET_SLIDER - 240 , 220)
    label20 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="KVA", font=("Helvetica", 16)), OFFSET_SLIDER - 200 , 190)
    label21 = bkrgframe.add(tk.Label(root, fg='white',bg='black', text="%", font=("Helvetica", 16)), OFFSET_SLIDER - 200 , 220)
 
    button1 = bkrgframe.add(tk.Button(root, text="Exit", command=end_prog ), 10, 10)
    button2 = bkrgframe.add(tk.Button(root, text="Send", command=send_value ),  470, 410)

    update_10kV_stroom()
    
    update_trafo("400","100")

    root.mainloop()
