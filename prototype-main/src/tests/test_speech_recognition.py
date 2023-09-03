import unittest
import sys
sys.path.append('/Smodal/prototype-main/src')
import speech_recognition

class TestSpeechRecognition(unittest.TestCase):

    def setUp(self):
        self.sr = speech_recognition

    def test_speech_to_text(self):       
        # test with a sample audio input
        # assuming the audio's text is "hello world"
        self.assertEqual(self.sr.speech_to_text("sample_audio.wav"), "hello world")

    def test_text_to_speech(self):
        # test with a sample text
        self.sr.text_to_speech("hello world")
        # check if the file "welcome.mp3" exists
        self.assertTrue(os.path.exists("welcome.mp3"))

if __name__ == '__main__':
    unittest.main()