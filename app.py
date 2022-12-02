import random
from kivy.lang import Builder
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib import use as mpl_use
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import kivy.properties as kp
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
import datetime as dt
import asyncio
from bleak import BleakClient

#list to store readings
y=[]

address='3775D9A2-99DD-C7C1-1AD5-6427D72B88B0'
uuid_char='00002101-0000-1000-8000-00805f9b34fb'

client=BleakClient(address)
 
class TestApp(App):
    def build(self):
        return Chart()
 
 
class Chart(BoxLayout):
 
    data = kp.ListProperty([])
   
 
    def __init__(self, **kwargs):
 
        super().__init__(**kwargs)
        self.fig, self.ax1 = plt.subplots()
        self.ax1.plot([], [], 'bo')
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        Clock.schedule_interval(self.update, 1/60)
    

    async def get_reading(self,*args):
        await client.connect()
        reading = await client.read_gatt_char(uuid_char)
        y.append(int.from_bytes(reading,byteorder='little'))
     
 
    def on_data(self, *args):

        self.ax1.clear()
        plt.title('ECG Measure over Time')
        plt.xlabel('Time')
        plt.ylabel('uV')
        
    
        #get reading
        asyncio.get_event_loop().run_until_complete(self.get_reading())
        


        if len(y)>20:
            y.pop(0)
        if len(self.data)>20:
            self.data.pop(0)

        self.ax1.plot(self.data, y, 'bo-', linewidth=5.0)
        self.fig.canvas.draw_idle()
 
    def update(self, *args): 
        self.data.append(dt.datetime.now())
        
             
 
if __name__ == '__main__':
    TestApp().run()
