from tkinter import *
from tkinter.ttk import Combobox
from tkinter.scrolledtext import ScrolledText
from tkinter import IntVar, messagebox

import gpsdGPSListener
import serialGPSlistener
import webbrowser
import settings
import js8callAPIsupport

HEIGHT=650
WIDTH=500
gpsOption=""

MSG_ERROR='ERROR'
MSG_INFO='INFO'
MSG_WARN='WARN'

def callback(url):
    webbrowser.open_new(url)


class SettingsPage(Frame):
    def saveSettingsToFile(self, controller):
        
        print('AUTO ON START '+self.autoonstartcombo.get())
        yesno = self.autoonstartcombo.get()
        autoOnAtStart = 1
        if yesno=='No':
            autoOnAtStart=0
      
#        print('Auto On Start Option '+self.autodefaultcombo.get())
#        val = self.autoonstartcombo.get()
#        autoOption = 0
#        if val=='Auto TX Grid':
#            autoOption=1
 
        print('Default Auto Option '+self.autodefaultcombo.get())
        val = self.autodefaultcombo.get()
        autoOption = 0
        if val=='Auto TX Grid to APRSIS':
            autoOption=1
      
#      self.autodefaultcombo['values']= ("Auto update JS8Call Grid", "Auto TX Grid to APRSIS")
        print('Debug '+self.showdebugcombo.get())
        yesno = self.showdebugcombo.get()
        debug = 0
        if yesno=='Yes':
            debug=1
      
        settings.Settings().saveConfigFile(self.serverEntry.get(),
                                           self.serverPortEntry.get(),
                                           self.autotimeEntry.get(),
                                           autoOnAtStart,
                                           autoOption,
                                           self.maidPrecisionEntry.get(),
                                           self.comportEntry.get(),
                                           self.comportspeedEntry.get(),
                                           self.gpstypecombo.get(),
                                           debug)
        
        controller.refreshSettings()
        
        return 1
    
    def addY(self, y):
        return y+0.065
        
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
       
        self.controller = controller
        relh = 0.05
        fontsize=30
        
        y=0.14
        titleLabel = Label(self, font=12, text="Settings")
        titleLabel.place(relx=0.05, relwidth=0.9,relheight=0.10)
        
        serverLabel = Label(self, font=40, text="JS8Call Server IP")
        serverLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=0.08)
        
        self.serverEntry = Entry(self, font=40, textvariable=controller.serverVar, justify='center')
        self.serverEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        self.serverEntry.config(state=DISABLED)
        
        y=self.addY(y)
        
        ##############################################
        serverPortLabel = Label(self, font=fontsize, text="JS8Call UDP Port")
        serverPortLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        self.serverPortEntry = Entry(self, font=fontsize, textvariable=controller.serverPortVar, justify='center')
        self.serverPortEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        
        #############################################
        y=self.addY(y)
        
        gpstypecomboLabel = Label(self, font=fontsize, text="GPS Interface")
        gpstypecomboLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        type=0
        self.gpstypecombo = Combobox(self, state='readonly')
        #self.gpstypecombo.bind('<<ComboboxSelected>>', self.comboChange)    
        self.gpstypecombo['values']= ("None", "com port", "GPSD")
        if controller.gpsOption=="None":
            type = 0
        elif controller.gpsOption=="com port":
            type=1
        else:
            type=2
        self.gpstypecombo.current(type) #set the selected item
        self.gpstypecombo.place(relx=0.5, rely=y, relwidth=0.48, relheight=relh)
        ###################################################
        y=self.addY(y)

        comportLabel = Label(self, font=fontsize, text="GPS COM Port")
        comportLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        self.comportEntry = Entry(self, font=fontsize, textvariable=controller.gpsComPortVar, justify='center')
        self.comportEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        
        ##############################################
        y=self.addY(y)
        
        #############################################
        comportspeedLabel = Label(self, font=fontsize-10, text="GPS COM Port Speed")
        comportspeedLabel.place(relx=0.05, rely=y,relwidth=0.4,relheight=relh)
        
        self.comportspeedEntry = Entry(self, font=fontsize, textvariable=controller.gpsComPortSpeedVar, justify='center')
        self.comportspeedEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        
        ##############################################
        y = self.addY(y)
        
        maidPrecisionLabel = Label(self, font=fontsize, text="GPS Precision")
        maidPrecisionLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        self.maidPrecisionEntry = Entry(self, font=fontsize, textvariable=controller.maidPreceision, justify='center')
        self.maidPrecisionEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        
        ###############################################
        y=self.addY(y)

        autotimeLabel = Label(self, font=fontsize, text="Auto Time (mins)")
        autotimeLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        self.autotimeEntry = Entry(self, font=fontsize, textvariable=controller.autoTimeVar, justify='center')
        self.autotimeEntry.place(relx=0.5,rely=y, relwidth=0.48,relheight=relh)
        ###################################################
        
        y=self.addY(y)
        
        autoonstartLabel = Label(self, font=fontsize, text="Auto on Startup")
        autoonstartLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        
        self.autoonstartcombo = Combobox(self, state='readonly')
        #self.gpstypecombo.bind('<<ComboboxSelected>>', self.comboChange)    
        self.autoonstartcombo['values']= ("No", "Yes")
        self.autoonstartcombo.current(controller.autoatstart) #set the selected item
        self.autoonstartcombo.place(relx=0.5, rely=y, relwidth=0.48, relheight=relh)
        ###########################################################

        y=self.addY(y)
        
        autodefaultLabel = Label(self, font=fontsize, text="Default Auto Action")
        autodefaultLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        self.autodefaultcombo = Combobox(self, state='readonly')
        #self.gpstypecombo.bind('<<ComboboxSelected>>', self.comboChange)    
       # self.autodefaultcombo['values']= ("Auto Set Grid", "Auto TX Grid")
        self.autodefaultcombo['values']= ("Auto update JS8Call Grid", "Auto TX Grid to APRSIS")
 
        self.autodefaultcombo.current(controller.autooption) #set the selected item
        self.autodefaultcombo.place(relx=0.5, rely=y, relwidth=0.48, relheight=relh)
        ###########################################################
 
        y=self.addY(y)
        
        showdebugLabel = Label(self, font=fontsize, text="Show debug output")
        showdebugLabel.place(relx=0.05, rely=y,relwidth=0.3,relheight=relh)
        
        self.showdebugcombo = Combobox(self, state='readonly')
        #self.gpstypecombo.bind('<<ComboboxSelected>>', self.comboChange)    
        self.showdebugcombo['values']= ("No", "Yes")
        self.showdebugcombo.current(controller.showoutput) #set the selected item
        self.showdebugcombo.place(relx=0.5, rely=y, relwidth=0.48, relheight=relh)
        ###########################################################
        
        y=self.addY(y)
        
        self.saveButton = Button(self, text="Save", command=lambda:self.saveSettingsToFile(controller), bg="white", font=30)
        self.saveButton.place(relx=0.3,rely=y,relwidth=0.48,relheight=relh)
        
        aboutMeLabel = Label(self,text="http://m0iax.com/findme", font=30)
        aboutMeLabel.place(relx=0.05, rely=0.9,relwidth=0.9,relheight=0.10)
        aboutMeLabel.bind("<Button-1>", lambda e: callback("http://m0iax.com/findme"))

class GPSPage(Frame):

    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        
        self.controller = controller
        
        self.configure(bg="navy", bd=5)
        
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.latlonvar = StringVar()
        
        titleLabel = Label(self, font=12, text="Maidenhead Locator")
        titleLabel.place(relx=0.05, relwidth=0.9,relheight=0.10)
        
        gridrefEntry = Entry(self, font=40, textvariable=controller.var1, justify='center')
        gridrefEntry.place(rely=0.14, relwidth=0.48,relheight=0.14)
        
        getGridButton = Button(self, text="Get Grid from GPS", command=self.getGridRef, bg="white", font=30)
        getGridButton.place(relx=0.52,rely=0.14,relwidth=0.48,relheight=0.14)
        
        latlonEntry = Entry(self, font=40, textvariable=controller.latlonvar, justify='center')
        latlonEntry.place(rely=0.3, relwidth=0.48,relheight=0.10)
        
        self.latlonButton = Button(self, text="Lat Lon to Msg Text", command=lambda:controller.setMapLink, bg="white", font=30)
        self.latlonButton.place(relx=0.52,rely=0.3,relwidth=0.48,relheight=0.10)
        self.latlonButton.configure(state='disabled')
         
        self.setJS8CallGridButton = Button(self, text="Send Grid to JS8Call", command=lambda: controller.sendGridToJS8Call(gridrefEntry.get()), bg="white", font=40)
        self.setJS8CallGridButton.place(relx=0.02, rely=0.42,relwidth=0.45,relheight=0.2)
        self.setJS8CallGridButton.configure(state='disabled')
        
        self.sendJS8CallALLCALLButton = Button(self, text="TX Grid", command=lambda: controller.sendGridToALLCALL(gridrefEntry.get()), bg="white", font=50)
        self.sendJS8CallALLCALLButton.place(relx=0.55, rely=0.42,relwidth=0.44,relheight=0.2)
        self.sendJS8CallALLCALLButton.configure(state='disabled')
    
    def getGridRef(self):
        mh = self.controller.getGrid()
        
        if mh!= "No Fix" and mh!='JJ00aa00':
                self.setJS8CallGridButton.configure(state='normal')
                self.sendJS8CallALLCALLButton.configure(state='normal')
                self.latlonButton.configure(state='normal')
                #self.ngrStr.set(ngr)
        else:
                self.setJS8CallGridButton.configure(state='disabled')
                self.sendJS8CallALLCALLButton.configure(state='disabled')
                self.latlonButton.configure(state='normal')
#                self.ngrStr.set('No Fix')
#                self.var1.set('No Fix')
#                self.latlonvar.set('No Fix')
class MessagePage(Frame):
    def createMessageString(self):
        messageString=""
        mode=""
        if self.combo.get()=="Email":
            mode="EMAIL-2"
        elif self.combo.get()=="SMS":
            mode = "SMSGTE"
        elif self.combo.get()=="APRS":
            mode=self.combo.get()
           
        mode = mode.ljust(9)
        if self.tocall.get()=="":
            return "Error, no email address is set"
        
        text=self.st.get('1.0', 'end-1c')  # Get all text in widget.
    
        if text=="":
            return "Error, message is empty, please enter a message to send"
        
        number = self.controller.seq
        number = format(number, '02d')
        if self.combo.get()=="Email":
            message = "@APRSIS CMD :"+mode+":"+self.tocall.get()+" "+text+"{"+number+"}"
        elif self.combo.get()=="APRS":
            tocallsign=self.tocall.get()
            tocallsign=tocallsign.ljust(9)
            message = "@APRSIS CMD :"+tocallsign+":"+text+"{"+number+"}"
        else: 
            message = "@APRSIS CMD :"+mode+":@"+self.tocall.get()+" "+text+"{"+number+"}"
        
        self.controller.seq=self.controller.seq+1
        #APRS sequence number is 2 char, so reset if >99
        if self.controller.seq>99:
            self.controller.seq=1
        
        messageString = message #mode+" "+self.tocall.get()+" "+text
        return messageString

    def setAPRSMessage(self):
        messageType=js8callAPIsupport.TYPE_TX_SETMESSAGE
        
        messageString=self.createMessageString()
        
        if messageString.startswith("Error"):
            self.controller.showMessage(js8callAPIsupport.MSG_ERROR, messageString)
            return
    
        self.controller.sendMessage(messageType, messageString)
        
        self.controller.showMessage(js8callAPIsupport.MSG_INFO, "Message text set in JS8Call, please use JS8Call to send the message.")
            
    def txAPRSMessage(self):
        messageType=js8callAPIsupport.TYPE_TX_SEND
        messageString=self.createMessageString()
        
        if messageString.startswith("Error"):
            return
        
        self.controller.sendMessage(messageType, messageString)
        self.controller.showMessage(js8callAPIsupport.MSG_INFO,"Message sent to JS8Call. It will now transmit the message.")

    def comboChange(self, event):
        mode = self.combo.get()
        if mode=="APRS":
            self.callLbl.config(text='Enter Callsign (including SSID)')
        elif mode=="Email":
            self.callLbl.config(text='Enter Email Address to send to')
        elif mode=="SMS":
            self.callLbl.config(text='Enter cell phone number')
 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.controller=controller
        self.configure(bg="black", bd=5)
        ############################################################
        #                 APRS Messaging form                     #
        ############################################################

        #aprsFrame=tk.Frame(self.mainWindow, bg="black", bd=5)
        #aprsFrame.place(relx=0.5,rely=0.48, relwidth=0.95, relheight=0.4, anchor='n')

        self.aprstitleLabel = Label(self, font=10, text="APRS Messages")
        self.aprstitleLabel.place(relx=0.05, relwidth=0.9,relheight=0.1)
       
        self.aprstypelabel = Label(self, text="APRS Message Type", justify="left")
        self.aprstypelabel.place(relx=0.01, rely=0.14,relwidth=0.3, relheight=0.1)
 
        self.combo = Combobox(self, state='readonly')
        self.combo.bind('<<ComboboxSelected>>', self.comboChange)    
        self.combo['values']= ("Email", "SMS", "APRS")
        self.combo.current(0) #set the selected item
        self.combo.place(relx=0.42, rely=0.14, relwidth=0.3, relheight=0.1)
 
        self.lbl1 = Label(self, text="JS8Call Mode", justify="left")
        self.lbl1.place(relx=0.01, rely=0.27)
 
        self.combo2 = Combobox(self, state='readonly')
        self.combo2['values']= ("Normal")
        self.combo2.current(0) #set the selected item
        self.combo2.place(relx=0.42, rely=0.27, relwidth=0.3)
 
        self.callLbl = Label(self, text="Enter Email Address", justify="left")
        self.callLbl.place(relx=0.01, rely=0.41)
 
        self.tocall = Entry(self,width=37)
        self.tocall.place(relx=0.42, rely=0.41, relwidth=0.5)
 
        self.msgLabel = Label(self, text="Message Text", justify="left")
        self.msgLabel.place(relx=0.01, rely=0.56)
 
        self.st = ScrolledText(self, height=5)
        self.st.place(relx=0.35, rely=0.56, relwidth=0.6)

        self.btn = Button(self, text="Set JS8Call Text", command=self.setAPRSMessage, width=20)
        self.btn.place(relx=0.01, rely=0.69, relwidth=0.3)

        self.btn2 = Button(self, text="TX With JS8Call", command=self.txAPRSMessage, width=20)
        self.btn2.place(relx=0.01, rely=0.83, relwidth=0.3)
        
        self.note1label = Label(self, text="Click Set JS8Call text to set the message text in JS8Call", justify="center", wraplength=300)
        self.note1label = Label(self, text="Click TX with JS8Call to set the message text in JS8Call and start transmitting", justify="center", wraplength=300)

class App(Tk):
    def showMessage(self, messagetype, messageString):
        if messagetype==MSG_ERROR:
            messagebox.showerror("Error", messageString)
        elif messagetype==MSG_WARN:
            messagebox.showwarning("Warning",messageString)
        elif messagetype==MSG_INFO:
            messagebox.showinfo("Information",messageString)
    
    def sendMessage(self, messageType,messageText):
        self.api.sendMessage(messageType,messageText)
    
    def getGrid(self):
        if self.gpsl==None:
            print('GPS Listener not running. Update settings and try again.')
           # js8callAPIsupport.js8CallUDPAPICalls.showMessage(MSG_ERROR, getStatus()))
            self.showMessage('ERROR', 'GPS Listener not running. Update settings and try again.')
            return
        print('Getting Grid from GPS')
        gpsText = self.gpsl.getMaidenhead()
        print(gpsText)
        if gpsText==None:
            gpsText = "No Fix"
        
        ngr = self.gpsl.get_ngr()
        
        if gpsText!=None:
            if gpsText=='None':
                gpsText="No Fix"
                    #print("Got Grid "+gpsText)
            if ngr!=None:
                None
                #print("Got NGR "+ngr)
            
            latlon=''
        
            if self.gpsl.getStatus().startswith('Error'):
                self.gpsText=self.gpsl.getStatus()
                latlon=self.gpsl.getStatus()
            else:
                lat=self.gpsl.getCurrentLat()
                lon=self.gpsl.getCurrentLon()
        
            if lat!=None:
                latf = f"{lat:.5f}"
                lonf = f"{lon:.5f}"
                latlon=str(latf)+', '+str(lonf)
        
            self.var1.set(gpsText)
            self.latlonvar.set(latlon)        
        
#            if gpsText!= "No Fix" and gpsText!='JJ00aa00':
#                self.setJS8CallGridButton.configure(state='normal')
#                self.sendJS8CallALLCALLButton.configure(state='normal')
#                self.latlonButton.configure(state='normal')
                #self.ngrStr.set(ngr)
#            else:
#                self.setJS8CallGridButton.configure(state='disabled')
#                self.sendJS8CallALLCALLButton.configure(state='disabled')
#                self.latlonButton.configure(state='normal')
#                self.ngrStr.set('No Fix')
#                self.var1.set('No Fix')
#                self.latlonvar.set('No Fix')
            
            #if gpsText=='JJ00aa00':
                #self.ngrStr.set('No Fix')
    
#           return gpsText
   
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
    def nav_buttons(self, frame, controller):
        gps_page=Button(frame, text="GPS", command=lambda:controller.show_frame(GPSPage), bg="white", font=30, width=15)
        gps_page.grid(row=2, column=0)
        aprs_page=Button(frame, text="APRS Message", command=lambda:controller.show_frame(MessagePage), bg="white", font=30, width=15)
        aprs_page.grid(row=2, column=1)
        settings_page=Button(frame, text="Settings", command=lambda:controller.show_frame(SettingsPage), bg="white", font=30, width=15)
        settings_page.grid(row=2, column=2)
    
    def sendGridToALLCALL(self,gridText):
        self.api.sendGridToALLCALL(gridText, self.gpsl.getStatus())
    def sendGridToJS8Call(self, gridText):
        self.api.sendGridToJS8Call(gridText, self.gpsl.getStatus())
      
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Main Window is closing, call any function you'd like here!")

    def __enter__(self):
            # make a database connection and return it
        print('Starting')
    def ask_quit(self):
        if self.gpsl!=None:
            print('Shutting down GPS Listener')
            self.gpsl.setReadGPS(False)
            self.gpsl.join()
            
        print('Exiting. Thanks for using JS8CallUtils By M0IAX')
        self.destroy()  
    def update_timer(self):
        if self.autoGridToJS8Call.get()==0:
            self.initTimer()
            self.timerStr.set("Timer Not Active")
            
        if self.autoGridToJS8Call.get()==1:
            
            if self.timer<=0:
                self.initTimer()
            self.timer=self.timer-1
            t="Timer: " + str(self.timer)
            self.timerStr.set(t)
            
            if self.timer<=0:
                gridstr = self.getGrid()
                
                combotext=self.autocombo.get()

                if gridstr!=None and gridstr!='':
                    if combotext=="Auto update JS8Call Grid":
                        self.sendGridToJS8Call(gridstr)
                    if combotext=="Auto TX Grid to APRSIS":    
                        self.sendGridToALLCALL(gridstr)
                        
                self.initTimer()
        self.after(1000, self.update_timer)
    #def update_status_timer(self):
    #    self.mainWindow.after(10000, self.update_status_timer)

    def initTimer(self):
            self.timer=self.MAX_TIMER
    def autocomboChange(self, event):
        return ''
    def comboChange(self, event):
        mode = self.combo.get()
        if mode=="APRS":
            self.callLbl.config(text='Enter Callsign (including SSID)')
        elif mode=="Email":
            self.callLbl.config(text='Enter Email Address to send to')
        elif mode=="SMS":
            self.callLbl.config(text='Enter cell phone number')
    def cb(self):
        None
        #if self.autoGridToJS8Call.get()==0:
        #    self.autoGridToJS8Call.set(1)
        #else:
        #    self.autoGridToJS8Call.set(0)
        #    self.timerStr.set("Timer Not Active")

    def refreshSettings(self):
        self.settingValues = settings.Settings()

        self.showoutput = int(self.settingValues.getDebugSettingValue('showoutput'))
        
        self.timeinmins = int(self.settingValues.getAppSettingValue('autotimeperiod'))
        self.autoatstart = int(self.settingValues.getAppSettingValue('autoonatstart'))
        self.autooption = int(self.settingValues.getAppSettingValue('autoselectedoption'))

        self.MAX_TIMER=self.timeinmins*60    
    
        self.serverPortVar = StringVar()
        self.serverVar = IntVar()
        
        self.serverPortVar.set(int(self.settingValues.getNetworkSettingValue('serverport')))
        self.serverVar.set(self.settingValues.getNetworkSettingValue('serverip'))
        
        self.gpsOption = self.settingValues.getGPSHardwareSettingValue('option')
    
        self.gpsComPortVar = StringVar()
        self.gpsComPortSpeedVar = StringVar()
        
        self.gpsComPortVar.set(self.settingValues.getGPSHardwareSettingValue('gpscomport'))
        self.gpsComPortSpeedVar.set(self.settingValues.getGPSHardwareSettingValue('gpsportspeed'))
        self.maidPreceision.set(self.settingValues.getAppSettingValue('precision'))
        self.autoTimeVar.set(self.settingValues.getAppSettingValue('autotimeperiod'))
        self.autoGridToJS8Call.set(self.settingValues.getAppSettingValue('autoonatstart'))
        
        if self.gpsOptionBeforeRefresh!=self.gpsOption:
            if self.gpsl!=None:
                print('Shutting down GPS Listener')
                #self.gpsl.destroy()
                self.gpsl.setReadGPS(False)
                self.gpsl.join()
                self.gpsl=None
            if self.gpsOption!='None':
                print('Starting GPS Listener')
                if self.gpsOption=='gpsd':
                    self.gpsl = gpsdGPSListener.GpsListener()
                else:
                    print('Runnig serial gps again')
                    self.gpsl = serialGPSlistener.GPSListener(self.settingValues.getGPSHardwareSettingValue('gpscomport'),
                                                            self.settingValues.getGPSHardwareSettingValue('gpsportspeed'),
                                                            self.settingValues.getAppSettingValue('precision'),
                                                            self.showoutput
                                                            )
                self.gpsl.start()
            else:
                print('Setting thread to None')
                self.gpsl=None    
        self.gpsOptionBeforeRefresh=self.gpsOption
            

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.seq=1
        
        self.settingValues = settings.Settings()
        
        self.showoutput = int(self.settingValues.getDebugSettingValue('showoutput'))
        
        self.timeinmins = int(self.settingValues.getAppSettingValue('autotimeperiod'))
        self.autoatstart = int(self.settingValues.getAppSettingValue('autoonatstart'))
        self.autooption = int(self.settingValues.getAppSettingValue('autoselectedoption'))

        self.MAX_TIMER=self.timeinmins*60    
    
        self.serverPortVar = StringVar()
        self.serverVar = IntVar()
        
        self.serverPortVar.set(int(self.settingValues.getNetworkSettingValue('serverport')))
        self.serverVar.set(self.settingValues.getNetworkSettingValue('serverip'))
        
        self.api = js8callAPIsupport.js8CallUDPAPICalls(self.settingValues.getNetworkSettingValue('serverip'),
                                                        int(self.settingValues.getNetworkSettingValue('serverport')))
        
        self.gpsOption = self.settingValues.getGPSHardwareSettingValue('option')
    
        self.gpsComPortVar = StringVar()
        self.gpsComPortSpeedVar = StringVar()
        
        self.gpsComPortSpeedVar = self.settingValues.getGPSHardwareSettingValue('gpsportspeed')
        self.gpsComPortVar = self.settingValues.getGPSHardwareSettingValue('gpscomport') 
        
        self.gpsOptionBeforeRefresh = self.gpsOption
        
        self.gpsl=None
        
        if self.gpsOption!="None":
            if self.gpsOption=='gpsd':
                self.gpsl = gpsdGPSListener.GpsListener()
            else:
                self.gpsl = serialGPSlistener.GPSListener(self.settingValues.getGPSHardwareSettingValue('gpscomport'),
                                                        self.settingValues.getGPSHardwareSettingValue('gpsportspeed'),
                                                        self.settingValues.getAppSettingValue('precision'),
                                                        self.showoutput
                                                        )
        
            self.gpsl.start()

        self.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.title("JS8Call Utilities by M0IAX")
        
        self.gpsComPortVar = StringVar()
        self.gpsComPortSpeedVar = StringVar()
        self.maidPreceision = StringVar()
        self.autoTimeVar = StringVar()
        self.autoGridToJS8Call = IntVar()
        
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.latlonvar = StringVar()
        
        #set default values
        self.gpsComPortVar.set(self.settingValues.getGPSHardwareSettingValue('gpscomport'))
        self.gpsComPortSpeedVar.set(self.settingValues.getGPSHardwareSettingValue('gpsportspeed'))
        self.maidPreceision.set(self.settingValues.getAppSettingValue('precision'))
        self.autoTimeVar.set(self.settingValues.getAppSettingValue('autotimeperiod'))
        self.autoGridToJS8Call.set(self.settingValues.getAppSettingValue('autoonatstart'))
        
        #Main window frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (GPSPage, MessagePage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        self.show_frame(GPSPage)

        bottomFrame=Frame(self)
        bottomFrame.pack()
                
        self.autocombo = Combobox(bottomFrame, state='readonly',width=25)
        self.autocombo.state='disabled'
        self.autocombo.bind('<<ComboboxSelected>>', self.autocomboChange)    
        self.autocombo['values']= ("Auto update JS8Call Grid", "Auto TX Grid to APRSIS")
 
        self.autocombo.current(self.autooption) #set the selected item
        #self.autocombo.place(relx=0.05,rely=0.63, relwidth=0.9,relheight=0.1)
        self.autocombo.grid(row=0, column=0)
    
        self.autoGridToJS8Call = IntVar(value=self.autoatstart)
        self.autoGridCheck = Checkbutton(bottomFrame, text="Enable Auto update every "+str(self.timeinmins)+" mins.", variable=self.autoGridToJS8Call, command=self.cb)
        #self.autoGridCheck.place(relx=0.05,rely=0.71, relwidth=0.9,relheight=0.1)
        self.autoGridCheck.grid(row=1, column=0)
        
        self.timer=60 #Set timer to 60 for the first tx GPS should have a lock in that time
        self.timerStr = StringVar()
        
        self.timerStr.set("Timer Not Active")
        self.timerlabel = Label(bottomFrame, textvariable=self.timerStr )
        #self.timerlabel.place(relx=0.05,rely=0.81, relwidth=0.9,relheight=0.1)
        self.timerlabel.grid(row=2, column=0)
    
        buttonFrame=Frame(self)
        buttonFrame.pack()
        
        self.nav_buttons(buttonFrame, self)
        
        self.update_timer()
        #self.update_status_timer()
        
    
try:

    app = App()
    app.protocol("WM_DELETE_WINDOW", app.ask_quit)
    app.mainloop()
    
    
  #  app.gpsl.setReadGPS(False)
    
finally:
    print('Finally Quit')
   # if app.gpsl!=None:
   #     app.gpsl.setReadGPS(False)
   #     app.gpsl.join()
        