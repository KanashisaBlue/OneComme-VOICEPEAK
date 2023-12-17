# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
from setuptools._distutils.util import strtobool

load_dotenv(override = True)

# 環境変数を参照
import os
VOICE_NARRATOR = os.getenv('VOICE_NARRATOR')
VOICE_VOLUME = os.getenv('VOICE_VOLUME')

DEBUG_FLAG = bool(strtobool(os.getenv('DEBUG_FLAG')))
EXCEPTION_OUTPUT_VOICE_FILEPATH = os.getenv('EXCEPTION_OUTPUT_VOICE_FILEPATH')
MAX_RETRY = int(os.getenv('MAX_RETRY'))
VOICEPEAK_APP_FILEPATH = os.getenv('VOICEPEAK_APP_FILEPATH')
AFPLAY_FILEPATH = os.getenv('AFPLAY_FILEPATH')
OUTPUT_VOICE_DIRPATH = os.getenv('OUTPUT_VOICE_DIRPATH')
