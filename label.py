#!/usr/bin/env python3

import argparse
import qrcode
from PIL import Image, ImageDraw, ImageFont

'''
sws:

if you want testing data make that an arugment 
file version even if its just a table with the last updated date and time.
'''


def printLabel(podQrData):
    CHOSEN_FONT = "Pillow/Tests/fonts/FreeMono.ttf"
    CHOSEN_FONT_SIZE = 44
    BASE_LABEL_WIDTH = 108 #labelmaker pixel width for 18mm label stock is 108 pixels
    LABEL_LENGTH = 150 #right right length for a label with QR code and band code at the bottom

    #check if podQrData is correct length at least:
    goodData = "1947ZZ9999-FF:FF:FF:FF:FF:FF-ABCD-0"
    if len(podQrData) != len(goodData):
        print(f"bad podQrData, is short: {podQrData}")
        quit()

    qr = qrcode.QRCode(
        version=None, #set to None to have QR auto fit further down
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        border=0,
    )
    qr.add_data(podQrData)
    qr.make(fit=True)
    qrCodeBasic = qr.make_image(fill_color="black", back_color="white")

    #SWS: Calulate the dimentions of the QR Code to be used when generating the image    
    #sws: basewidth == baseWidth, wpercent == wPercent

    wPercent = (BASE_LABEL_WIDTH/float(qrCodeBasic.size[0]))
    hSize = int((float(qrCodeBasic.size[1])*float(wPercent)))
    qrCodeBasic = qrCodeBasic.resize((BASE_LABEL_WIDTH,hSize), Image.ANTIALIAS)

    qrCodeExpanded = Image.new("L", (BASE_LABEL_WIDTH, LABEL_LENGTH), "white") #"L" = 8-bit pixels black and white, white bg.
    qrCodeExpanded.paste(qrCodeBasic, (0,0))


    qrCodeText = ImageDraw.Draw(qrCodeExpanded)
    fnt = ImageFont.truetype(CHOSEN_FONT, CHOSEN_FONT_SIZE)
    podCode = podQrData.split("-")[2] #grab the third element in the string, is the pod code
    print(f"podCode: {podCode}")
    qrCodeText.text((0,BASE_LABEL_WIDTH), podCode, font=fnt, fill=("black"))

    qrCodeExpanded.show()
    qrCodeExpanded.save("qr-code-text.png")
    return(True)

def main(commandline):
    print(f"now printing: {args.poddata}")
    printLabel(args.poddata)

if __name__ == "__main__":
    print("label-maker 0.1.0")
    parser = argparse.ArgumentParser(description='FPC label generator')
    parser.add_argument('--poddata', required=True, help='eg: 1947ZZ9999-FF:FF:FF:FF:FF:FF-ABCD-0') 
    args = parser.parse_args()
    main(args)