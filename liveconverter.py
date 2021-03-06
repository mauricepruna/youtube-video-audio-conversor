import os, shutil
import sys
import configparser
from youtube_dl import YoutubeDL, DateRange
from datetime import date, timedelta


def youtube_converter():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    channels = config.sections()

  

    for channel in channels:

        channel_url = config[channel]['channel_url']
        number_of_days = config[channel]['number_of_days']
        quality = config[channel]['quality']
        if channel_url and number_of_days and quality:
        
            today = date.today()
            before = today - timedelta(days=int(number_of_days))
            datebefore = today.strftime("%Y%m%d")
            dateafter = before.strftime("%Y%m%d")
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality
                }],
                'ignoreerrors':"True",
                'outtmpl': './download/%(uploader)s-%(title)s-%(upload_date)s.%(ext)s',
                'restrictfilenames':"True",
                'download_archive' : 'downloadedVideos.txt',
                'daterange': DateRange(dateafter, datebefore),
                'playlistend': 10
            }
            ydl = YoutubeDL(ydl_opts)
            ydl.download([channel_url])

        
        else:
            print("Missing one of the configurations needed:\n channel:{channel} url:{url} days:{days} quality:{qual} ".format(channel=channel, url=channels, days=number_of_days, qual=quality))
            exit(0)

def folder_cleaner():
    folder = './download'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
if __name__ == '__main__':

    folder_cleaner()
    youtube_converter()

    