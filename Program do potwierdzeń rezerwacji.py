from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pdfplumber
from datetime import datetime
import re
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import sys
import os

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def find(str):
    pattern = re.compile(r'Dla:\s([a-zA-Z]\w+)\s([a-zA-Z]\w+)\s([\s\S]+)\stel.:\s([\s\S]+)\s+Pot[\s\S]+dniu:\s([\s\S]+)\sWyjazd[\s\S]+dniu:\s([\s\S]+)\sNr pokoju:\s([0-9,]+)\n[\s\S]+gości:\s([0-9]+)\s[\s\S]+pobytu:\s([0-9,]+)\s')
    matches = pattern.findall(str)
    list = matches[0]
    print(list)
    asign(list)

def asign(str):
    global imie_s, nazwisko_s, adres_s, tel_s, mail_s, checkin_s, checkout_s, room_s, guests_s, price_s
    nazwisko_s = str[0]
    imie_s = str[1]
    adres_s = str[2].replace('\n',', ')
    tel_s = str[3]
    checkin_s = str[4]
    checkout_s = str[5]
    room_s = str[6]
    guests_s = str[7]
    price_s = str[8]
    pre_fill()

def openFile():
    filepath = filedialog.askopenfilename(initialdir="C:",
                                          title="Open file okay?",
                                          filetypes= (("PDF files","*.pdf"),
                                          ("all files","*.*")))
    with pdfplumber.open(filepath) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    find(text)
    return text

def cancel_selected(event):
    cancel_e.config(state='normal')
    cancel_e.delete("1.0", "end")
    global cancel
    if cancel_opt.get() == 'Zasady Anulacji 1':
        with open("Anulacja1.txt", encoding="utf8") as myfile:
            cancel = myfile.readlines()
        cancel_list = ''.join(cancel)
        cancel_e.insert(END, cancel_list.replace('\n', ', '))
        cancel_e.config(state='disabled')
    if cancel_opt.get() == 'Zasady Anulacji 2':
        with open("Anulacja2.txt", encoding="utf8") as myfile:
            cancel = myfile.readlines()
        cancel_list = ''.join(cancel)
        cancel_e.insert(END, cancel_list.replace('\n', ', '))
        cancel_e.config(state='disabled')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - TKINTER - - -


root = Tk()
root.title("Potwierdzenia Rezerwacji (beta)")
root.iconbitmap('Icon.Ico')
root.geometry('597x828')

try:
    with open("FolderZapisu.txt", "r") as text_file:
        save_path = text_file.readline()
        print(save_path)
except:
    save_path = 'Desktop/'
    print("Ex")


imie = StringVar()
nazwisko = StringVar()
adres = StringVar()
adres2 = StringVar()
tel = StringVar()
mail = StringVar()
room = StringVar()
guests = StringVar()
checkin = StringVar()
checkout = StringVar()
price = StringVar()
comment = StringVar()
cancel = []
ser1 = StringVar()
ser2 = StringVar()
ser3 = StringVar()
ser4 = StringVar()


options = ["Usługi Gastro.", "Usługi SPA", "Usługi Dodat.", ]
cancel_option = ["Zasady Anulacji 1", "Zasady Anulacji 2"]
clicked_1 = StringVar()
clicked_2 = StringVar()
clicked_3 = StringVar()
clicked_4 = StringVar()
cancel_opt = StringVar()
cancel_opt.set(cancel_option[0])

mainframe = ttk.Frame(root, padding="18 18 26 26")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

imie_e = ttk.Entry(mainframe, width=20, textvariable=imie)
imie_e.grid(column=1, row=1, sticky=(W, E))
nazwisko_e = ttk.Entry(mainframe, width=30, textvariable=nazwisko)
nazwisko_e.grid(column=3, row=1, sticky=(W, E))
adres_e = ttk.Entry(mainframe, width=60, textvariable=adres)
adres_e.grid(column=1, row=2, columnspan=3, sticky=(W, E))
adres2_e = ttk.Entry(mainframe, width=60, textvariable=adres2)
adres2_e.grid(column=1, row=3, columnspan=3, sticky=(W, E))
tel_e = ttk.Entry(mainframe, width=20, textvariable=tel)
tel_e.grid(column=1, row=4, sticky=(W, E))
mail_e = ttk.Entry(mainframe, width=30, textvariable=mail)
mail_e.grid(column=3, row=4, sticky=(W, E))
checkin_e = ttk.Entry(mainframe, width=20, textvariable=checkin)
checkin_e.grid(column=1, row=5, sticky=(W, E))
checkout_e = ttk.Entry(mainframe, width=20, textvariable=checkout)
checkout_e.grid(column=3, row=5, sticky=(W, E))
guests_e = ttk.Entry(mainframe, width=20, textvariable=guests)
guests_e.grid(column=1, row=6, sticky=(W, E))
room_e = ttk.Entry(mainframe, width=20, textvariable=room)
room_e.grid(column=3, row=6, sticky=(W, E))
price_e = ttk.Entry(mainframe, width=20, textvariable=price)
price_e.grid(column=1, row=7, sticky=(W, E))

ser1_e = ttk.Entry(mainframe, width=20, textvariable=ser1)
ser1_e.grid(column=2, row=8, columnspan=3, sticky=(W, E))
ser2_e = ttk.Entry(mainframe, width=20, textvariable=ser2)
ser2_e.grid(column=2, row=9, columnspan=3, sticky=(W, E))
ser3_e = ttk.Entry(mainframe, width=20, textvariable=ser3)
ser3_e.grid(column=2, row=10, columnspan=3, sticky=(W, E))
ser4_e = ttk.Entry(mainframe, width=20, textvariable=ser4)
ser4_e.grid(column=2, row=11, columnspan=3, sticky=(W, E))

drop_1 = OptionMenu(mainframe, clicked_1, *options)
drop_1.grid(column=1, row=8, sticky=(W, E))
drop_2 = OptionMenu(mainframe, clicked_2, *options)
drop_2.grid(column=1, row=9, sticky=(W, E))
drop_3 = OptionMenu(mainframe, clicked_3, *options)
drop_3.grid(column=1, row=10, sticky=(W, E))
drop_4 = OptionMenu(mainframe, clicked_4, *options)
drop_4.grid(column=1, row=11, sticky=(W, E))

cancel_option = OptionMenu(mainframe, cancel_opt, *cancel_option, command=cancel_selected)
cancel_option.grid(column=3, row=16, sticky=E)

comment_e = Text(mainframe, width=50,height=4, wrap=WORD)
comment_e.grid(column=0, row=15, columnspan=5, sticky=(W, E))
cancel_e = Text(mainframe, width=50,height=12, wrap=WORD)
cancel_e.grid(column=0, row=17, columnspan=5, sticky=(W, E))

def set_output():
    global save_path
    save_path = filedialog.askdirectory()
    print(str(save_path))

    with open("FolderZapisu.txt", "w") as text_file:
        text_file.write(save_path)

    if len(save_path) < 1:
        save_path = 'Desktop/'
    return save_path


def pre_fill():
    imie_e.insert(END, imie_s)
    nazwisko_e.insert(END, nazwisko_s)
    adres_e.insert(END, adres_s)
    #adres2_e.insert(END, adres2_s)
    tel_e.insert(END, tel_s)
    #mail_e.insert(END, adres_s)
    checkin_e.insert(END, checkin_s)
    checkout_e.insert(END, checkout_s)
    room_e.insert(END, room_s)
    guests_e.insert(END, guests_s)
    price_e.insert(END, price_s)

def comment_prepare(com):
    global lines
    lines = []
    c = 0
    c1 = 0
    addnew = True
    addnew2 = True
    addnew3 = True
    addnew4 = True
    for letter in com:
        c += 1
        if len(com) < 80:
            lines.append(com.replace('\n', ''))
            break
        if c>80 and letter == ' ' and addnew:
            lines.append(com[0:c])
            c1 = c
            addnew = False
        if len(com) > 80 and len(com) < 160 and not addnew:
            lines.append(com[c1:len(com)].replace('\n', ''))
            break
        if c>160 and letter == ' ' and addnew2:
            lines.append(com[c1:c])
            c1 = c
            addnew2 = False
        if len(com) > 160 and len(com) < 240 and not addnew2:
            lines.append(com[c1:len(com)].replace('\n', ''))
            break
        if c>240 and letter == ' ' and addnew3:
            lines.append(com[c1:c])
            c1 = c
            addnew3 = False
        if len(com) > 240 and len(com) < 320 and not addnew3:
            lines.append(com[c1:len(com)].replace('\n', ''))
            break
        if c>320 and letter == ' ' and addnew4:
            lines.append(com[c1:c])
            c1 = c
            addnew4 = False
        if len(com) > 320 and len(com) < 400 and not addnew4:
            lines.append(com[c1:len(com)].replace('\n', ''))
            break
        if len(com) > 400 and not addnew4:
            lines.append(com[c1:410].replace('\n', ''))
            break
    return lines


cancel_selected(True)


# ------------------------------------------------------------------------------ PDF ---
# ------------------------------------------------------------------------------ DRAW --
def draw_PDF():
    image = 'logo1.jpg'
    pdfmetrics.registerFont(TTFont('Fon', 'Gothic.ttf'))
    pdfmetrics.registerFont(TTFont('Bon', 'GOTHICB_0.ttf'))

    filename = 'Potwierdzenie przyjęcia rezerwacji nr ' + (str(datetime.date(datetime.now()))).replace('-', '') + '.pdf'
    save_name = os.path.join(os.path.expanduser("~"), save_path, filename)
    title = filename.replace('pdf', '')
    print(save_path)
    pdf = canvas.Canvas(save_name)
    pdf.setTitle(filename)

    from reportlab.lib.colors import HexColor
    imie = imie_e.get()
    nazwisko = nazwisko_e.get()
    adres = adres_e.get()
    adres2 = adres2_e.get()
    tel = tel_e.get()
    mail = mail_e.get()
    checkin = checkin_e.get()
    checkout = checkout_e.get()
    room = room_e.get()
    guests = guests_e.get()
    price = price_e.get()
    ser1 = ser1_e.get()
    ser2 = ser2_e.get()
    ser3 = ser3_e.get()
    ser4 = ser4_e.get()
    a = 0
    try:
        comment = comment_e.get(1.0, END)
    except:
        comment = ' '
        print("An exception occurred, no comment was submitted")


    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Fon", 12)
    pdf.drawString(42, 800, "HOTEL SMILE M. DRÓŻDŻ SP.J")
    pdf.drawString(42, 786, "ul. Główna 234, 34-460 Szczawnica")
    pdf.drawString(495, 800, str((datetime.date(datetime.now()))).replace('-', '.'))

    pdf.setFont('Bon', 16)
    pdf.drawCentredString(296, 714, title)
    pdf.drawCentredString(296, 690, "w Hotelu Smile ***")
    pdf.setFont('Bon', 12)
    pdf.drawString(50, 653, "Dla:")
    pdf.setFont('Fon', 12)
    pdf.drawString(50, 622, (imie + ' ' + nazwisko))
    pdf.drawString(50, 604, adres + adres2)
    pdf.setFont('Bon', 12)
    pdf.drawString(50, 572, "Potwierdzamy Państwa rezerwację wg następujących danych:")
    pdf.setFont('Fon', 12)
    pdf.drawString(50, 538, ('Nr. telefonu:  ' + tel))
    if len(mail) > 4: pdf.drawString(320, 538, ('Email:  ' + mail))
    pdf.drawString(50, 517, ('Przyjazd w dniu:  ' + checkin))
    pdf.drawString(310, 517, ('Wyyjazd w dniu:  ' + checkout))
    pdf.drawString(50, 496, ('Nr. Pokoju:  ' + room))
    pdf.drawString(310, 496, ('Liczba Gości:  ' + guests))
    pdf.drawString(50, 475, ('Koszt Pobytu:  ' + price + ' zł'))

    if clicked_1.get() == 'Usługi SPA' and len(ser1) >= 1:
        pdf.drawString(50, 454, ('Usługi SPA:  ' + ser1))
        a += 22
    if clicked_1.get() == 'Usługi Gastro.' and len(ser1) >= 1:
        pdf.drawString(50, 454, ('Usługi Gastronomiczne:  ' + ser1))
        a += 22
    if clicked_1.get() == 'Usługi Dodat.' and len(ser1) >= 1:
        pdf.drawString(50, 454, ('Usługi Dodatkowe:  ' + ser1))
        a += 22
    if clicked_2.get() == 'Usługi SPA' and len(ser2) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi SPA:  ' + ser2))
        a += 22
    if clicked_2.get() == 'Usługi Gastro.' and len(ser2) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi Gastronomiczne:  ' + ser2))
        a += 22
    if clicked_2.get() == 'Usługi Dodat.' and len(ser2) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi Dodatkowe:  ' + ser2))
        a += 22
    if clicked_3.get() == 'Usługi SPA' and len(ser3) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi SPA:  ' + ser3))
        a += 22
    if clicked_3.get() == 'Usługi Gastro.' and len(ser3) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi Gastronomiczne:  ' + ser3))
        a += 22
    if clicked_3.get() == 'Usługi Dodat.' and len(ser3) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi Dodatkowe:  ' + ser3))
        a += 22
    if clicked_4.get() == 'Usługi SPA' and len(ser4) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi SPA:  ' + ser4))
        a += 22
    if clicked_4.get() == 'Usługi Gastro.' and len(ser4) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi Gastronomiczne:  ' + ser4))
        a += 22
    if clicked_4.get() == 'Usługi Dodat.' and len(ser4) >= 1:
        pdf.drawString(50, 454 - a, ('Usługi Dodatkowe:  ' + ser4))
        a += 22

    pdf.setFillColor(HexColor('#606161'))
    pdf.setFont('Bon', 12)
    pdf.drawString(50, 440 - a, "Warunki anulacji pobytu:")
    pdf.setFont('Fon', 10)
    pdf.drawString(50, 410 - a, cancel[0].replace('\n', ''))
    pdf.drawString(50, 394 - a, cancel[1].replace('\n', ''))
    pdf.drawString(50, 378 - a, cancel[2].replace('\n', ''))
    pdf.drawString(50, 364 - a, cancel[3].replace('\n', ''))
    pdf.drawString(50, 348 - a, cancel[4].replace('\n', ''))
    try:
        pdf.drawString(50, 332 - a, cancel[5].replace('\n', ''))
    except: pass
    try:
        pdf.drawString(50, 316 - a, cancel[6].replace('\n', ''))
    except: pass
    try:
        pdf.drawString(50, 300 - a, cancel[7].replace('\n', ''))
    except: pass
    try:
        pdf.drawString(50, 284 - a, cancel[8].replace('\n', ''))
    except: pass

    if len(comment) > 4:
        pdf.setFont('Bon', 10)
        pdf.drawString(50, 260 - a, ('Uwagi do Rezerwacji: '))
        pdf.setFont('Fon', 10)
        comment_prepare(comment)
        num = 0
        for line in lines:
            pdf.drawString(50, 240 - a, lines[num])
            num += 1
            a += 16

    pdf.setFillColor(HexColor(000000))

    pdf.line(50, 130, 546, 130)
    pdf.drawInlineImage(image, 171, 20, width=240, height=60)

    pdf.setFont("Fon", 11)
    pdf.drawCentredString(295, 112, "Hotel Smile ***, ul. Główna 234, 34-460 Szczawnica")
    pdf.drawCentredString(295, 96, "mail: biuro@hotelsmile.pl, tel. +48 606 662 665, "
                                    "12 262 10 06, www.hotelsmile.pl")

    text = pdf.beginText(340, 152)
    text.setFont('Fon', 12)
    pdf.drawText(text)

    pdf.save()
    restart_program()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ PDF ---



ttk.Label(mainframe, text="Dane Gościa: ", font=('Helvetica', 11, 'bold')).grid(column=0, row=0, sticky=W)
Dane1 = Button(mainframe, text="Wczytaj dane z potwierdzenia PDF", bd = '3', command=openFile).grid(column=3, row=0, columnspan=3, sticky=W)
ttk.Label(mainframe, text="Imię: ", font=('Helvetica', 11)).grid(column=0, row=1, sticky=W)
ttk.Label(mainframe, text="Nazwisko: ", font=('Helvetica', 11)).grid(column=2, row=1, sticky=E)
ttk.Label(mainframe, text="Adres: ", font=('Helvetica', 11)).grid(column=0, row=2, sticky=W)
ttk.Label(mainframe, text="Nr. Tel: ", font=('Helvetica', 11)).grid(column=0, row=4, sticky=W)
ttk.Label(mainframe, text="Email: ", font=('Helvetica', 11)).grid(column=2, row=4, sticky=E)
ttk.Label(mainframe, text="Przyjazd: ", font=('Helvetica', 11)).grid(column=0, row=5, sticky=W)
ttk.Label(mainframe, text="Wyjazd: ", font=('Helvetica', 11)).grid(column=2, row=5, sticky=E)
ttk.Label(mainframe, text="Liczba Gości: ", font=('Helvetica', 11)).grid(column=0, row=6, sticky=W)
ttk.Label(mainframe, text="Nr. Pokoju: ", font=('Helvetica', 11)).grid(column=2, row=6, sticky=W)
ttk.Label(mainframe, text="Koszt Pobytu: ", font=('Helvetica', 11)).grid(column=0, row=7, sticky=W)
ttk.Label(mainframe, text="zł", font=('Helvetica', 11)).grid(column=2, row=7, sticky=W)
ttk.Label(mainframe, text="Usługi Dodatkowe:", font=('Helvetica', 11)).grid(column=0, row=8, sticky=W)
ttk.Label(mainframe, text="Uwagi:", font=('Helvetica', 11)).grid(column=0, row=11, sticky=W)

ttk.Label(mainframe, text="Warunki Anulacji: ", font=('Helvetica', 11, 'bold')).grid(column=0, row=16, columnspan=3, sticky=W)
Dane2 = Button(mainframe, text="Wybierz folder zapisu", bd = '3', command=set_output).grid(column=0, row=18, columnspan=3, sticky=W)
Dane3 = Button(mainframe, text="Utwórz potwierdzenie rezerwacji PDF", bd = '3', command=draw_PDF).grid(column=2, row=18, columnspan=3, sticky=E)



for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.bind('<Return>')
root.mainloop()