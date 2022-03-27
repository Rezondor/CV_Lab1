import datetime
import math
import shutil
import threading
import tkinter as tk
import tkinter.filedialog as fd
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)




class TkinterWin(tk.Tk):
    window = 0
    old_x, old_y = 0, 0
    rect_id = -1
    Y = -1;
    rlable = 0
    blable = 0
    glable = 0
    sredotk = 0
    intensitylable = 0
    positionlable = 0
    standotk = 0
    rgb_im = 0
    np_image = 0
    canvas = 0
    var = 0
    var1 = 0
    fig = 0
    temp_mass = [0, 0, 0, 0, 0]
    prev_x = 0
    prev_y = 0
    image = 0
    w = 0
    h = 0
    checkbox_check = 0
    scale = 0
    img = 0
    grafFrame = 0
    window2 = 0
    canvas2 = 0
    canvas1 = 0
    save_image = 0

    def __init__(self, root):
        self.window = root

        self.fig = plt
        self.window.title("Лаб 1 Основное окно")
        self.window.minsize(width=900, height=600)

        self.var = tk.IntVar()
        self.var1 = tk.IntVar()
        self.var.set(-1)

        # Основной фрейм для фото
        # Ширину и высоту надо изменить при загрузке изображения
        image1 = Image.open("C:\\Users\\svezh\\Desktop\\CV\\Lab1\\5.png")

        sema = threading.Semaphore(1)
        self.rgb_im = image1.convert('RGB')
        self.prev_x, self.prev_y = -1, -1
        self.np_image = np.array(image1)
        self.np_image = self.np_image[:, :, :3]

        photo = ImageTk.PhotoImage(image1)
        self.w, self.h = image1.size
        imgfarme = tk.Frame(self.window)
        self.save_image = self.np_image
        self.canvas = tk.Canvas(imgfarme, height=self.h, width=self.w)
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=photo)


        # Основной фрейм для инфы
        infoframe = tk.Frame(self.window, width=400, height=400, highlightthickness=1, highlightbackground="black")

        # Фрейм для кнопок и РГБ
        dopframe1 = tk.Frame(infoframe, width=400, height=50)

        # Фрейм для инфы по яркости и РГБ
        rgbfarme = tk.Frame(dopframe1, width=200, height=50, highlightthickness=1, highlightbackground="black")

        # Лейблы для ргб и яркости и позиции
        self.rlable = tk.Label(rgbfarme, text="R: ", anchor="nw")
        self.blable = tk.Label(rgbfarme, text="B: ", anchor="nw")
        self.glable = tk.Label(rgbfarme, text="G: ", anchor="nw")
        self.sredotk = tk.Label(rgbfarme, text="μWp: ", anchor="nw")
        self.standotk = tk.Label(rgbfarme, text="sWp: ", anchor="nw")
        self.positionlable = tk.Label(rgbfarme, text="Позиция: ", anchor="nw")
        self.intensitylable = tk.Label(rgbfarme, text="Интенсивность: ", width=23, anchor="nw")

        self.positionlable.pack(fill=tk.X, side=tk.TOP)
        self.intensitylable.pack(fill=tk.X, side=tk.TOP)
        self.sredotk.pack(fill=tk.X, side=tk.TOP)
        self.standotk.pack(fill=tk.X, side=tk.TOP)
        self.rlable.pack(fill=tk.X, side=tk.TOP)
        self.glable.pack(fill=tk.X, side=tk.TOP)
        self.blable.pack(fill=tk.X, side=tk.TOP)

        # Фрейм для кнопок
        buttonfarme = tk.Frame(dopframe1, width=200, height=50, highlightthickness=1, highlightbackground="black")
        self.checkbox_check = tk.IntVar()
        savebutton = tk.Button(buttonfarme, text="Сохранить", width=25, command=self.save_click)
        checkbox = tk.Checkbutton(buttonfarme, text="Яркость по строке", variable=self.checkbox_check, onvalue=1, offvalue=0)

        self.checkbox_check.set(0)
        savebutton.grid(row=0, padx=5, pady=5)
        checkbox.grid(row=1, padx=5, pady=5)

        # Фрейм для изменения характеристик фото
        radbuttonframe = tk.Frame(infoframe, width=400, height=50, highlightthickness=1, highlightbackground="black")
        radiobuttonframe = tk.Frame(radbuttonframe, width=400, height=50)
        peremframe = tk.Frame(radbuttonframe, width=400, height=50)
        self.scale = tk.Scale(peremframe, from_=-100, to=100, orient=tk.HORIZONTAL, resolution=1, length=400, command=self.onScale)

        btrabut = tk.Radiobutton(radiobuttonframe, text="Яркость", variable=self.var, value=0, command=self.setval)
        rrabut = tk.Radiobutton(radiobuttonframe, text="Красный", variable=self.var, value=1, command=self.setval)
        brabut = tk.Radiobutton(radiobuttonframe, text="Синий", variable=self.var, value=3, command=self.setval)
        grabut = tk.Radiobutton(radiobuttonframe, text="Зелёный", variable=self.var, value=2, command=self.setval)
        conrabut = tk.Radiobutton(radiobuttonframe, text="Контрастность", variable=self.var, value=4, command=self.setval)

        self.scale.pack()
        self.scale.set(0)

        btrabut.grid(padx=5, pady=5, column=0, row=1)
        rrabut.grid(padx=5, pady=5, column=0, row=0)
        brabut.grid(padx=5, pady=5, column=1, row=0, sticky="nw")
        grabut.grid(padx=5, pady=5, column=2, row=0, sticky="nw")

        conrabut.grid(padx=5, pady=5, column=2, row=1)
        radiobuttonframe.grid(padx=5, pady=5, column=0, row=0)
        peremframe.grid(padx=5, pady=5, column=0, row=1)

        # Фрейм для задания 5 "С"
        dopframe2 = tk.Frame(infoframe, width=400, height=50, highlightthickness=1, highlightbackground="black")
        button5Cfarme = tk.Frame(dopframe2, width=400, height=50, highlightthickness=1, highlightbackground="black")
        button5F2farme = tk.Frame(dopframe2, width=400, height=50, highlightthickness=1, highlightbackground="black")

        neglable = tk.Label(button5Cfarme, text="Негатив", anchor="nw")
        btnegbutton = tk.Button(button5Cfarme, text="Яркости", width=13, command=self.neg_br)
        dop = tk.Label(button5F2farme, text="Доп задание", anchor="nw")
        dopbtbutton = tk.Button(button5F2farme, text="Совместить", width=13, command=self.dop_task)

        neglable.grid(column=0, row=0, sticky="nw")
        btnegbutton.grid(padx=5, pady=5, column=0, row=1)
        dop.grid(column=0, row=0, sticky="nw")
        dopbtbutton.grid(padx=5, pady=5, column=0, row=1)

        # Фрейм для задания 5 "D"
        button5Dfarme = tk.Frame(infoframe, width=400, height=50, highlightthickness=1, highlightbackground="black")
        tr_lable = tk.Label(button5Dfarme, text="Обмен цветов", anchor="nw")
        r_b_tr_button = tk.Button(button5Dfarme, text="R<->B", width=13, command=self.trade_color_R_B)
        r_g_tr_button = tk.Button(button5Dfarme, text="R<->G", width=13, command=self.trade_color_R_G)
        g_b_tr_button = tk.Button(button5Dfarme, text="G<->B", width=13, command=self.trade_color_G_B)

        tr_lable.grid(column=0, row=0, sticky="nw")
        r_b_tr_button.grid(padx=5, pady=5, column=0, row=1)
        r_g_tr_button.grid(padx=5, pady=5, column=1, row=1)
        g_b_tr_button.grid(padx=5, pady=5, column=2, row=1)

        # Фрейм для задания 5 "E"
        button5Efarme = tk.Frame(infoframe, width=400, height=50, highlightthickness=1, highlightbackground="black")
        obm_lable = tk.Label(button5Efarme, text="Симметричное отображение ", anchor="nw")
        hor_obm_button = tk.Button(button5Efarme, text="По горизонтали", width=13, command=self.hor)

        obm_lable.grid(padx=5, pady=5, column=0, row=0)
        hor_obm_button.grid(padx=5, pady=5, column=1, row=0)

        # Фрейм для задания 5 "F"
        button5Ffarme = tk.Frame(infoframe, width=400, height=50, highlightthickness=1, highlightbackground="black")
        del_lable = tk.Label(button5Ffarme, text="Удаление шума", anchor="nw")
        del_4_button = tk.Button(button5Ffarme, text="4-связность", width=13, command=self.del_4)
        del_8_button = tk.Button(button5Ffarme, text="8-связность", width=13, command=self.del_8)

        del_lable.grid(column=0, row=0, sticky="nw")
        del_4_button.grid(padx=5, pady=5, column=0, row=1)
        del_8_button.grid(padx=5, pady=5, column=1, row=1)

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-1>', self.click_can)
        self.canvas.grid()

        imgfarme.grid(padx=5, pady=5, column=0, row=0)
        infoframe.grid(padx=5, pady=5, column=1, row=0)
        dopframe1.grid(padx=5, pady=5, column=0, row=0, sticky="nw")
        dopframe2.grid(padx=5, pady=5, column=0, row=5, sticky="nw")

        radbuttonframe.grid(padx=5, pady=5, column=0, row=1, sticky="nw")
        button5Cfarme.grid(padx=5, pady=5, column=0, row=0, sticky="nw")
        button5Dfarme.grid(padx=5, pady=5, column=0, row=3, sticky="nw")
        button5Efarme.grid(padx=5, pady=5, column=0, row=4, sticky="nw")
        button5Ffarme.grid(padx=5, pady=5, column=0, row=6, sticky="nw")
        button5F2farme.grid(padx=5, pady=5, column=1, row=0, sticky="nw")
        rgbfarme.grid(padx=5, pady=5, column=0, row=0)
        buttonfarme.grid(padx=5, pady=5, column=1, row=0)
        self.window2 = tk.Toplevel(self.window)
        self.grafFrame = tk.Frame(self.window2, width=400, height=200,highlightthickness=1, highlightbackground="black")
        self.grafFrame.grid(padx=5, pady=5, column=0, row=0)
        self.graf()
        self.window.mainloop()

    def graf(self):
        if self.canvas1:
            self.canvas1.get_tk_widget().destroy()
        colors = ("red", "green", "blue", "black")
        channel_ids = (0, 1, 2, 3)
        self.fig.title("Color Histogram")
        self.fig.xlabel("Color value")
        self.fig.ylabel("Pixel count")
        bb = self.fig.figure()
        ax = bb.add_axes([0.1, 0.1, 0.85, 0.85])
        self.fig.xlim([0, 256])
        for channel_id, c in zip(channel_ids, colors):
            if channel_id != 3:
                histogram, bin_edges = np.histogram(
                    self.np_image[:, :, channel_id], bins=256, range=(0, 256)
                )
            else:
                histogram, bin_edges = np.histogram(
                    self.np_image[:, :, 0] + self.np_image[:, :, 1] + self.np_image[:, :, 2], bins=256, range=(0, 256)
                )
            ax.plot(histogram, label=c, color=c)
        ax.legend()


        self.canvas1 = FigureCanvasTkAgg(bb, master=self.grafFrame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(padx=5, pady=5, column=0, row=0)


    def motion(self, event):
        try:
            x, y = event.x, event.y
            self.Y = event.y
            if (self.prev_x, self.prev_y) == (x, y): return
            if (self.rect_id < 0):
                self.old_x, self.old_y = x, y
                self.rect_id = self.canvas.create_rectangle(x - 6, y - 6, x + 6, y + 6)
            else:
                self.canvas.delete(self.rect_id)
                self.rect_id = self.canvas.create_rectangle(x - 6, y - 6, x + 6, y + 6)
                shift = x - self.old_x, y - self.old_y
                self.old_x, self.old_y = x, y
                self.canvas.move(self.rect_id, *shift)
                self.prev_x, self.prev_y = x, y

            img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
            self.image = self.canvas.create_image(0, 0, anchor="nw", image=img)
            r, g, b = self.np_image[y][x][0], self.np_image[y][x][1], self.np_image[y][x][2]
            sred = (r + g + b) / 3
            sredotkl = (abs(r - sred) + abs(b - sred) + abs(g - sred) / 3)
            cvadotk = math.sqrt((1 / 3) * (((r - sred) ** 2) + ((g - sred) ** 2) + ((b - sred) ** 2)))
            self.rlable["text"] = f'R: {r}'
            self.blable["text"] = f'B: {b}'
            self.glable["text"] = f'G: {g}'
            self.sredotk["text"] = f'μWp: {sredotkl:.3f}'
            self.intensitylable["text"] = f'Интенсивность: {sred:.3f}'
            self.positionlable["text"] = f'Позиция: {x}, {y}'
            self.standotk["text"] = f'sWp: {cvadotk:.3f}'
            self.prev_x, self.prev_y = x, y



        except IndexError:
            return

    def graf1(self, y):
        if self.canvas1:
            self.canvas1.get_tk_widget().destroy()
        c = "blue"
        self.fig.title("Color Histogram")
        self.fig.xlabel("Color value")
        self.fig.ylabel("Pixel count")
        bb = self.fig.figure()
        ax = bb.add_axes([0.1, 0.1, 0.85, 0.85])
        self.fig.xlim([0, 256])
        histogram, bin_edges = np.histogram(
            self.np_image[y, :, 0] + self.np_image[y, :, 1] + self.np_image[y, :, 2], bins=256, range=(0, 256)
        )
        ax.plot(histogram, label=c, color=c)
        ax.legend()

        self.canvas1 = FigureCanvasTkAgg(bb, master=self.grafFrame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(padx=5, pady=5, column=0, row=0)

    def save_click(self):
        directory = fd.askdirectory(title="Выберите папку", initialdir="/")
        vrem_name = datetime.datetime.now().time().second.__str__() + "." + datetime.datetime.now().time().minute.__str__() \
                    + "." + datetime.datetime.now().time().hour.__str__() + "_" + date.today().__str__() + ".png"

        Image.fromarray(self.np_image).save(vrem_name)
        shutil.move(vrem_name, directory)

    # Обмен цветов
    def trade_color_R_B(self):
        self.np_image[:, :, [0]], self.np_image[:, :, [2]] = self.np_image[:, :, [2]], self.np_image[:, :, [0]]
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.save_image = self.np_image
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.graf()

    def trade_color_R_G(self):
        self.np_image[:, :, [0]], self.np_image[:, :, [1]] = self.np_image[:, :, [1]], self.np_image[:, :, [0]]
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.save_image = self.np_image
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def trade_color_G_B(self):
        self.np_image[:, :, [2]], self.np_image[:, :, [1]] = self.np_image[:, :, [1]], self.np_image[:, :, [2]]
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.save_image = self.np_image
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def neg_br(self):
        self.np_image = 255 - self.np_image
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.save_image = self.np_image
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    # Отражение
    def hor(self):
        self.np_image = np.fliplr(self.np_image)
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.save_image = self.np_image
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    # увеличение/уменьшение интенсивности яркости и отдельных цветовых каналов
    def intens(self, val, col):
        vrem = int(val)
        if col == -1:
            self.np_image = self.np_image + vrem
        else:
            if 0 <= col < 3:
                self.np_image[..., col] = self.np_image[..., col] + vrem
        new_function = np.vectorize(self.addition)
        self.np_image = new_function(self.np_image)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def contr(self, val):
        self.np_image = self.save_image
        contrast = (100.0 + float(val)) / 100.0
        contrast = contrast * contrast
        a = self.np_image
        a = a / 255.0
        a = a - 0.5
        a = a * contrast
        a = a + 0.5
        a = a * 255

        a = a.astype(int)
        new_function = np.vectorize(self.addition)
        a = new_function(a)
        self.np_image = a
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def addition(self, x):
        if x <= 0:
            return 0
        else:
            if x >= 255:
                return 255
            else:
                return x

    def onScale(self, val):
        vrem = self.var.get()
        if vrem != -1:
            self.temp_mass[vrem] = val
            if vrem == 0:
                self.intens(val, -1)
            if vrem == 1:
                self.intens(val, vrem - 1)
            if vrem == 2:
                self.intens(val, vrem - 1)
            if vrem == 3:
                self.intens(val, vrem - 1)
            if vrem == 4:
                self.contr(val)

    def setval(self):
        vrem = self.var.get()
        if 0<= vrem <4:
            self.scale.config(from_=-255, to=255)
        else:
            self.scale.config(from_=-100, to=100)
        self.scale.set(self.temp_mass[vrem])


    def dop_task(self):
        self.img = np.array(Image.open("C:\\Users\\svezh\\Desktop\\CV\\Lab1\\4.png"))
        self.img = self.img[:, :, :3]
        dst = (self.img * 0.8 + self.np_image * 0.3).astype(np.uint8)
        self.np_image = dst
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image ))
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def del_4(self):
        self.rgb_im = Image.fromarray(self.np_image).convert('RGB')
        found_pixels = []
        for i, pixel in enumerate(self.rgb_im.getdata()):
            found_pixels.append(i)

        found_pixels_coords = [divmod(index, self.h) for index in found_pixels]
        members = [(0, 0)] * 5

        for i, j in found_pixels_coords:
            if 0 < i < self.w - 1 and 0 < j < self.h - 1:
                members[0] = self.rgb_im.getpixel((i - 1, j))
                members[1] = self.rgb_im.getpixel((i, j - 1))
                members[2] = self.rgb_im.getpixel((i, j))
                members[3] = self.rgb_im.getpixel((i, j + 1))
                members[4] = self.rgb_im.getpixel((i + 1, j))
                res = [int(sum(ele) / len(members)) for ele in zip(*members)]
                res = tuple(res)
                self.rgb_im.putpixel((i, j), res)
            else:
                continue
        np_image2 = np.array(self.rgb_im)
        self.np_image = np_image2[:, :, :3]
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def del_8(self):
        self.rgb_im = Image.fromarray(self.np_image).convert('RGB')
        found_pixels = []
        for i, pixel in enumerate(self.rgb_im.getdata()):
            found_pixels.append(i)

        found_pixels_coords = [divmod(index, self.h) for index in found_pixels]
        members = [(0, 0)] * 9

        for i, j in found_pixels_coords:
            if 0 < i < self.w - 1 and 0 < j < self.h - 1:
                members[0] = self.rgb_im.getpixel((i - 1, j - 1))
                members[1] = self.rgb_im.getpixel((i - 1, j))
                members[2] = self.rgb_im.getpixel((i - 1, j + 1))
                members[3] = self.rgb_im.getpixel((i, j - 1))
                members[4] = self.rgb_im.getpixel((i, j))
                members[5] = self.rgb_im.getpixel((i, j + 1))
                members[6] = self.rgb_im.getpixel((i + 1, j - 1))
                members[7] = self.rgb_im.getpixel((i + 1, j))
                members[8] = self.rgb_im.getpixel((i + 1, j + 1))
                res = [int(sum(ele) / len(members)) for ele in zip(*members)]
                res = tuple(res)
                self.rgb_im.putpixel((i, j), res)
            else:
                continue
        np_image2 = np.array(self.rgb_im)
        self.np_image = np_image2[:, :, :3]
        self.graf()
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.np_image.astype(np.uint8)))
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def click_can(self, event):
        if self.checkbox_check.get() == 1:
            self.graf1(self.Y)


aaa = TkinterWin(tk.Tk())
aaa.window2.destroy()




