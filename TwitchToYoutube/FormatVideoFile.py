from moviepy.editor import *
#Import Settings from Config.py
try:
    import Config
    FPS = Config.FPS
except ImportError:
    print("Error Importing Config.py")


def GetVideoSection(fileName, startTime, endTime):
    # Load file and select the subclip
    clip = VideoFileClip(fileName).subclip(startTime,endTime)
    
    final_clip = CompositeVideoClip([clip])

    # write the result to a file in any format
    final_clip.to_videofile(fileName+"_edited.mp4",fps=FPS)