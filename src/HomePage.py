import os
import sys
import cPickle
import re

from Tkinter import*
from tkMessageBox import*
from tkFileDialog import askopenfilename,asksaveasfilename
import Pmw

Pmw.initialise()
import math
from MathUtils import*
from PlatformUtils import * 

from TransitionPiecePageClass import * 
from InterpenetrationPiecePageClass import * 


class HomeScreen(Frame):
    def __init__(self):
        Frame.__init__(self)

        try:
            self.master.state(GetZoomedStateOption(sys.platform))
        except Exception:
            pass 
           

        self.master.protocol("WM_DELETE_WINDOW", self.CloseHomeScreen)
        self.master.title("SHEET METAL WORK")
        self.master.rowconfigure(0,weight = 1)
        #
        # Load Icon bitmap. 
        if 'win' in sys.platform :
            try:
                self.master.wm_iconbitmap(os.path.join('SubFiles2','Icon.ico'))
            except Exception as message:
                pass

        elif 'linux' in sys.platform: 
            try:
                self.linux_bitmap  = PhotoImage(file = os.path.join("SubFiles","interfile1.tx"))
                self.master.tk.call('wm','iconphoto',self.master._w,self.linux_bitmap)
            except Exception as message:
                pass #print("Could not load bitmap on linux system : ",message)
        else:
            pass          
        # Setup the default filepth folder  
        try:
            b = os.getcwd()
            defaultfilepath = os.path.join(b, "SheetMetalWork")
            if not os.path.isdir(defaultfilepath):
            	os.mkdir(defaultfilepath)
        except Exception:
            pass
        
        self.master.columnconfigure(0,weight = 1)
        self.grid(sticky = W+E+N+S, row = 0, column = 0)
        self.wtext = "Chondochol Design"
        self.columnconfigure(0,weight = 1)

        self.transitionpiecepage =\
                            TransitionPiecePage(self)
        self.interpenetrationpage = InterpenetrationPiecePage(self)

        self.countinterpenetration = 0
        self.counttransition = 0
        

        self.rowconfigure(0,weight = 1)
        self.rowconfigure(2,weight = 1)

        self.frame1 = Frame(self)
        self.frame1.grid(sticky = W+E+N+S, row = 0,column = 0)
        self.frame1.rowconfigure(0,weight = 1)
        self.frame1.rowconfigure(1,weight = 1)
        self.frame1.columnconfigure(0,weight = 1)
        self.frame1.columnconfigure(1,weight = 1)

        self.frame2 = Frame(self)
        self.frame2.grid(sticky = N+W+E, row = 2, column = 0)
        self.frame2.rowconfigure(0,weight = 1)
        self.frame2.columnconfigure(0,weight = 1)
        self.frame2.columnconfigure(1,weight = 1)
        

        try:
            self.inter_file1 = PhotoImage(file = os.path.join("SubFiles","interfile1.tx"))
            self.trans_file1 = PhotoImage(file = os.path.join("SubFiles","transfile1.tx"))
        except Exception:
            self.button1 = Button(self.frame1,\
                                  text = "Interpenetration Piece",\
                                  command = self.StartInterpenetration)
            self.button2 = Button(self.frame1,\
                            text = "Transition Piece", command = self.StartTransitionPiece)

        else:

            self.button1 = Button(self.frame1,\
                                  image = self.inter_file1,\
                                  command = self.StartInterpenetration)

            self.button2 = Button(self.frame1,\
                               image = self.trans_file1, command = self.StartTransitionPiece)

        self.labelbutton1 = Label(self.frame1,text = "INTERPENETRATION PIECE",\
                                  font = "Arial 15 bold")
        self.labelbutton1.grid(sticky = W+E, row = 1,column = 0)
            
        self.labelbutton2 = Label(self.frame1,text = "TRANSITION PIECE", font = "Arial 15 bold")
        self.labelbutton2.grid(sticky = W+E, row = 1,column = 1)
       
        self.button1.grid(sticky = W+E+N+S, row = 0, column = 0,padx = 20)

        self.button2.grid(sticky = W+E+N+S, row = 0,column = 1,padx = 20)

        self.label = Label(self.frame2,text = "Dr. S. Gbeminiyi", font = "Arial 10 ")
        self.label.grid(sticky = NW, row = 0,column = 0)
        try:
            self.logofile = PhotoImage(file = os.path.join("SubFiles","transfile2.tx"))
        except Exception,message:
            self.labellogo = Label(self.frame2,text = self.wtext , font = "Arial 7 ")
            

        else:
            self.labellogo = Label(self.frame2,image = self.logofile)
            
        self.labellogo.grid(sticky = NE, row = 0,column = 1)

    def StartInterpenetration(self):

        self.countinterpenetration +=1
        if self.countinterpenetration == 1:
            self.interpenetrationpage.CreateWindow()

        else:
            self.interpenetrationpage.Lift()

    def StartTransitionPiece(self):
        self.counttransition +=1
        if self.counttransition == 1:
            self.transitionpiecepage.CreateWindow()
        else:
            self.transitionpiecepage.Lift()

    def Lower0(self):
        self.transitionpiecepage.Lower()
    def Lower1(self):
        self.interpenetrationpage.Lower()

    def CloseHomeScreen(self):
        if self.transitionpiecepage.AnyProject():
            answer = askyesnocancel("Quit","You Have Active Projects.\nDo you want to quit Anyway?")
        else:
            answer = 1
        if answer:
            self.master.destroy()

    def OpenOption(self,classname,fileobj):
        if classname == "Transition Piece":
            self.transitionpiecepage.ReceiveDataToOpen(fileobj)
        elif classname == "Interpenetration Piece":
            self.interpenetrationpage.ReceiveDataToOpen(fileobj)
        else:
            pass

    def ShowNext(self):
        self.rectpage.CreateWindow()

    def InitializeCount1(self):
        self.counttransition = 0
    def InitializeCount2(self):
        self.countinterpenetration = 0


        
