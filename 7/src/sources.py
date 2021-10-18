import cv2
from abc import ABC, abstractmethod

class Source(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setHeight(self, height):
        self.height = height

    def setWidth(self, width):
        self.width = width

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    @abstractmethod
    def getImage(self):
        pass

class VideoSource(Source):
    def __init__(self, filename):
        super().__init__()
        self.source = cv2.VideoCapture(filename)
        self.height = int(self.source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width  = int(self.source.get(cv2.CAP_PROP_FRAME_WIDTH))

    def getImage(self):
        _, frame = self.source.read()
        return cv2.resize(frame, (self.width, self.height))


class ImageSource(Source):
    def __init__(self, filename):
        super().__init__()
        self.source = cv2.imread(filename)
        self.height = self.source.shape[0]
        self.width  = self.source.shape[1]

    def setHeight(self, height):
        super().setHeight(height)
        self.source = cv2.resize(self.source, (self.width, self.height))

    def setWidth(self, width):
        super().setWidth(width)
        self.source = cv2.resize(self.source, (self.width, self.height))

    def getImage(self):
        return self.source


def sourceFabric(filename):
    if filename.endswith("mp4"):
        return VideoSource(filename)
    elif filename.endswith("jpg"):
        return ImageSource(filename)
    else:
        raise Exception("wrong file format")