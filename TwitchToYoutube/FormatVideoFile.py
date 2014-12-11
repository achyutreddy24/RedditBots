from moviepy.editor import *


def GetVideoSection(fileName, startTime, endTime):
    # Load file and select the subclip 00:00:50 - 00:00:60
    clip = VideoFileClip(fileName).subclip(startTime,endTime)

    # write the result to a file in any format
    final_clip.to_videofile(fileName+"_edited",fps=30)