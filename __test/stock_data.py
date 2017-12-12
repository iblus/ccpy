import sys
import os
import time
import math
import threading
import xpinyin

from tkinter import *
import tkinter.messagebox as messagebox

from pprint import pprint
import msvcrt

import ystockquote
import stockquote
from pip._vendor.distlib.compat import raw_input
from tkinter import *
import tkinter.messagebox as messagebox

import tushare as ts

stockListTmp = []
class Th2(threading.Thread):
    def __init__(self, func, args='', name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        
    def gerResult(self):
        return self.res
    
    def run(self):
        print('starting ',self.name, 'at:', time.ctime())
        self.res = self.func()



class GuiApplication(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.list = ''
        
        dd = ystockquote.getStockList('list.txt')
        aa = sorted(dd.keys())
        self.stock = dict()
        self.stockPY = dict()
        p = xpinyin.Pinyin()
        for i in aa:
            self.stock[i[2:8]] = dd[i]
            self.stockPY[i[2:8]] = p.get_initials(dd[i], '')
        self.createWidgets()
    def quit(self):
        self.destroy()
        self.quit()
        
    def getStockList(self,tmm):
        self.nameListInput.delete(0, END)
#         if tmm == ' ':
#             for i in sorted(self.stock.keys()):
#                 tt = str(i)+'  '+str(self.stock[i])
#                 self.nameListInput.insert(END,tt)
#         elif tmm.isdigit():
#             for i in sorted(self.stock.keys()):
#                 if i.find(tmm) != -1:
#                     tt = str(i)+'  '+str(self.stock[i])
#                     self.nameListInput.insert(END,tt)
#             
#         else:
#             for i in sorted(self.stockPY.keys()):
#                 stt = tmm.upper()
# #                 stt = tmm.lower()
#                 if self.stockPY[i].find(stt) != -1:
#                     tt = str(i)+'  '+str(self.stock[i])
#                     self.nameListInput.insert(END,tt)
                
        keys = [x[0] for x in self.stockPY.items() if ((x[0].find(tmm)!=-1) or (x[1].find(tmm.upper())!=-1))]
        for i in sorted(keys):
            tt = str(i) + ' ' + str(self.stock[i])
            self.nameListInput.insert(END, tt)
        return keys
    def printGetList(self, event):
        global stockListTmp
        a= self.nameListInput.curselection()
        tt = self.nameListInput.get(a)[0:6]
        if not tt in stockListTmp:
            stockListTmp.append(tt)
        
               
    def createWidgets(self):
        try:
            self.nameInput = Entry(self)
            self.nameInput.focus()
            
            self.nameInput.bind('<KeyRelease>', self.hello)
            self.nameInput.pack()
            
            self.nameListInput = Listbox(self)
            self.nameListInput.bind('<Double-Button-1>',self.printGetList)
            self.getStockList(' ')
            
            self.nameListInput.pack()
            
    #         self.alertButton = Button(self, text='OK', command=self.hello)
            self.alertButton2 = Button(self, text='Clear', command=self.clear)
            self.alertButton2.pack(side=RIGHT)
    #         self.alertButton.pack(side=LEFT)
        except Exception as err:
            print(str(err))
        

    def hello(self,event):
        global stockListTmp
        try:
            name = self.nameInput.get()
            if name[0].isdigit():
                name2 = ''.join(i for i in name if i in '0123456789')
                self.nameInput.delete(0,END)
        #         self.nameInput.selec
                self.nameInput.insert(0, name2)
            else:
                name2 = name
            tt = self.getStockList(name2)
            
            self.list = None
            if(len(tt) == 1):
                self.list = tt[0]

            if self.list == None:
                name ='erro'
    #             return None
            else:
                if not self.list in stockListTmp:
                    stockListTmp.append(self.list)
                    name = 'code:{0} name:{1}'.format(self.list, self.stock[self.list])
            
                #messagebox.showinfo('Message', ' %s' % name)
            print(event.keycode)
            if event.keycode == 13:
#                 self.destroy()
#                 self.quit()
                pass
                
        except Exception as err:
            print(str(err))
    
    def clear(self):
        global stockListTmp
        stockListTmp.clear()
        
    def getStock(self):
        global stockListTmp
        if self.list == None:
            return None        
        stockListTmp.append(self.list)
        return self.list

isRun = 1

def getList():
    global stockListTmp
    global isRun
    while(True):
        a = msvcrt.getch()
        while msvcrt.kbhit():
            msvcrt.getch()
        if bytes.decode(a) == '\r':
            tk = GuiApplication()
            tk.focus_force()
            tk.mainloop()
            
        elif bytes.decode(a) == 'q':
            isRun = 0
            break
    print('Exiting getList...')        

def dispStock():
    global stockListTmp
    global isRun
    while(True):
        if isRun == 0:
            break
        time.sleep(5)
        stockquote.ddmain(2,1)
        if stockListTmp != None:
            stockquote.test_china_individual_data(stockListTmp)          
    print('Exiting dispStock...')

def main():
    
    th2 = Th2(func=dispStock)
    th2.start()

    getList()
#     th1.join()
    th2.join()
    

if __name__ == '__main__':
    main()