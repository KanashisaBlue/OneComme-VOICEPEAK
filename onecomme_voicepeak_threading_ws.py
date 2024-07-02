# Copyright (c) 2023 悲しさ（ https://x.com/KanashisaBlue ）
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

# わんコメ-VOICEPEAK 連携スクリプト（公開WebSocket API版 / わんコメ バージョン5以降をご利用ください）
# v2.0.2

import config
import json
import os
import re
import unicodedata
import subprocess
import asyncio
import websockets
import uuid
import time
import signal

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# websocket受信処理
async def ws_recv(websocket):

    try:
        print('読み上げが可能な状態です... このスクリプトを停止する場合は ctrl + c で停止してください')

        voice_volume = config.VOICE_VOLUME
        voice_speed = '100'
        voice_pitch = '0'

        #重複読み上げ対策用にコメントIDを保存していく
        read_ids = set()

        while True:
            
            #データを受信するまで待つ（ブロッキング）
            data = json.loads(await websocket.recv())

            if data['type'] == 'connected':

                if config.DEBUG_FLAG:
                    print('わんコネからの接続情報を確認しました')

                voice_volume = str(round(float(data['data']['config']['speech']['volume']) * 2.0 * float(config.VOICE_VOLUME), 2))

                if float(data['data']['config']['speech']['rate']) < 1.0:
                    voice_speed = str(round(100.0 - ((1.0 - float(data['data']['config']['speech']['rate'])) * 50.0 / 0.9)))
                else:
                    voice_speed = str(round(100.0 + ((float(data['data']['config']['speech']['rate'] - 1.0) * 100.0 / 2.5))))

                if float(data['data']['config']['speech']['pitch']) < 1.0:
                    voice_pitch = str(round(0.0 - float(1.0 - data['data']['config']['speech']['pitch']) * 300.0 / 0.9))
                else:
                    voice_pitch = str(round(float(data['data']['config']['speech']['pitch'] - 1.0) * 300.0))

                if config.DEBUG_FLAG:
                    print('わんコネの初期設定をしました')
                    print('読み上げボリューム：' + voice_volume)
                    print('読み上げ速度：' + voice_speed)
                    print('読み上げピッチ：' + voice_pitch)

            elif data['type'] == 'config':

                voice_volume = str(round(float(data['data']['speech']['volume']) * 2.0 * float(config.VOICE_VOLUME), 2))

                if float(data['data']['speech']['rate']) < 1.0:
                    voice_speed = str(round(100.0 - ((1.0 - float(data['data']['speech']['rate'])) * 50.0 / 0.9)))
                else:
                    voice_speed = str(round(100.0 + ((float(data['data']['speech']['rate'] - 1.0) * 100.0 / 2.5))))

                if float(data['data']['speech']['pitch']) < 1.0:
                    voice_pitch = str(round(0.0 - float(1.0 - data['data']['speech']['pitch']) * 300.0 / 0.9))
                else:
                    voice_pitch = str(round(float(data['data']['speech']['pitch'] - 1.0) * 300.0))

                if config.DEBUG_FLAG:
                    print('わんコネの設定変更を反映しました')
                    print('読み上げボリューム：' + voice_volume)
                    print('読み上げ速度：' + voice_speed)
                    print('読み上げピッチ：' + voice_pitch)

            elif data['type'] == 'comments':

                for commnent in data['data']['comments']:

                    #読み上げるファイル名で使用する
                    comment_id = str(uuid.uuid4())
                    
                    #送られてきたデータに読み上げるテキストがある場合のみ処理を行う
                    if 'speechText' in commnent['data']:

                        #コメントIDを出力
                        if config.DEBUG_FLAG:
                            print(commnent['data']['id'])

                        #重複読み上げを防ぐために過去に読み上げたコメントIDをチェック
                        if commnent['data']['id'] not in read_ids:

                            #コメントの感情の初期値
                            happy = '0'
                            sad = '0'
                            fun = '0'
                            angry = '0'

                            #タグの削除（絵文字や不具合文字なども含む）
                            read_comment = str(commnent['data']['speechText']).replace('&lt;', '<').replace('&gt;', '>')
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

                            #絵文字から感情データを追加
                            if '😊' in read_comment:
                                happy = '100'
                            if '😢' in read_comment:
                                sad = '100'
                            if '😆' in read_comment:
                                fun = '100'
                            if '😡' in read_comment:
                                angry = '100'

                            #読み上げファイル作成コマンド作成
                            read_command = config.VOICEPEAK_APP_FILEPATH + ' -s "' + read_comment + '" --speed ' + voice_speed  + ' --pitch ' + voice_pitch + ' -o ' + config.OUTPUT_VOICE_DIRPATH + '/vp_' + comment_id + '.wav -n "' + config.VOICE_NARRATOR + '"' + ' -e happy=' + happy + ',sad=' + sad + ',fun=' + fun + ',angry=' + angry 
                            if config.DEBUG_FLAG:
                                print(read_command)

                            #読み上げファイル作成
                            for i in range(config.MAX_RETRY):
                                if config.DEBUG_FLAG:
                                    #read_command_result = 1 #失敗テスト用
                                    read_command_result = subprocess.call([read_command], shell = True)
                                else:
                                    read_command_result = subprocess.call([read_command], shell = True, stderr = subprocess.PIPE)

                                if read_command_result == 0:
                                    #キューに追加する（別スレッドでデキューする）
                                    comment_que.put((comment_id, voice_volume))

                                    #コメントIDを保存
                                    read_ids.add(commnent['data']['id'])
                                    break
                                elif i == config.MAX_RETRY - 1:
                                    if config.DEBUG_FLAG:
                                        print('ファイル作成失敗 ' + str(i + 1) + '回目')
                                    comment_que.put((comment_id, voice_volume))
                                    break
                                else:
                                    if config.DEBUG_FLAG:
                                        print('ファイル作成失敗 ' + str(i + 1) + '回目')
                                        print(read_command)
                                    time.sleep(0.5)

                    else:
                        if config.DEBUG_FLAG:
                            print('わんコメの読み上げが有効になっていません : ' + commnent['service'])
            
    except Exception as e:
        print('このスクリプトの異常動作もしくはわんコメのアプリケーション終了を検知しました。このスクリプトをctrl + cで終了してください')
        print(f"\"{e}\"")

# websocket接続処理
async def ws_connect():
    
    try:
        async with websockets.connect("ws://127.0.0.1:11180/sub") as websocket: #固定のため直書き
            print('わんコメとの接続が完了しました。')
            await ws_recv(websocket)

    except Exception as e:
        print('WebSocketの接続ができません。このスクリプトをctrl + cで一度終了し、わんコメを立ち上げてから再度起動してください。')
        print(f"\"{e}\"")

# 音声データ作成用スレッド用関数
def func_make():

    asyncio.run(ws_connect())
    exit() #ここまで処理は来ない

#音声データ読み上げ用スレッド用関数
def func_read():

    #キューに入ってるファイルを一つづつ読み上げる
    while True:

        #コメントのキューを取得するまで待つ（キューが空になるとブロッキング）
        comment_tuple = comment_que.get()

        #読み上げファイル存在チェック
        read_file_path = config.OUTPUT_VOICE_DIRPATH + '/vp_' + str(comment_tuple[0]) + '.wav'
        is_file = os.path.isfile(read_file_path)

        #読み上げ音量
        read_volume = comment_tuple[1];

        if is_file:
            if config.DEBUG_FLAG:
                subprocess.call([config.AFPLAY_FILEPATH + ' ' + read_file_path + ' -v ' + read_volume], shell = True)
            else:
                subprocess.call([config.AFPLAY_FILEPATH + ' ' + read_file_path + ' -v ' + read_volume], shell = True, stderr = subprocess.PIPE)

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
                    subprocess.call([config.AFPLAY_FILEPATH + ' ' + config.EXCEPTION_OUTPUT_VOICE_FILEPATH + ' -v ' + read_volume], shell = True)
                else:
                    subprocess.call([config.AFPLAY_FILEPATH + ' ' + config.EXCEPTION_OUTPUT_VOICE_FILEPATH + ' -v ' + read_volume], shell = True, stderr = subprocess.PIPE)
            else:
                if config.DEBUG_FLAG:
                    print('読み上げができなかった場合（エラー等）に読み上げるwavファイルがないので無音です。読み上げ失敗用のwavファイルを用意し、.envのEXCEPTION_OUTPUT_VOICE_FILEPATHを設定してください')

#メイン処理
if __name__ == '__main__':

    #ctrl+cでスクリプト終了
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    #コメントデータキュー
    comment_que = Queue()

    print('スクリプト起動...')
    with ThreadPoolExecutor() as executor:
        executor.submit(func_make) #コメント音声データ作成スレッド
        executor.submit(func_read) #コメント読み上げ処理スレッド

    #通常はここまで処理は来ない
    print('スレッド関連のエラー発生')
