import threading

import pygame
import webbrowser
import os
import time
from youtubeUtils import YoutubeUtils
from osUtils import OsUtils
from sceneUtils import SceneUtils
import random


class SimplePygamePage:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 500, 400
        self.TEXT_COLOR = (255, 255, 255)
        self.TEXTBOX_USED_COLOR = (0, 255, 0)
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.GIF_BUTTON_COLOR = (0, 0, 255)
        self.SUGGESTION_COLOR = (120, 120, 120)

        # Set up the display window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Youtube video summarizer")

        # Load a sample GIF image
        self.gif_path = "downloads/mario game/summary.gif"

        # Font for text input
        self.font = pygame.font.Font(None, 32)

        # Initialize text input
        self.text_input = ""
        self.instructions_text = "Please enter a subject for the video:"

        self.gif_button_rect = None

        # Flag and variables for controlling GIF display
        self.last_show_time = 0
        self.gif_display_interval = 5  # Interval in seconds between GIF displays

        self.suggestion_button_rect = pygame.Rect(440, 50, 30, 40)
        self.suggestions = []
        self.result = ""
        self.processing = False

        # Variables for gif maker
        self.os_utils_manager = OsUtils()
        self.youtube_utils_manager = YoutubeUtils(self.os_utils_manager)

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_text_input_box()
        self.draw_suggestion_button()
        self.show_suggestion_results()
        self.show_text_input()
        self.show_button()
        self.draw_result()
        pygame.display.flip()

    def draw_text_input_box(self):
        text_surface = self.font.render(self.instructions_text, True, self.TEXT_COLOR)
        self.screen.blit(text_surface, (30, 20))
        textbox_color = self.TEXTBOX_USED_COLOR if len(self.text_input) > 0 else self.TEXT_COLOR
        pygame.draw.rect(self.screen, textbox_color, (30, 50, 400, 40), 2)

    def draw_suggestion_button(self):
        pygame.draw.rect(self.screen, self.TEXT_COLOR, self.suggestion_button_rect)
        button_text = self.font.render("+", True, self.BACKGROUND_COLOR)
        self.screen.blit(button_text, (450, 57))

    def show_suggestion_results(self):
        y = 95
        suggestion_font = pygame.font.Font(None, 20)

        for suggest in self.suggestions[:5]:
            button_text = suggestion_font.render(suggest, True, self.SUGGESTION_COLOR)
            self.screen.blit(button_text, (30, y))
            y += 15

    def show_text_input(self):
        text_surface = self.font.render(self.text_input, True, self.TEXT_COLOR)
        self.screen.blit(text_surface, (35, 55))

    def show_button(self):
        self.gif_button_rect = pygame.Rect(130, 180, 200, 40)
        pygame.draw.rect(self.screen, self.GIF_BUTTON_COLOR, self.gif_button_rect)
        button_text = self.font.render("Show GIF", True, self.TEXT_COLOR)
        self.screen.blit(button_text, (180, 190))

    def draw_result(self):
        y = 240
        result_font = pygame.font.Font(None, 24)

        for result_line in self.split_result_text():
            text_surface = result_font.render(result_line, True, self.SUGGESTION_COLOR)
            self.screen.blit(text_surface, (30, y))
            y += 20

    def split_result_text(self):
        line_length = 50
        return [self.result[i: i + line_length] for i in range(0, len(self.result), line_length)]

    def show_gif(self):
        try:
            # Get the absolute path of the GIF file
            gif_abs_path = os.path.abspath(self.gif_path)
            # Use webbrowser to open the GIF file in the default web browser
            webbrowser.open(f"file://{gif_abs_path}")
        except Exception as e:
            print(f"Error opening GIF in web browser: {e}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(self.text_input) > 0:
                        if not self.processing:
                            self.processing = True
                            my_thread = threading.Thread(target=self.make_gif)
                            my_thread.start()

                elif len(self.text_input) < 20:
                    self.text_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.gif_button_rect.collidepoint(mouse_pos):
                    if not self.processing:
                        self.processing = True
                        my_thread = threading.Thread(target=self.make_gif)
                        my_thread.start()
                elif self.suggestion_button_rect.collidepoint(mouse_pos):
                    if not self.processing and len(self.text_input) > 0:
                        self.suggestions = YoutubeUtils.suggest(self.text_input)
                        random.shuffle(self.suggestions)

        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()

        pygame.quit()

    def make_gif(self):
        self.result = "processing..."

        if len(self.text_input) > 0:
            video_path = self.youtube_utils_manager.download_video(self.text_input)
            if video_path:
                scene_utils_manager = SceneUtils(video_path, self.os_utils_manager)
                self.result, self.gif_path = scene_utils_manager.create_gif()
            else:
                self.result = 'Subject length should be 1 -> 20.'

            self.text_input = ""
            self.suggestions = []

            self.show_gif()
        else:
            self.result = 'Subject length should be 1 -> 20.'

        self.processing = False

