# UART Tx/Rx demo
import tkinter as tk
from tkinter import ttk
import serial
import threading

# A simple Information Window that show a window when write wrong "COM"
class InformWindow:
    def __init__(self,informStr):
        self.window = tk.Tk()             # Create a tk window
        self.window.title("Information")  # Set the title of the window
        self.window.geometry("220x60")    # Set the size of the window
        self.window.configure(bg='seagreen1') # Set the background color of the window
        label = tk.Label(self.window,background="yellow2", text=informStr)
        buttonOK = tk.Button(self.window,background="yellow2",fg = "red",text="OK",command=self.ButtonOK)
        label.pack(side = tk.TOP)        # Place the label on the top of the window
        buttonOK.pack(side = tk.BOTTOM)  # Place the button on the bottom of the window
        self.window.mainloop()

    def ButtonOK(self):        # Process for the 'OK' button
        self.window.destroy()

class mainGUI:
    def __init__(self):
        window = tk.Tk()
        window.title(" GUI UART Tx/Rx ")
        window.configure(bg='blue')
        # Set the initial uart state to False
        self.uartState = False # is uart open or not

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tk.Frame(window)
        #frame_COMinf.configure(bg="black")
        frame_COMinf.grid(row = 1, column = 1)    # Place the frame on the second row, first column

        labelCOM = tk.Label(frame_COMinf,fg = "blue",text="COMx: ")
        self.COM = tk.StringVar(value = "COM4")       # Set the value of COM to 'COM4'
        ertryCOM = tk.Entry(frame_COMinf, textvariable = self.COM)
        labelCOM.grid(row = 1, column = 1, padx = 5, pady = 3)  # Place the label on the first row, first column, with a padding of 5 and 3
        ertryCOM.grid(row = 1, column = 2, padx = 5, pady = 3)  # Place the entry on the first row, second column, with a padding of 5 and 3

        labelBaudrate = tk.Label(frame_COMinf,fg = "blue",text="Baudrate: ")  # Create the label for Baudrate
        self.Baudrate = tk.IntVar(value = 9600)                               # Set the value of Baudrate to '9600'
        ertryBaudrate = tk.Entry(frame_COMinf, textvariable = self.Baudrate)
        labelBaudrate.grid(row = 1, column = 3, padx = 5, pady = 3)    # Place the label on the first row, third column, with a padding of 5 and 3
        ertryBaudrate.grid(row = 1, column = 4, padx = 5, pady = 3)    # Place the entry on the first row, fourth column, with a padding of 5 and 3

        labelParity = tk.Label(frame_COMinf,fg = "blue",text="Parity: ")
        self.Parity = tk.StringVar(value ="NONE")                         # Set the value of Parity to 'NONE'
        comboParity = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Parity)   # Create a combobox
        comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        comboParity["state"] = "readonly"   # Set the combobox to readonly
        labelParity.grid(row = 2, column = 1, padx = 5, pady = 3)
        comboParity.grid(row = 2, column = 2, padx = 5, pady = 3)

        labelStopbits = tk.Label(frame_COMinf,fg = "blue",text="Stopbits: ")    # Create the label for Stopbits
        self.Stopbits = tk.StringVar(value ="1")                                # Set the value of Stopbits to '1'
        comboStopbits = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1","2")
        comboStopbits["state"] = "readonly"
        labelStopbits.grid(row = 2, column = 3, padx = 5, pady = 3)
        comboStopbits.grid(row = 2, column = 4, padx = 5, pady = 3)
        
         # Create the Start/Stop button
        self.buttonSS = tk.Button(frame_COMinf, fg = "blue",text = "Start", command = self.processButtonSS)
        self.buttonSS.grid(row = 3, column = 4, padx = 5, pady = 3, sticky = tk.E)

        # serial object
        self.ser = serial.Serial()
        # Create a threading to read the serial
        self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        self.ReadUARTThread.start()   # Start the threading

        frameRecv = tk.Frame(window)    # Create a frame to contain the received data
        frameRecv.grid(row = 2, column = 1)   # Place the frame on the third row, first column
        labelOutText = tk.Label(frameRecv,fg = "blue",text="Received Data:")
        labelOutText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameRecvSon = tk.Frame(frameRecv)
        frameRecvSon.grid(row = 2, column =1)
        scrollbarRecv = tk.Scrollbar(frameRecvSon)  # Create a scrollbar
        scrollbarRecv.pack(side = tk.RIGHT, fill = tk.Y)  # Place the scrollbar on the right side, and fill up the Y axis
        # Create a textbox
        self.OutputText = tk.Text(frameRecvSon, wrap = tk.WORD, width = 60, height = 20, yscrollcommand = scrollbarRecv.set)
        self.OutputText.pack()

        # create a frame for transmit data
        frameTrans = tk.Frame(window)
        frameTrans.grid(row = 3, column = 1)
        labelInText = tk.Label(frameTrans,fg = "blue",text="To Transmit Data:")
        labelInText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameTransSon = tk.Frame(frameTrans)
        frameTransSon.grid(row = 2, column =1)
        scrollbarTrans = tk.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side = tk.RIGHT, fill = tk.Y)
        self.InputText = tk.Text(frameTransSon, wrap = tk.WORD, width = 60, height = 5, yscrollcommand = scrollbarTrans.set)
        self.InputText.pack()
        self.buttonSend = tk.Button(frameTrans,fg = "blue", text = "Send", command = self.processButtonSend)
        self.buttonSend.grid(row = 3, column = 1, padx = 5, pady = 3, sticky = tk.E)
        
        window.mainloop()

    def processButtonSS(self):
        # print(self.Parity.get())
        if (self.uartState):
            self.ser.close()
            self.buttonSS["text"] = "Start"
            self.uartState = False
        else:
            # restart serial port
            self.ser.port = self.COM.get()
            self.ser.baudrate = self.Baudrate.get()
            
            strParity = self.Parity.get()
            if (strParity=="NONE"):
                self.ser.parity = serial.PARITY_NONE
            elif(strParity=="ODD"):
                self.ser.parity = serial.PARITY_ODD
            elif(strParity=="EVEN"):
                self.ser.parity = serial.PARITY_EVEN
            elif(strParity=="MARK"):
                self.ser.parity = serial.PARITY_MARK
            elif(strParity=="SPACE"):
                self.ser.parity = serial.PARITY_SPACE
                
            strStopbits = self.Stopbits.get()
            if (strStopbits == "1"):
                self.ser.stopbits = serial.STOPBITS_ONE
            elif (strStopbits == "2"):
                self.ser.stopbits = serial.STOPBITS_TWO
            
            try:
                self.ser.open()
            except:
                infromStr = "Can't open "+self.ser.port
                InformWindow(infromStr)
            
            if (self.ser.isOpen()): # open success
                self.buttonSS["text"] = "Stop"
                self.uartState = True

    def processButtonSend(self):
        if (self.uartState):
            strToSend = self.InputText.get(1.0,tk.END)  # get data from text
            bytesToSend = strToSend[0:-1].encode(encoding='ascii') # encode data to bytes
            self.ser.write(bytesToSend)
            print(bytesToSend)
        else:
            infromStr = "Not In Connect!"
            InformWindow(infromStr)  # call a function to show the string

    def ReadUART(self):
        # print("Threading...")
        while True:
            if (self.uartState):
                try:
                    ch = self.ser.read().decode(encoding='ascii')
                    print(ch,end='')
                    self.OutputText.insert(tk.END,ch)
                except:
                    infromStr = "Something wrong in receiving."
                    InformWindow(infromStr)
                    self.ser.close() # close the serial when catch exception
                    self.buttonSS["text"] = "Start"
                    self.uartState = False
                    

mainGUI()

