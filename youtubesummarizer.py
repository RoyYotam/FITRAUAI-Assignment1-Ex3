import youtubeUtils
import sceneUtils
import osUtils


def main():
    os_utils_manager = osUtils.OsUtils()
    youtube_utils_manager = youtubeUtils.YoutubeUtils(os_utils_manager)
    query = input("Please enter a subject for the video").strip()

    if 50 < len(query) < 2:
        print('Subject length should be 1 -> 50.')
    else:
        video_path = youtube_utils_manager.download_video(query)
        if video_path:
            scene_utils_manager = sceneUtils.SceneUtils(video_path, os_utils_manager)
            # watermark_images(images, "Your Name Here")
            scene_utils_manager.create_gif()
            # print(" ".join(texts))
        else:
            print("No suitable video found.")


if __name__ == "__main__":
    main()
