from datetime import datetime
import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import re
from reportlab.pdfgen import canvas

# ------------------------------------------------------------------------------------------- GOOGLE VISION ------------


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'VISION_API_KEY.json'

client = vision.ImageAnnotatorClient()

FILE_NAME = 'P1.jpg'
FOLDER_PATH = r'C:\Users\Admin\Desktop\AI'

with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.text_detection(image=image)  # returns TextAnnotation
df = pd.DataFrame(columns=['locale', 'description'])

texts = response.text_annotations

for text in texts:
    df = df.append(
        dict(
            locale=text.locale,
            description=text.description
        ),
        ignore_index=True
    )

bill = (
df['description'][0])  # .readlines()# --------- SEARCHING FOR PRODUCT INFORMATIONS USING REGULAR EXPRESSIONS ---

bill = bill.replace(',', '.')
bill.replace('ó', 'o')

pat3 = re.compile(r'[1-9][.]?[0-9]{,5}\s{1}x.*')
pat5 = re.compile(r'\nA(\n?.*?)([1-9].?[0-9]{,5}\sx)', flags=re.DOTALL)
pat6 = re.compile(r'\n([A-Z].*)')



# -------------------------------------------------- PRICES ----------------------------------
matches = pat3.findall(bill)
match_list = []
for match in matches:
    match_list.append(match)
print(match_list)
# --------------------------------------------------- NAMES ------------------------------------------------------------
matches2 = pat5.search(bill)
print(matches2.group(1))  #
names_text = matches2.group(1)  # ---- Searching for the fragment of text containing names -----------------------------
match_list2 = []

names = pat6.findall(names_text)
for name in names:
    if len(name) > 2:
        match_list2.append(name)
print(match_list2)  #
# ------------------------------------------------- DICTIONARY (OPTIONAL) ----------------------------------------------
values = match_list
keys = match_list2
dictionary = dict(zip(keys, values))

# ------------------------------------------------------------------------------------------- INVOICE APP --------------
class Product():
    def __init__(self, product, quantity, unit, discount, VAT_rate, VAT_amount, gross_ppu, gross_price, net_price):
        self.product = product
        self.quantity = quantity
        self.unit = unit
        self.discount = discount
        self.VAT_rate = VAT_rate  # 23%, 8% lub 5%
        self.VAT_amount = VAT_amount
        self.gross_ppu = gross_ppu
        self.gross_price = gross_price
        self.net_price = net_price

    def net_Calculate(self):
        self.gross_price = round(self.net_price * 1.23, 2)
        return self


# ------------------------------------------------------------------------------------------ FISHING -------------------
pat7 = re.compile(r'([1-9][.]?[0-9]{,5})\sx([0-9][0-9]?[0-9]?[.]?[0-9]{2})\s([0-9][0-9]?[0-9]?[.]?[0-9]{2})([A-Z])')

Quant = list()
Units = list()
PricePU = list()
PriceGR = list()
VatRa = list()
VatAm = list()
NetPr = list()

for k in match_list:
    i = pat7.search(k)
    Quant.append(float(i.group(1)))
    PricePU.append(float(i.group(2)))
    PriceGR.append(float(i.group(3)))
    if i.group(4) == 'A':
        Vat = 23
    elif i.group(4) == 'B':
        Vat = 8
    elif i.group(4) == 'C':
        Vat = 5
    VatRa.append(Vat)

    if len(i.group(1)) > 2:
        Units.append('kg.')
    else:
        Units.append('pc.')
    NetPrice_Calc = round((float(i.group(3)) / (1 + (Vat / 100))), 2)  # ZLE
    NetPr.append(NetPrice_Calc)
    VatAm.append(round(((Vat / 100) * NetPrice_Calc), 2))

print(Units)
print(Quant)
print(PricePU)
print(PriceGR)
print(VatRa)
print(VatAm)
print(NetPr)

Items = list()
for i in range(len(keys)):
    Items.append(Product(keys[i], Quant[i], Units[i], 0, VatRa[i], VatAm[i], PricePU[i], PriceGR[i], NetPr[i]))


# -----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------- PDF GENERATOR ------------

def drawMyRuler(pdf):
    pdf.drawString(100, 810, '')
    pdf.drawString(200, 810, '')
    pdf.drawString(300, 810, '')
    pdf.drawString(400, 810, '')
    pdf.drawString(500, 810, '')

    pdf.drawString(10, 100, '')
    pdf.drawString(10, 200, '')
    pdf.drawString(10, 300, '')
    pdf.drawString(10, 400, '')
    pdf.drawString(10, 500, '')
    pdf.drawString(10, 600, '')
    pdf.drawString(10, 700, '')
    pdf.drawString(10, 800, '')


# --------------------------------------------------------------- PDF CONTENT ---
fileName = 'Invoice_' + str(datetime.date(datetime.now())) + FILE_NAME.replace('.jpg', '') + '.pdf'
documentTitle = fileName

title = fileName.replace('pdf', '')
title2 = 'Company Name Inc.'
Address = ['Department 98, 44-46 Morningside Road', 'Edinburgh, Scotland', 'EH10 4BF  tel.:  48 515 468 485']
Categories = 'NO.    PRODUCT NAME            QUANT.  UNIT    DISCOUNT  VAT RATE  VAT AMOUNT  PPU + VAT  GROSS PRICE  NET PRICE'

image = 'Sample_logo.png'

pdf = canvas.Canvas(fileName)
pdf.setTitle(documentTitle)

drawMyRuler(pdf)

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(
    TTFont('Fon', 'GeosansLight.ttf')
)
pdf.setFont('Fon', 30)
pdf.drawCentredString(280, 580, title)
pdf.setFont('Fon', 24)
pdf.drawCentredString(280, 538, title2)

# ----------------------------------------------------------------------------

pdf.setFillColorRGB(0, 0, 0)
pdf.setFont("Fon", 9.67)
pdf.drawString(56, 486, Categories)


# PROD INFO NO.  PRODUCT NAME   QUANT.  UNIT  DISCOUNT  VAT RATE  VAT AMOUNT  PPU + VAT  GROSS PRICE  NET PRICE'
def draw_Products(Product):
    for Item in Items:
        Spacing = 30 * Items.index(Item)
        pdf.setFont("Fon", 9.67)
        pdf.drawString(56, 461 - Spacing, str(Items.index(Item) + 1))
        pdf.drawString(86, 461 - Spacing, (Item.product).replace('_', ' '))
        pdf.drawString(186, 461 - Spacing, str(Item.quantity))
        pdf.drawString(222, 461 - Spacing, str(Item.unit))
        pdf.drawString(249, 461 - Spacing, str(Item.discount))
        pdf.drawString(299, 461 - Spacing, str(Item.VAT_rate))
        pdf.drawString(342, 461 - Spacing, str(Item.VAT_amount))
        pdf.drawString(402, 461 - Spacing, str(Item.gross_ppu))
        pdf.drawString(447, 461 - Spacing, str(Item.gross_price))
        pdf.drawString(508, 461 - Spacing, str(Item.net_price))

draw_Products(Items)

# --------------------------------- LINES ---
# HORIZONTAL
pdf.line(50, 500, 550, 500)
pdf.line(50, 480, 550, 480)
pdf.line(50, 450, 550, 450)
pdf.line(50, 420, 550, 420)
pdf.line(50, 390, 550, 390)
pdf.line(50, 360, 550, 360)
pdf.line(50, 330, 550, 330)
pdf.line(50, 300, 550, 300)
pdf.line(50, 270, 550, 270)
pdf.line(50, 240, 550, 240)
pdf.line(50, 210, 550, 210)
pdf.line(50, 180, 550, 180)
# VERTICAL
pdf.line(50, 180, 50, 500)
pdf.line(80, 180, 80, 500)
pdf.line(178, 180, 178, 500)
pdf.line(215, 180, 215, 500)
pdf.line(241, 180, 241, 500)
pdf.line(293, 180, 293, 500)
pdf.line(336, 180, 336, 500)
pdf.line(396, 180, 396, 500)
pdf.line(441, 180, 441, 500)
pdf.line(502, 180, 502, 500)
pdf.line(550, 180, 550, 500)

text = pdf.beginText(340, 152)
text.setFont('Fon', 12)

for line in Address:
    text.textLine(line)

pdf.drawText(text)

pdf.drawInlineImage(image, 194, 646)

pdf.save()
