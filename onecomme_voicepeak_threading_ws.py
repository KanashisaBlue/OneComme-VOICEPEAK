# Copyright (c) 2023 悲しさ（ https://x.com/KanashisaBlue ）
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

# わんコメ-VOICEPEAK 連携スクリプト
# v1.0.0

import config
import json
import os
import re
import unicodedata
import subprocess
import pandas as pd
import asyncio
import websockets
import uuid
import time
import signal

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# websocket受信処理
async def ws_recv(websocket):

    #アスキーアートインデックス用（関数内関数）
    def SetIndexLen(row):
        row[3] = len(row.name)
        return row

    #アスキーアートを消す（関数内関数）
    def StrAAReplace(str):
        for index, item in aadb_df.iterrows():
            if str.count(index) > 0:
                str = str.replace(index, item.values[0])
        return str

    try:
        #AA読み上げ用データを作成
        is_aafile = os.path.isfile(config.AA_DB_FILEPATH)
        if is_aafile:
            aadb_df = pd.read_table(config.AA_DB_FILEPATH, header = None, index_col = 1)
            aadb_df = aadb_df.apply(SetIndexLen, axis = 1)
            aadb_df = aadb_df.sort_values(3, ascending = False)

        print('読み上げが可能な状態です... このスクリプトを停止する場合は ctrl + c で停止してください')
        while True:
            data = json.loads(await websocket.recv())

            #取得したデータをコンソールに表示（デバッグモードのみ）
            if config.DEBUG_FLAG:
                print(data)

            #受信データごとに処理を分ける
            if data['operation'] == 'speech.getVoiceList':
                try:
                    await websocket.send('{"operation":"speech.getVoiceList","status":"success","id":"speech.getVoiceList","voice":["悲しさ独自スクリプト"]}')
                except:
                    if config.DEBUG_FLAG:
                        print('except error....')

            elif data['operation'] == 'translate':
                await websocket.send('{"operation":"translate","params":[{"id":"hU0a-NZE","lang":"en_US","text":"おはようございます"}]}')

            elif data['operation'] == 'speech':

                #idを決める
                comment_id = str(uuid.uuid4())

                #タグの削除（絵文字や不具合文字なども含む）
                if is_aafile:
                    read_comment = StrAAReplace(str(data["params"][0]["text"]).replace('&lt;', '<').replace('&gt;', '>'))
                else:
                    read_comment = str(data["params"][0]["text"]).replace('&lt;', '<').replace('&gt;', '>')
                read_comment = re.compile(r"<[^>]*?>").sub(' 略 ', read_comment)
                read_comment = read_comment.replace("｀", "")
                read_comment = read_comment.replace("`", "")
                read_comment = read_comment.replace("\\", " ")

                #半角カタカナを全角カタカナに
                read_comment = unicodedata.normalize('NFKC', read_comment)

                #コメントの改行やコーテーションを削除
                read_comment = read_comment.replace('\n', ' ').replace('&quot;', ' ').replace('&#39;', ' ').replace('"', ' ')

                #URL省略
                read_comment = re.sub('https?://[A-Za-z0-9_/:%#$&?()~.=+-]+?(?=https?:|[^A-Za-z0-9_/:%#$&?()~.=+-]|$)', ' URL略 ', read_comment)

                #読み上げが長くなる場合は省略
                if len(read_comment) > config.MAX_READ_COMMENTSTRING_NUM:
                    read_comment = read_comment[:config.MAX_READ_COMMENTSTRING_NUM] + '、以下略'

                #読み上げファイル作成コマンド作成
                read_command = config.VOICEPEAK_APP_FILEPATH + ' -s "' + read_comment + '" --speed ' + config.VOICE_SPEED + ' -o ' + config.OUTPUT_VOICE_DIRPATH + '/vp_' + comment_id + '.wav -n "' + config.VOICE_NARRATOR + '"'

                #読み上げファイル作成
                for i in range(config.MAX_RETRY):
                    if config.DEBUG_FLAG:
                        #read_command_result = 1 #失敗テスト用
                        read_command_result = subprocess.call([read_command], shell = True)
                    else:
                        read_command_result = subprocess.call([read_command], shell = True, stderr = subprocess.PIPE)

                    if read_command_result == 0:
                        #キューに追加する（別スレッドでデキューする）
                        comment_que.put(comment_id)
                        break
                    elif i == config.MAX_RETRY - 1:
                        if config.DEBUG_FLAG:
                            print('ファイル作成失敗 ' + str(i + 1) + '回目')
                        comment_que.put('__commentfile_make_faild')
                        break
                    else:
                        if config.DEBUG_FLAG:
                            print('ファイル作成失敗 ' + str(i + 1) + '回目')
                            print(read_command)
                        time.sleep(0.5)

                #一応、クライアントに返す（意味ないカモだけど）
                await websocket.send('{"operation":"speech","status":"sended","id":"' + comment_id + '","text":"' + str(data["params"][0]["text"]) + '","talker":"' + str(data["params"][0]["talker"]) + '"}')

    except Exception as e:
        print(f"わんコメの終了を検知しました。このスクリプトをctrl + cで終了してください。\"{e}\"")

# websocket接続処理
async def ws_connect():
    
    try:
        async with websockets.serve(ws_recv, "localhost", config.WEBSOCKET_PORT):
            await asyncio.Future()

    except Exception as e:
        print(f"websocketの接続ができません。このスクリプトをctrl + cで終了してください。\"{e}\"")

# 音声データ作成用スレッド用関数
def func_make():

    asyncio.run(ws_connect())
    exit() #ここまで処理は来ない

#音声データ読み上げ用スレッド用関数
def func_read():

        #キューに入ってるファイルを一つづつ読み上げる
        while True:

            #読み上げファイル存在チェック
            read_file_path = config.OUTPUT_VOICE_DIRPATH + '/vp_' + str(comment_que.get()) + '.wav'
            is_file = os.path.isfile(read_file_path)

            if is_file:
                if config.DEBUG_FLAG:
                    subprocess.call([config.AFPLAY_FILEPATH + ' ' + read_file_path + ' -v ' + str(config.VOICE_VOLUME)], shell = True)
                else:
                    subprocess.call([config.AFPLAY_FILEPATH + ' ' + read_file_path + ' -v ' + str(config.VOICE_VOLUME)], shell = True, stderr = subprocess.PIPE)

                #読み上げファイルを削除
                os.remove(read_file_path)

            #ファイルが存在しない場合はエラーメッセージを読み上げる
            else:
                if config.DEBUG_FLAG:
                    print('読み上げ実行失敗。以下のファイルが存在していません')
                    print(read_file_path)
                
                is_file = os.path.isfile(config.EXCEPTION_OUTPUT_VOICE_FILEPATH)
                if is_file:
                    if config.DEBUG_FLAG:
                        subprocess.call([config.AFPLAY_FILEPATH + ' ' + config.EXCEPTION_OUTPUT_VOICE_FILEPATH + ' -v ' + str(config.VOICE_VOLUME)], shell = True)
                    else:
                        subprocess.call([config.AFPLAY_FILEPATH + ' ' + config.EXCEPTION_OUTPUT_VOICE_FILEPATH + ' -v ' + str(config.VOICE_VOLUME)], shell = True, stderr = subprocess.PIPE)
                else:
                    if config.DEBUG_FLAG:
                        print('読み上げができなかった場合（エラー等）に読み上げるwavファイルがないので無音です。読み上げ失敗用のwavファイルを用意し、.envのEXCEPTION_OUTPUT_VOICE_FILEPATHを設定してください')

#メイン処理
if __name__ == '__main__':

    #ctrl+cでスクリプト終了
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #コメントデータキュー
    comment_que = Queue()

    print('スクリプト起動... 読み上げ開始まで最大30秒程度おまちください...')
    with ThreadPoolExecutor() as executor:
        executor.submit(func_make) #コメント音声データ作成スレッド
        executor.submit(func_read) #コメント読み上げ処理スレッド

    #通常はここまで処理は来ない
    print('スレッド関連のエラー発生')
