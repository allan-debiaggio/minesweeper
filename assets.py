import pygame

class Assets:
    def __init__(self):
        self.audio_files = {}
        self.image_files = {}

    def load_audio(self, audio_dict):
        """
        Load audio files into the asset manager.
        :param audio_dict: A dictionary where keys are event names and values are file paths.
        """
        for event_name, file_path in audio_dict.items():
            try:
                self.audio_files[event_name] = pygame.mixer.Sound(file_path)
            except pygame.error:
                self.audio_files[event_name] = None  # Handle missing audio files gracefully

    def play_audio(self, event_name):
        """
        Play the audio for a specific event.
        :param event_name: The name of the event (e.g., 'click', 'flag').
        """
        sound = self.audio_files.get(event_name)
        if sound:
            sound.play()

    def load_images(self, image_dict):
        self.image_files.update(image_dict)

    def get_image(self, image_name, fallback_assets=None):
        image_path = self.image_files.get(image_name, None)
        if image_path is None and fallback_assets:
            return fallback_assets.get_image(image_name)
        return image_path

class ClassicAssets(Assets):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()  # Initialize pygame mixer

        # Load audio files
        self.load_audio({
            'click': 'assets/sound/classic/Click.mp3',
            'flag': 'assets/sound/classic/Flag.mp3',
            'mine': 'assets/sound/classic/Mine.mp3',
            'hover': 'assets/sound/classic/Hover.mp3',
            'questionmark': 'assets/sound/classic/Questionmark.mp3',
            'game_over': 'assets/sound/classic/Game_Over.mp3',
            'victory': 'assets/sound/classic/Victory.mp3'
        })