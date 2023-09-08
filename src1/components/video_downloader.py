import os,sys
import requests
from pytube import YouTube

from src1.exception import CustomException
from src1.logger import logger

class VideoDownloader:
    def __init__(self,url:str, save_path:str):
        self.url=url
        self.save_path=save_path

    def download(self) ->str | None:

        try:
            if 'youtu' in self.url:
                return self._download_youtube()
            else:
                return self._download_other()
        except Exception as e:
            raise CustomException(e,sys)

    def _download_youtube(self) ->str:

        try:
            yt=YouTube(self.url)
            video=yt.streams.first()
            video.download(self.save_path)
            logger.info(f"Youtube Video downloaded to {os.path.join(self.save_path,video.default_filename)}")
            return os.path.join(self.save_path,video.default_filename)
        except Exception as e:
            raise CustomException(e,sys)

    def _download_other(self)  ->str:

        try:
            response=requests.get(self.url,stream=True)
            filename=self.url.split("/")[-1]
            with open(os.path.join(self.save_path,f"{filename}"),"wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)
            logger.info(f"Video Downloaded to {os.path.join(self.save_path,filename)}")
            return os.path.join(self.save_path,filename)
        except Exception as e:
            raise CustomException(e,sys)                      