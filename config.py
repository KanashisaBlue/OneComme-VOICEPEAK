# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
from setuptools._distutils.util import strtobool

load_dotenv(override = True)

# 環境変数を参照
import os
VOICE_VOLUME = os.getenv('VOICE_VOLUME')
VOICE_SPEED = os.getenv('VOICE_SPEED')
VOICE_NARRATOR = os.getenv('VOICE_NARRATOR')
MAX_READ_COMMENTSTRING_NUM = int(os.getenv('MAX_READ_COMMENTSTRING_NUM'))

DEBUG_FLAG = bool(strtobool(os.getenv('DEBUG_FLAG')))
AA_DB_FILEPATH = os.getenv('AA_DB_FILEPATH')
EXCEPTION_OUTPUT_VOICE_FILEPATH = os.getenv('EXCEPTION_OUTPUT_VOICE_FILEPATH')
MAX_RETRY = int(os.getenv('MAX_RETRY'))
VOICEPEAK_APP_FILEPATH = os.getenv('VOICEPEAK_APP_FILEPATH')
AFPLAY_FILEPATH = os.getenv('AFPLAY_FILEPATH')
OUTPUT_VOICE_DIRPATH = os.getenv('OUTPUT_VOICE_DIRPATH')
WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT'))