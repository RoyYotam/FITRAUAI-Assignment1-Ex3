import osUtils
from scenedetect.backends.opencv import VideoStreamCv2
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector
import cv2
from easyocr import Reader
from PIL import Image, ImageDraw


class SceneUtils:
    def __init__(self, video_path, os_utils_manager, log=False):
        self.video_path = video_path
        self.scenes = []
        self.images = []
        self.images_with_watermark = []
        self.text = []
        self.os_utils_manager = os_utils_manager
        self.log = log
        self.watermark_text = 'Roy Yotam'
        self.watermark_color = (255, 255, 255)

    # Scene detection
    def detect_scenes(self):
        if osUtils.OsUtils.is_video_path_valid_with_warning(self.video_path):
            video_manager = VideoStreamCv2(self.video_path)
            scene_manager = SceneManager()
            scene_manager.add_detector(ContentDetector())

            scene_manager.detect_scenes(frame_source=video_manager, show_progress=False)

            self.scenes = scene_manager.get_scene_list()

            if self.log:
                print(f"{len(self.scenes)} scenes were found.")

    # Extract frames and perform OCR
    def extract_text_from_scenes(self):
        cap = cv2.VideoCapture(self.video_path)
        reader = Reader(['en'])
        self.os_utils_manager.create_images_folder()

        for i, (start, end) in enumerate(self.scenes):
            # Calculate the midpoint time of the scene
            midpoint_time = (start.get_seconds() + end.get_seconds()) / 2
            cap.set(cv2.CAP_PROP_POS_MSEC, midpoint_time * 1000)

            ret, frame = cap.read()
            if ret:
                # Convert the frame from BGR to RGB
                frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Generate a filename for the image (e.g., scene_001.jpg)
                image_filename = f"scene_{i+1:03d}.jpg"
                image_path = self.os_utils_manager.image_path(image_filename)

                # Save the image to the output folder
                self.images.append([frame_image, image_path])
                # frame_image.save(image_path)

                if self.log:
                    print(f"{image_filename} was saved.")

                # Uncomment this part if you want to extract text from the frame using 'reader'
                # text = reader.readtext(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                # self.texts.append(" ".join([t[1] for t in text]))

        cap.release()  # Release the video capture
        self.watermark_and_save_images()

    # Watermark and save images
    def watermark_and_save_images(self):
        for img, path in self.images:
            draw = ImageDraw.Draw(img)
            width, height = img.size
            text_width, text_height = draw.textsize(self.watermark_text)
            position = (width - (1.5 * text_width), height - (1.5 * text_height))
            draw.text(position, self.watermark_text, self.watermark_color)
            img.save(path)
            self.images_with_watermark.append(img)

    # Create GIF
    def create_gif(self, filename="summary.gif"):
        self.detect_scenes()
        self.extract_text_from_scenes()

        self.images_with_watermark[0].save(
            self.os_utils_manager.gif_path(filename), save_all=True, append_images=self.images_with_watermark[1:], optimize=False, duration=100, loop=0
        )

        if self.log:
            print(f"{filename} was created!")

