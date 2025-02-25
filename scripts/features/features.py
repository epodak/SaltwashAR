# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from constants import *

class Features:

    # initialise features
    def __init__(self, config_provider):

        text_to_speech = None
        if (config_provider.acting or config_provider.browser or
            config_provider.calculator or config_provider.hand_gesture or
            config_provider.happy_colour or config_provider.mixing_desk or
            config_provider.optical_character_recognition or config_provider.play_your_cards_right or
            config_provider.slideshow or config_provider.weather):
            from texttospeech import TextToSpeech
            text_to_speech = TextToSpeech()

        speech_to_text = None
        if (config_provider.acting or config_provider.browser or
            config_provider.calculator or config_provider.mixing_desk or
            config_provider.phrase_translation or config_provider.play_your_cards_right or
            config_provider.weather):
            from speechtotext import SpeechToText
            speech_to_text = SpeechToText()

        self.acting = None
        if config_provider.acting:
            from acting import Acting
            self.acting = Acting(text_to_speech, speech_to_text)

        self.browser = None
        if config_provider.browser:
            from browser import Browser
            self.browser = Browser(text_to_speech, speech_to_text)

        self.calculator = None
        if config_provider.calculator:
            from calculator import Calculator
            self.calculator = Calculator(text_to_speech, speech_to_text)

        self.hand_gesture = None
        if config_provider.hand_gesture:
            from handgesture import HandGesture
            self.hand_gesture = HandGesture(text_to_speech)

        self.happy_colour = None
        if config_provider.happy_colour:
            from happycolour import HappyColour
            self.happy_colour = HappyColour(text_to_speech)

        self.mixing_desk = None
        if config_provider.mixing_desk:
            from mixingdesk import MixingDesk
            self.mixing_desk = MixingDesk(text_to_speech, speech_to_text)

        self.optical_character_recognition = None
        if config_provider.optical_character_recognition:
            from opticalcharacterrecognition import OpticalCharacterRecognition
            self.optical_character_recognition = OpticalCharacterRecognition(text_to_speech)

        self.phrase_translation = None
        if config_provider.phrase_translation:
            from phrasetranslation import PhraseTranslation
            self.phrase_translation = PhraseTranslation(speech_to_text)

        self.play_your_cards_right = None
        if config_provider.play_your_cards_right:
            from playyourcardsright import PlayYourCardsRight
            self.play_your_cards_right = PlayYourCardsRight(text_to_speech, speech_to_text)

        self.slideshow = None
        if config_provider.slideshow:
            from slideshow import Slideshow
            self.slideshow = Slideshow(text_to_speech)

        self.television = None
        if config_provider.television:
            from television import Television
            self.television = Television()

        self.weather = None
        if config_provider.weather:
            from weather import Weather
            self.weather = Weather(text_to_speech, speech_to_text)

    # indicate whether a feature is speaking
    def is_speaking(self):
        return ((self.acting and self.acting.is_speaking) or
                (self.browser and self.browser.is_speaking) or
                (self.calculator and self.calculator.is_speaking) or           
                (self.hand_gesture and self.hand_gesture.is_speaking) or
                (self.happy_colour and self.happy_colour.is_speaking) or                
                (self.mixing_desk and self.mixing_desk.is_speaking) or
                (self.optical_character_recognition and self.optical_character_recognition.is_speaking) or
                (self.phrase_translation and self.phrase_translation.is_speaking) or
                (self.play_your_cards_right and self.play_your_cards_right.is_speaking) or
                (self.slideshow and self.slideshow.is_speaking) or
                (self.weather and self.weather.is_speaking))

    # provide emotion from a feature
    def get_emotion(self):
        if self.acting: 
            return self.acting.emotion
        elif self.hand_gesture: 
            return self.hand_gesture.emotion
        elif self.happy_colour: 
            return self.happy_colour.emotion
        else:
            return None

    # update background image from a feature
    def update_background_image(self, image):
        if self.slideshow and self.slideshow.background_image.size > 0: 
            return self.slideshow.background_image  
        elif self.television and self.television.background_image.size > 0: 
            return self.television.background_image
        else:
            return image

    # handle features
    def handle(self, rocky_robot, sporty_robot, image):
        self._handle_acting(rocky_robot, sporty_robot)
        self._handle_browser(rocky_robot, sporty_robot)
        self._handle_calculator(rocky_robot, sporty_robot)
        self._handle_hand_gesture(rocky_robot, sporty_robot, image)
        self._handle_happy_colour(rocky_robot, image)
        self._handle_mixing_desk(rocky_robot)
        self._handle_optical_character_recognition(rocky_robot, sporty_robot, image)
        self._handle_phrase_translation(sporty_robot)
        self._handle_play_your_cards_right(sporty_robot)
        self._handle_slideshow(rocky_robot, sporty_robot, image)
        self._handle_television(rocky_robot, sporty_robot, image)
        self._handle_weather(rocky_robot, sporty_robot)

    # handle acting
    def _handle_acting(self, rocky_robot, sporty_robot):
        if not self.acting: return
 
        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.acting.start()
        else:
            self.acting.stop()

    # handle browser
    def _handle_browser(self, rocky_robot, sporty_robot):
        if not self.browser: return

        if rocky_robot.is_facing:
            self.browser.start(ROCK)
        elif sporty_robot.is_facing:
            self.browser.start(SPORT)
        else:
            self.browser.stop()

    # handle calculator
    def _handle_calculator(self, rocky_robot, sporty_robot):
        if not self.calculator: return
 
        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.calculator.start()
        else:
            self.calculator.stop()

    # handle hand gesture
    def _handle_hand_gesture(self, rocky_robot, sporty_robot, image):
        if not self.hand_gesture: return

        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.hand_gesture.start(image)
        else:
            self.hand_gesture.stop()

    # handle happy colour
    def _handle_happy_colour(self, rocky_robot, image):
        if not self.happy_colour: return

        if rocky_robot.is_facing:
            self.happy_colour.start(image)
        else:
            self.happy_colour.stop()

    # handle mixing desk
    def _handle_mixing_desk(self, rocky_robot):
        if not self.mixing_desk: return
 
        if rocky_robot.is_facing:
            self.mixing_desk.start()
        else:
            self.mixing_desk.stop()

    # handle optical character recognition
    def _handle_optical_character_recognition(self, rocky_robot, sporty_robot, image):
        if not self.optical_character_recognition: return

        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.optical_character_recognition.start(image)
        else:
            self.optical_character_recognition.stop()

    # handle phrase translation
    def _handle_phrase_translation(self, sporty_robot):
        if not self.phrase_translation: return

        if sporty_robot.is_facing:
            self.phrase_translation.start()
        else:
            self.phrase_translation.stop()

    # handle play your cards right
    def _handle_play_your_cards_right(self, sporty_robot):
        if not self.play_your_cards_right: return

        if sporty_robot.is_facing:
            self.play_your_cards_right.start()
        else:
            self.play_your_cards_right.stop()

    # handle slideshow
    def _handle_slideshow(self, rocky_robot, sporty_robot, image):
        if not self.slideshow: return

        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.slideshow.start(image)
        else:
            self.slideshow.stop()

    # handle television
    def _handle_television(self, rocky_robot, sporty_robot, image):
        if not self.television: return

        if rocky_robot.is_rendered or sporty_robot.is_rendered:
            self.television.start(image)
        else:
            self.television.stop()

    # handle weather
    def _handle_weather(self, rocky_robot, sporty_robot):
        if not self.weather: return

        if rocky_robot.is_facing or sporty_robot.is_facing:
            self.weather.start()
        else:
            self.weather.stop()