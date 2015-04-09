#import moviepy.editor as me
#import importlib
#import os
import subprocess

def GetVideoSection(fileName, startTime, endTime):
    duration = endTime - startTime
    subprocess.call("ffmpeg -ss {start} -t {duration} -i {filen} {filen}_edited.mp4".format(start=startTime, duration=duration, filen=fileName), shell=True)
    
    #fvd = importlib.reload(me) #Moviepy crashes when converting a second video, workaround for now
    # Load file and select the subclip
    #clip = me.VideoFileClip(fileName).resize(width=1920, height=1080).subclip(startTime,endTime)
    
    #final_clip = me.CompositeVideoClip([clip])

    # write the result to a file in any format
    #final_clip.to_videofile(fileName+"_edited.mp4",fps=30)
    
    #statinfo = os.stat(fileName+'_edited.mp4')
    
    #newFPS = 30
    #while statinfo.st_size > 25000000:
    #    newFPS = newFPS - 5
    #    print("File is too big for e-mail, lowering fps")
    #    clip = me.VideoFileClip(fileName+'_edited.mp4')
    #    
    #    final_clip.to_videofile(fileName+"_edited.mp4",fps=newFPS)
    #    statinfo = os.stat(fileName+'_edited.mp4')
