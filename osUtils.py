import os
import re


class OsUtils:
    def __init__(self, log=False):
        self.downloads_folder_path = 'downloads'
        self.video_folder_path = 'downloads'
        self.images_folder_path = 'downloads'
        self.images_folder = 'images'
        self.video_name = 'unnamed_file'
        self.log = log

    def create_folder_if_not_exists(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
            self.log_if_allow(f"Folder created:\n{path}")

    def downloads_folder_validate(self):
        self.create_folder_if_not_exists(self.downloads_folder_path)

    def create_subject_folder(self, subject):
        self.downloads_folder_validate()

        self.video_folder_path = os.path.join(self.downloads_folder_path, subject)
        self.create_folder_if_not_exists(self.video_folder_path)

    def get_valid_name_from_subject(self, subject, replacement='_'):
        # Characters that are not allowed in filenames across most operating systems
        illegal_chars = r'[\/:*?"<>|\'\.]'

        # Replace illegal characters with the replacement character
        valid_filename = re.sub(illegal_chars, replacement, subject)

        # Remove leading and trailing spaces and dots
        valid_filename = valid_filename.strip(' .')

        # Ensure filename is not empty after stripping
        if valid_filename:
            self.video_name = valid_filename

        return self.video_name

    def get_file_path(self):
        return os.path.join(self.video_folder_path, self.video_name_with_type())

    def video_name_with_type(self):
        return f"{self.video_name}.mp4"

    def get_full_path(self, subject, video_name):
        name = self.get_valid_name_from_subject(subject)
        self.create_subject_folder(name)
        self.get_valid_name_from_subject(video_name)
        return [self.get_file_path(), [self.video_folder_path, self.video_name_with_type()]]

    def create_images_folder(self):
        self.images_folder_path = os.path.join(self.video_folder_path, self.images_folder)
        self.create_folder_if_not_exists(self.images_folder_path)

    def image_path(self, image_name):
        return os.path.join(self.images_folder_path, image_name)

    def gif_path(self, gif_name):
        return os.path.join(self.video_folder_path, gif_name)

    @ staticmethod
    def is_video_path_valid_with_warning(path):
        if os.path.exists(path):
            return True
        else:
            print(f"Video file not found at: {path}")
            return False

    def log_if_allow(self, message):
        if self.log:
            print(message)
