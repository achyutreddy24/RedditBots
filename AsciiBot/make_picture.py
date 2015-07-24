#Code from here http://www.reddit.com/r/RequestABot/comments/2z6wbj/request_a_comment_screenshot_bot_for_ascii/cpg83tt

import os
import subprocess
import tkinter

def make_jpg(filename, output):
    filename_noext = filename
    filename_text = filename_noext + '.txt'
    filename_ghost = filename_noext + '_render.ps'
    filea = open(filename_text, 'r', encoding='utf-8')
    lines = filea.read()
    lines_split = lines.split('\n')
    lines_height = len(lines_split)
    lines_width = len(lines_split[0])
    print('%d x %d' % (lines_width, lines_height))
    lines_height *= 75
    lines_width *= 50
    filea.close()
    t = tkinter.Tk()
    c = tkinter.Canvas(t, width=lines_width, height=lines_height)
    c.pack()
    c.create_text(0, 0, text=lines, anchor="nw", font=("Courier New", 36))
    print('Writing Postscript')
    c.postscript(file=filename_ghost, width=lines_width, height=lines_height)
    t.destroy()
    print('Writing JPG')
    #Uses ImageMagick convert (should be installed on most linux systems and can be downloaded for windows(uses ghostscript))
    subprocess.call('convert {psfname} {pngfname}'.format(psfname=filename_ghost, pngfname=output+'.jpg'), shell=True)

make_jpg('test','test')
