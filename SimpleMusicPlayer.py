import os
import sys
import tkinter as tk
import tkinter.filedialog
from tkinter import Text
import itertools
import threading
import pickle
import glob
import pygame
from pydub import AudioSegment
import random
#__line__
import re
import tempfile
import shutil
#/__line__
import subprocess
from subprocess import PIPE


class encoder:
    def __init__(self, stream, out, **options):
        self.stream = stream
        self.out = out
   
        
    def output(self, *options):
        self.fname = os.path.basename(self.stream)
        #if option == False:
            #self.command = ['ffmpeg.exe', '-i', self.stream, self.out]
        #elif option == True:
        self.command = ['ffmpeg.exe', '-i', self.stream, self.out]
        if len(options) != 0:
            self.command[len(self.command) - 1:1] = options
        #print(self.command)
        subprocess.run(self.command)
        


def changePage(page):
    # MainPageを上位層にする
    page.tkraise()


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        str = f'{str}\n'
        self.widget.delete("1.0", "end")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        
    def flush(self):
        self.widget.delete("1.0", "end")
        #pass


def set_dir():
    if not os.path.exists('./lib.txt'):
        dir = './'
        saving_direcory_path = tkinter.filedialog.askdirectory(initialdir = dir)
        saving_direcory_path = saving_direcory_path + '/'
        with open('./lib.txt', 'a') as a:
            a.write(saving_direcory_path)
    else:
        with open('./lib.txt', 'r') as a:
            saving_direcory_path = a.read()

    return saving_direcory_path
    
    
def set_dirs(fe, opt=None):
    if fe == 0:
        if not os.path.exists('./libs.txt'):
            with open('./libs.txt', 'w') as a:
                a.write(opt)
        with open('./libs.txt', 'r') as a:
            saving_direcory_path = [x.strip() for x in a.readlines()]
            
    elif not os.path.exists('./libs.txt'):
        dir = './'
        saving_direcory_path = tkinter.filedialog.askdirectory(initialdir = dir)
        saving_direcory_path = saving_direcory_path + '/'
        with open('./libs.txt', 'a') as a:
            a.write(saving_direcory_path)
            
    elif fe == 1:
        dir = './'
        saving_direcory_path = tkinter.filedialog.askdirectory(initialdir = dir)
        saving_direcory_path = saving_direcory_path + '/'
        with open('./libs.txt', 'a') as a:
            a.write(f'\n{saving_direcory_path}')
        with open('./libs.txt', 'r') as a:
            saving_direcory_path = [x.strip() for x in a.readlines()]
            
    else:
        with open('./libs.txt', 'r') as a:
            saving_direcory_path = [x.strip() for x in a.readlines()]

    return saving_direcory_path

def set_vol():
    if not os.path.exists('./vol.txt'):
        saving_direcory_path = str(1.0)
        with open('./vol.txt', 'a') as a:
            a.write(saving_direcory_path)
    else:
        with open('./vol.txt', 'r') as a:
            saving_direcory_path = a.read()

    return saving_direcory_path

def record_vol(i):
    if os.path.exists('./vol.txt'):
        saving_direcory_path = i
        with open('./vol.txt', 'w') as a:
            a.write(saving_direcory_path)

    
def export_imgs(fpath, pathy):
    with tempfile.TemporaryDirectory() as temp_dir:
        object = f'{fpath}'
        shutil.copy(object, temp_dir)
        object = f'{temp_dir}/{os.path.basename(str(object))}'
        a = os.path.splitext(os.path.basename(str(object)))[0]
        text = f'{pathy}{a}.wav'
        if not os.path.exists(f'{pathy}{a}.wav'):
            ffmpeg_encoder = encoder(object, f'{pathy}{a}.wav')
            ffmpeg_encoder.output()
            
        return text




class clock:
    def __init__(self, root):
        self.root = root

        self.time_start = 0
        self.min = 0
        self.flag = 0
        self.pause_flag = 0
        self.zeroflag = 0



    def time_counter(self):
        #self.a = threading.Thread(target=self.update)
        #self.a.start()
        if self.zeroflag == 0 and self.pause_flag == 0:
            self.time_start = 0
            self.zeroflag = 1


        if self.pause_flag == 0 and self.zeroflag == 1:
            self.msintimer += 1
            
        if self.pause_flag == 0 and self.zeroflag == 1 and self.msintimer >= 8:
            self.msintimer = 0
            self.time_start += 1
            
        if self.time_start >= 60 and self.pause_flag == 0:
            self.min += 1
            self.time_start = 0
            
        elif self.pause_flag == 1:
            self.stop()
            self.pause_flag = 0

        if pygame.mixer.get_busy:
            self.id = self.root.after(125, self.time_counter)

        self.update()

    def update(self):
        if self.flag == 1:
            sound = AudioSegment.from_file(self.entries[self.boxes])
            rate = sound.frame_rate
            pygame.mixer.init(frequency = rate)
            z = pygame.mixer.Sound(self.entries[self.boxes])
            self.z = z.get_length()
            #if self.time_start + self.min * 60 > self.z + 1:
                 #if var.get() >= 1 :
                    #self.reset(self.mes, self.listbox, self.entries, self.boxes)
                 #else:
                      #self.root.after_cancel(self.id)
                #self.reset(self.mes, self.listbox, self.entries, self.boxes)
            self.mes.configure(text=f'{str(self.min).zfill(2)}:{str(self.time_start).zfill(2)}')


    def reset(self, mes, listbox, entries, boxes):
        self.zeroflag = 0
        self.time_start = 0
        self.min = 0
        self.msintimer = 0

        self.mes = mes
        self.listbox = listbox
        self.entries = entries
        self.boxes = boxes
        if self.flag == 0:
            self.flag = 1
        else:
            self.root.after_cancel(self.id)
        self.time_counter()


    def pause(self):
        self.nowmin = self.min
        self.nowtime = self.time_start
        self.nowmsintimer = self.msintimer
        self.root.after_cancel(self.id)
     

    def unpause(self):
        self.pause_flag = 1
        self.min = self.nowmin
        self.time_start = self.nowtime
        self.msintimer = self.nowmsintimer
        self.time_counter()

    def stop(self):
        self.root.after_cancel(self.id)






def gets_info(x):
    n = pygame.mixer.Sound(x)
    info = n.get_length()
    return info



class Box_Count(object):
    def __init__(self, frames, clock):
        self.clock = clock

        self.Val = tk.StringVar()
        self.boxes = 0
        self.flag = 0
        self.aflag = 0
        self.info = 0
        self.barflag = 0
        self.valx = 0

        self.idflag = 0
        self.play_flag = 0


        self.flags = [i for _ in range(5) for i in [0]]
        self.dir = set_dir()
        self.entries = glob.glob(f'{self.dir}**')
        
        self.var = tkinter.IntVar()
        self.var.set(0)
        #test
        for i, ty in enumerate(self.entries):
            if 'wav' in ty:
                continue
                
            elif 'wav' not in ty:
                if not os.path.exists('./needs'):
                    os.mkdir('./needs')
                fname = export_imgs(ty, './needs/')
                self.entries[i] = fname
        #/test
        self.update()

        self.mes = tk.Label(frames[0], width=50, text='')
        self.mes.pack()
        self.mesg = tk.Label(frames[0], text='▼     PLAY    LIST    ▼')
        self.mesg.pack()

        self.listbox = tk.Listbox(frames[0], width=55, height=25)
        self.listbox.pack()

        #length=100
        self.scale_mes = tk.Label(frames[4], text='vol')
        self.scale = tk.Scale(frames[4], length=300, orient = 'h', from_ = 0.00, to = 1.00,
                      resolution = 0.01 ,command = self.volume_change)

        self.mesge = tk.Label(frames[3], width=50, text='')

        
        self.vol = set_vol()
        self.scale.set(float(self.vol)) # 音量スライダーの初期値
        self.scale_mes.pack(side='left')
        self.scale.pack(side="left")
        self.mesge.pack()
        pygame.mixer.init()
        


    def add_box(self, * event):
        self.play_flag = 0
        if self.var.get() == 3:
            self.boxes = random.randrange(len(self.entries))
            if self.barflag == 1:
                self.barflag = 0
        elif self.var.get() == 0:
            self.play_flag = 1
            self.stop()
        elif self.var.get() == 1:
            pass
        else:
            print('seq2')
            if self.boxes > len(self.entries):
                self.boxes = 0
            else:
                self.boxes += 1

        if self.play_flag == 0:
            self.play(self.mes, self.listbox, self.entries, self.boxes, self.mesge)
            self.info = gets_info(self.entries[self.boxes])
        #play(self.mes, self.listbox, self.entries, self.boxes)
        #self.info = gets_info(self.entries[self.boxes])
        if not self.idflag == 0:
            self.refresh_seq()
        else:
            self.idflag = 1
        return 0

    def decrease_box(self, * event):
        self.play_flag = 0

        if self.var.get() == 3:
            self.boxes = random.randrange(len(self.entries))
            if self.barflag == 1:
                self.barflag = 0
        elif self.var.get() == 0:
            self.play_flag = 1
            self.stop()
        elif self.var.get() == 1:
            pass
        else:
            self.boxes -= 1
            if self.boxes < 0:
                self.boxes = len(self.entries)
            #else:
        if self.play_flag == 0:
            self.play(self.mes, self.listbox, self.entries, self.boxes, self.mesge)
            self.info = gets_info(self.entries[self.boxes])
        if not self.idflag == 0:
            self.refresh_seq()
        else:
            self.idflag = 1

    def pause(self, * event):
        if self.flag == 0:
             self.flag = 1
             self.play(self.mes, self.listbox, self.entries, 0, self.mesge)

        elif self.aflag == 0:
            self.aflag = 1
            pygame.mixer.music.pause()
            self.clock.pause()
            self.root.after_cancel(self.id)

        elif self.aflag == 1:
            self.aflag = 0
            pygame.mixer.music.unpause()
            self.clock.unpause()
            self.barflag = 0

    def callback(self, * event):
        self.flag = 1
        num = self.listbox.curselection()[0]
        self.boxes = num
        self.clock.reset(self.mes, self.listbox, self.entries, self.boxes)
        self.play(self.mes, self.listbox, self.entries, self.boxes, self.mesge)
        self.info = gets_info(self.entries[self.boxes])

        if not self.idflag == 0:
            self.refresh_seq()
            
        else:
            self.idflag = 1

    def seq(self):
        if self.boxes > len(self.entries):
            self.boxes = 0
        else:
            self.boxes += 1
        self.clock.reset(self.mes, self.listbox, self.entries, self.boxes)
        self.play(self.mes, self.listbox, self.entries, self.boxes, self.mesge)
        self.info = gets_info(self.entries[self.boxes])
        self.refresh_seq()

    def random(self):
         self.dump = self.boxes
         self.boxes = random.randrange(len(self.entries))
         while self.dump == self.boxes:
            self.boxes = random.randrange(len(self.entries))
            
         self.clock.reset(self.mes, self.listbox, self.entries, self.boxes)
         self.play(self.mes, self.listbox, self.entries, self.boxes, self.mesge)
         self.info = gets_info(self.entries[self.boxes])
         self.refresh_seq()

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.init()
        self.clock.stop()
        self.refresh_seq()

    def loop(self):
        self.clock.reset(self.mes, self.listbox, self.entries, self.boxes)
        self.play(self.mes, self.listbox, self.entries, self.boxes, self.mesge)
        self.info = gets_info(self.entries[self.boxes])
        self.refresh_seq()

    def control(self, valx):
            self.valx = valx
            self.barflag = 1
            self.dec = int(self.info - (self.clock.time_start + self.clock.min * 60 )) * 1000
            commandlist = [self.stop, self.loop, self.seq, self.random]
            self.id = self.root.after(int(self.dec), commandlist[valx])

    def update(self):
         if self.info != 0  and self.var.get() == 0  and self.barflag == 0 and self.aflag == 0:
            print('ln5')
            self.control(0)

         elif self.info != 0  and self.var.get() == 1  and self.barflag == 0 and self.aflag == 0:
            print('ln6')
            self.control(1)

         elif self.info != 0 and self.var.get() == 2 and self.barflag == 0 and self.aflag == 0:#シーケンシャル再生
            print('ln4')
            self.control(2)

         elif self.info != 0 and self.var.get() == 3 and self.barflag == 0 and self.aflag == 0:#random再生
            print('ln3')
            self.control(3)

         elif self.valx != self.var.get(): #and (var.get() == 0 or var.get() == 1):
            print('changed')
            self.refresh_seq()

         self.id2 = self.root.after(5, self.update)

    def refresh_seq(self):
        #if self.barflag == 1:
            #self.dec = float(self.info * 1000 - ((self.clock.time_start - (self.clock.min * 60)) * 1000)
            self.barflag = 0
            #self.clock.stop()
            self.root.after_cancel(self.id)

    def flush(self):
         for i, d in enumerate(self.entries):
             d = os.path.splitext(os.path.basename(d))[0]
             indicate = f'{str(i).zfill(2)}: {d}'
             self.listbox.insert(tk.END, indicate)

    def volume_change(self, * event):
        pygame.mixer.music.set_volume(float(self.scale.get()))
        record_vol(str(self.scale.get()))

    def mute(self, * event):
        
        if self.flags[1] == 0:
            self.flags[1] = 1
            self.buttons[3].configure(text=u'unmute')
            pygame.mixer.music.set_volume(0.0)

        else:
            self.flags[1] = 0
            self.buttons[3].configure(text=u'mute')
            pygame.mixer.music.set_volume(float(self.scale.get()))

    def refresh(self, * event):
        self.dir = set_dir()
        self.entries = glob.glob(f'{self.dir}**')
        #test
        self.listbox.delete(0, tk.END)
        for i, ty in enumerate(self.entries):
            if 'wav' not in ty:
                if not os.path.exists('./needs'):
                    os.mkdir('./needs')
                fname = export_imgs(ty, './needs/')
                self.entries[i] = fname
        self.flush()
        
        
    def play(self, mes, listbox, entries, boxes, mes2):
        self.clock.reset(mes2, listbox, entries, boxes)
        pygame.mixer.quit()
        mes.configure(text=f'{os.path.splitext(os.path.basename(entries[boxes]))[0]}')
        listbox.activate(boxes)
      
        t = threading.Thread(target=self.mplay(entries[boxes]))
        t.start()

    def mplay(self, x):
            sound = AudioSegment.from_file(x)
            rate = sound.frame_rate
            pygame.mixer.init(frequency = rate)
            if self.flags[1] == 1:
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(float(self.scale.get()))

            pygame.mixer.music.load(x)
            if self.var.get() == 1:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()

        
class mplayer(Box_Count):
    def __init__(self, frame, clock, root):
        self.root = root

        self.frame = frame
        frames = [x for _ in range(6) for x in [tk.Frame(frame[1], width=350, height=50)] for _ in [x.pack()]]
        super().__init__(frames, clock)


        
        self.buttons = [a for button, command in zip(['◀', '●', '▶', 'mute', 'R'], [self.decrease_box, self.pause, self.add_box, self.mute, self.refresh]) for a in [tk.Button(frames[0], text=f'{button}', width=10)] for _ in [a.pack(side='left')] for _ in [a.bind("<Button-1>", command)]]
        for i, rbutton in enumerate(['def', 'loop', 'seq', 'random']):
            rbutton = tk.Radiobutton(frames[2], value=i, variable=self.var, text=rbutton)
            rbutton.pack(side = 'left')
        button2 = [a for button, command in zip(['dynamiq', 'folder'], [lambda event:self.exchange(frame[2]), lambda event:self.exchange(frame[3])]) for a in [tk.Button(frames[5], text=f'{button}', width=10)] for _ in [a.pack(side="left")] for _ in [a.bind("<Button-1>", command)]]
        #self.exchange(frame[0])
        self.flush()
        self.listbox.bind("<Double-1>", self.callback)
        



    def exchange(self, frame, * event):
        changePage(frame)
        

class dynamiq(tk.Frame):
    def __init__(self, root, Box_Count):
        self.Box_Count = Box_Count
        self.root = root
        super().__init__(root[2])
        self.pack()
        self.labels = [f for f in [tk.Label(self, text='▼   音量正規化   ▼'), tk.Listbox(self, width=55, height=25)] for _ in [f.pack()]]
        self.buttons = [button for button, command in zip([tk.Button(self, text='START'), tk.Button(self, text='BACK')], [self.start, lambda event:changePage(self.root[1])]) for _ in [button.pack()] for _ in [button.bind("<Button-1>", command)]]

    def match_target_amplitude(self, sound, target_dBFS): 
        change_in_dBFS = target_dBFS - sound.dBFS 
        return sound.apply_gain(change_in_dBFS)
        
        
    def main(self):
        dir = set_dir()
        self.target = [fn for fn in glob.glob(f'{dir}*.*') if '_normalized' not in fn]
        self.flush()
        for x in self.target:
             a, ext = os.path.splitext(os.path.basename(str(x)))
             ext = ext[1:]
             sound = AudioSegment.from_file(x, ext)
             normalized_sound = self.match_target_amplitude(sound, -20.0)
             normalized_sound.export(f'{dir}{a}_normalized.{ext}', format=ext)
             os.remove(x)
             self.Box_Count.refresh()
             self.labels[1].delete(0, tk.END)

             
        changePage(self.root[1])

        
    def start(self, * event):
        t = threading.Thread(target=self.main)
        t.start()
        
        
    def flush(self, * event):
         for i, d in enumerate(self.target):
             d = os.path.splitext(os.path.basename(d))[0]
             indicate = f'{str(i).zfill(2)}: {d}'
             self.labels[1].insert(tk.END, indicate)

        #st2.configure(text=f'{i} / {len(nums)}: {title}')

class folders(tk.Frame):
    def __init__(self, root, Box_Count):
        self.Box_Count = Box_Count
        self.root = root
        super().__init__(root[3])
        self.pack()
        self.labels = [f for f in [tk.Label(self, text='▼   SET_DIRS    ▼'), tk.Listbox(self, width=55, height=25), tk.Label(self, text='')] for _ in [f.pack()]]
        self.labels[1].bind("<Double-1>", self.update_dir)
        self.buttons = [button for button, command in zip([tk.Button(self, text='ADD'), tk.Button(self, text='CL'), tk.Button(self, text='BACK')], [self.add, self.decrease_box, lambda event:changePage(self.root[1])]) for _ in [button.pack()] for _ in [button.bind("<Button-1>", command)]]
        dirpath = set_dir()
        self.dirs  = set_dirs(0, opt=dirpath)
        self.flush()
        self.flag = 0
        changePage(root[1])

        
    def update_dir(self, * event):
        nums = self.labels[1].curselection()[0]
        self.dir = self.dirs[nums]
        
        with open('./lib.txt', 'w') as f:
            f.write(self.dir)
        self.labels[2].configure(text=self.dir)
        self.Box_Count.refresh()
        
        
    def add(self, * event):
        self.dirs = set_dirs(1)
        self.flush()
        self.Box_Count.refresh()
        
    def decrease_box(self, * event):
       self.dirs.remove(self.dirs[len(self.dirs) - 1])
       self.labels[1].delete(len(self.dirs), tk.END)
       with open('./libs.txt', 'w') as f:
            for x, d in enumerate(self.dirs):
                #if x == 0:
                 #   f.write(d)
               # else:
                    f.write(f'\n{d}')
       self.Box_Count.refresh()
            
            
    def flush(self, * event):
         self.labels[1].delete(0, tk.END)
         for i, d in enumerate(self.dirs):
             #if i == 0:
             #   continue
             #else:
                indicate = f'{str(i).zfill(2)}: {d}'
                self.labels[1].insert(tk.END, indicate)
             
             
             
             
             
def main():
    root = tk.Tk()

    # ウインドウのタイトルを定義する
    root.title(u'GUIsaitama')

    # ここでウインドウサイズを定義する
    root.geometry('350x750')
    root.withdraw
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # TEST AREA 
    frame = [i for _ in range(4) for i in [tk.Frame(root, width=350, height=750)] for _ in [i.grid(row=0, column=0, sticky='nsew')]]


    clocks = clock(root)

    Box_Count = mplayer(frame, clocks, root)
    dynamiq(frame, Box_Count)
    folders(frame, Box_Count)


    root.mainloop()


if __name__ == '__main__':
    main()