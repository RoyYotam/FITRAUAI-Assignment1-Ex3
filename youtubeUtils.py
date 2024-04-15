from pytube import Search, exceptions


class YoutubeUtils:
    def __init__(self, os_utils_manager, log=False):
        self.os_utils_manager = os_utils_manager
        self.ten_minutes = 600
        self.log = log

    # Download the top video under 10 minutes
    def download_video(self, search_query):
        search = Search(search_query)

        for video in search.results:
            if video.length < self.ten_minutes:
                file_path_and_folder_and_file_names = self.os_utils_manager.get_full_path(search_query, video.title)
                if self.log:
                    print(f"Downloading video: {video.title}")
                    print(f"file's path: {file_path_and_folder_and_file_names[0]}")

                try:
                    video.streams.get_highest_resolution().download(output_path=file_path_and_folder_and_file_names[1][0],
                                                                    filename=file_path_and_folder_and_file_names[1][1])
                    return file_path_and_folder_and_file_names[0]
                except exceptions as e:
                    pass
                    # ("Video is restricted, and can't be downloaded.")

        return None

    @staticmethod
    def suggest(search_query):
        try:
            return Search(search_query).completion_suggestions
        except Exception:
            return []
