#!/usr/bin/env python

import sys
import re
import datetime
from pyPdf import PdfFileWriter, PdfFileReader

backpage = False

def append_file(out, input_file_name):
    print("Open %s" % input_file_name)
    input1 = PdfFileReader(file(input_file_name, "rb"))
    page = input1.getPage(0)

    upperleft_x = page.mediaBox.getUpperLeft_x()
    upperleft_y = page.mediaBox.getUpperLeft_y()
    upperright_x = page.mediaBox.getUpperRight_x()
    upperright_y = page.mediaBox.getUpperRight_y()

    # print(page.mediaBox)
    # print(page.mediaBox.getUpperLeft_x())
    # print(page.mediaBox.getUpperLeft_y())
    # print(page.mediaBox.getUpperRight_x())
    # print(page.mediaBox.getUpperRight_y())
    # print(page.mediaBox.lowerLeft)
    # print(page.mediaBox.upperLeft)
    # print(page.mediaBox.lowerRight)
    # print(page.mediaBox.upperRight)

    if backpage:
        # устанавливаем зону обрезки по оборотной стороне уведомления
        page.mediaBox.upperRight = (
            float(page.mediaBox.getUpperRight_x()),
            float(page.mediaBox.getUpperRight_y()) - (float(page.mediaBox.getUpperLeft_y()) * 0.325)
        )
        page.mediaBox.lowerRight = (
            float(page.mediaBox.getLowerRight_x()) * 0.7,
            float(page.mediaBox.getUpperRight_y()) - (float(page.mediaBox.getUpperLeft_y()) * 0.48)
        )
    else :
        # устанавливаем зону обрезки по основной стороне уведомления
        page.mediaBox.lowerRight = (
            float(page.mediaBox.getLowerRight_x()) * 0.7,
            float(page.mediaBox.getUpperLeft_y()) - (float(page.mediaBox.getUpperLeft_y()) * 0.325)
        )
    #print(page.mediaBox)
    out.addPage(page)
    print('Croped and added to output file')

output = PdfFileWriter()

fnames = [] # копим сюда составные части имён файлов
out_name  = []; #отфильтрованные части имён файлов для выходного файла
fnrx = re.compile('[\s_\-]+');

for i in range(len(sys.argv)):
    if i > 0:
        if sys.argv[i] == 'backpage':
            backpage = True
        else:
            fnames.append(fnrx.split(sys.argv[i].split('\\').pop().split('.')[0]));
            append_file(output, sys.argv[i])

# фильруем части имён файлов
for fn in fnames:
    for k in range(len(fn)):
        if len(out_name) - 1 < k:
            out_name.append([]);
        if out_name[k].count(fn[k]) < 1:
            out_name[k].append(fn[k])
        #out_name[k].sort()
        #out_name[k].reverse();

for k in range(len(out_name)):
    if k == 0:
        out_name[k] = [datetime.date.today().strftime('%y%m%d')]
    out_name[k] = '_'.join(out_name[k]);

# собираем из отфильтрованных частей конечное имя файла
postfix  = '_crop'
if backpage:
    postfix  = '_backpage'
out_name = ('_'.join(out_name) + postfix)[0:251]+'.pdf';


print('')
print(out_name)
print("has %s pages" % output.getNumPages())
print('Saving...')

outputStream = file(out_name, "wb")
output.write(outputStream)
outputStream.close()

print('Done')
