# OneComme-VOICEPEAK

# Overview

コメントビューアのわんコメと、読み上げソフトのVOICEPEAKを連携するPythonスクリプトです。  
わんコメのコメントの読み上げをVOICEPEAKのキレイな読み上げで読ませることができます。  

Windowsを利用されている方は「ゆかコネNEO」を利用された方が手軽かと思いますので、そちらをご利用ください。  
https://nmori.github.io/yncneo-Docs/

このPythonスクリプトはゆかコネNEOが利用できない環境（主にMacOS）での利用を想定しています。  

# Caution

このPythonスクリプトを利用することによって発生したことによるトラブルや損害等に関して、当方は一切の責任を負いません。自己責任の下でご利用ください。  

このPythonスクリプトはわんコメ、VOICEPEAKともに非公認の野良スクリプトです。両運営に対してこのPythonスクリプトに関する問い合わせなどはお控えください。 

両アプリのいずれかでバージョンアップ等による仕様変更が起きた場合、急に動かなくなる恐れがあります。バージョンアップを契機にして動かなくなった場合は、このページの最下部にある連絡先からアプリケーションのバージョン情報と合わせてご連絡ください。

# Environment

#### MacOS（64bit）  
Intel CPUのMacOS上にて動作確認を行っていますが、AppleシリコンのMacOS上でもたぶん動作します。  

#### ■Python（3.11系以降）
動作確認できているのはバージョン3.12.1とバージョン3.11.6です。  
おそらくバージョン3.11以降で動作すると思いますが、動作確認できている3.11.6以降をお勧めします。  
MacOS標準で入ってるPythonはバージョンが古いので、3.11系以降のPythonを別途インストールしてください。  
インストーラーで入れる方法もあるようですが、pyenvを使って入れる方法の方が後々の管理も楽ですので、個人的にはこちらをお勧めします。  
（インストーラー版Pythonでは動作確認していません）

以下のPythonライブラリの導入は必須ですので、pipコマンド等でインストールお願いします。

- python-dotenv
- setuptools
- websockets

# Requirement

#### ■わんコメ（WebSocketに対応したバージョン）
（バージョン5.0.8で動作確認済み。可能な限り最新のバージョンをご利用ください）  

配信者のためのコメントアプリ わんコメ  
https://onecomme.com/

利用に関しては利用規約の遵守をお願いします（特にわんコメ無料版をお使いの方はクレジット表記のルールに関して注意してください）  
https://onecomme.com/terms/

#### ■VOICEPEAK 商用可能6ナレーターセット（コマンドラインでの読み上げに対応したアプリケーション及びバージョン）
（バージョン1.2.7で動作確認済み。ただし、バージョン1.2.5だと不具合があるので、バージョン1.2.6以降にしてください）

VOICEPEAK 商用可能6ナレーターセット  
https://www.ah-soft.com/voice/6nare/

利用に関しては利用規約の遵守をお願いします  
https://www.ah-soft.com/voice/6nare/eula.html

VOICEPEAKのキャラクター製品シリーズでは動作確認をしていませんが、設定（.env）を調整することで使えると思います。  
個人利用でもキャラクターにより許諾範囲が違うみたいなので、詳しくはこちらをご覧ください。  
https://www.ah-soft.com/commercial/voicepeak/private/

# Usage

最新版（v2.0.0以降）をダウンロードして任意の場所に配置してください。  
https://github.com/KanashisaBlue/OneComme-VOICEPEAK/archive/refs/heads/main.zip

わんコメのバージョン4以下をお使いの場合はv1.0系の最新版（v1.0.4）をご利用ください。  
https://github.com/KanashisaBlue/OneComme-VOICEPEAK/archive/refs/tags/v1.0.4.zip

.env.example ファイルを .env にリネームして、必要に応じて内容を変更してください（変更しなくても動くとは思いますが、VOICEPEAKをデフォルトの場所以外にインストールしてる場合などは変更が必要になります）

## v2.0.0以降をご利用の方のみ

まず、わんコメを「起動した状態」にしてください。  

次にターミナルアプリ（「ターミナル」「iTerm2」など）を起動し、以下のようなコマンドでonecomme_voicepeak_threading_ws.pyのPythonスクリプトを実行してください。

`cd [Pythonスクリプトがあるディレクトリ] && python ./onecomme_voicepeak_threading_ws.py`

「スクリプト起動... わんコメとの接続が完了しました。読み上げができる状態です。読み上げが可能な状態です... このスクリプトを停止する場合は ctrl + c で停止してください」  
と表示されます。基本はこの状態でわんコメとの連携が完了しています。

※わんコメの仕様により、VOICEPEAKの読み上げとわんコメのシステムの読み上げが同時に両方読み上げられてしまう不具合が発生します。回避方法は以下のブログをご覧ください。  
https://kanashisa.blue/2023/12/10/onecomme-voicepeak/

## v1.0系をご利用の方のみ

まず、わんコメを「終了した状態」にしてください。  

次にターミナルアプリ（「ターミナル」「iTerm2」など）を起動し、以下のようなコマンドでonecomme_voicepeak_threading_ws.pyのPythonスクリプトを実行してください。

`cd [Pythonスクリプトがあるディレクトリ] && python ./onecomme_voicepeak_threading_ws.py`

「スクリプト起動... 読み上げ開始まで最大30秒程度おまちください...」という文字が出たまま停止します。  
その状態でわんコメを起動してください。

わんコメを起動したら、メニューの「連携」から以下の設定を入れてください。  

- 「ゆかコネNEO / TRANS-THROUGH」の「有効化」にチェックを入れる
- プロトコルは「ws」、ホスト名は「127.0.0.1」、ポート番号は「8765」
- 読み上げタブの「読み上げ連携」にチェックを入れ、読み上げボイスに「悲しさ独自スクリプト」を選択する

以上の設定を行うと、ターミナル上に「読み上げが可能な状態です... このPythonスクリプトを停止する場合は ctrl + c で停止してください」と表示され、連携に必要な最低限の設定は完了します。

## ここからはv2.0.0以降およびv1.0系共通

メニューから「コメントテスター」を起動し、「読み上げ」のチェックボックスにチェックを入れて、下の「送信」ボタンを押してコメントが読まれれば、連携は成功しています。  

このPythonスクリプトを終了する際は、ターミナル上で ctrl + c で停止してください。

ナレーターの変更、ベースボリュームの設定は、いったんPythonスクリプトを終了したあとに .env ファイルの内容を書き換えてから、再度Pythonスクリプトを起動してください。  

わんコメ側の設定についてはブログ記事を参照してください。  
https://kanashisa.blue/2023/12/10/onecomme-voicepeak/

VOICEPEAK側は特に設定は不要ですが、辞書機能は読み上げに反映されるので、適宜利用してください。

# FAQ

#### ？.エラーが出て動きません
A. 細かいサポートはしてませんので、各自ググるなどして対応してください。エラー内容について要点を簡潔に分かりやすくまとめて連絡いただければ対応させていただきます。書かれている内容がよく分からないなどの場合は対応しません。ご了承ください。

#### ？.Pythonの環境構築（バージョン3.11系以降のインストール、Pythonライブラリのインストール）が難しいです
A. こちらも細かいサポートはできません。各自で頑張ってバージョン3.11系以降の環境を整えてください。下記のサイトが参考になるかもしれません。  

pyenvでPythonをインストールする方法  
https://tld.holy.jp/2022/12/07/install-python/  

pipを使ってライブラリをインストールする方法  
https://www.sejuku.net/blog/50417

#### ？たまにVOICEPEAKがエラーを出す
A. 原因がよく分からないのですが、VOICEPEAKのバージョン1.2.6くらいから出るようになりました。とりあえずVOICEPEAKのエラーは放置して大丈夫です。エラーが起きた際にはリトライ処理を入れているので、エラーで読み上げられないということはほぼ発生しないはずです。

#### ？Pythonスクリプトとかなんか難しい。簡単に扱えるようにアプリ化してほしい
A. 個人的にはアプリにするほどでもないと思いますが、Pythonの環境構築やターミナルの操作が難しいと感じる人は多いとおもうので、そういう要望が多ければ考えます。

# Contribution

もし不具合や要望などありましたらGitHubのIssueかX（旧Twitter）のDMまでお願いします。  

# Revision History

このPythonスクリプトをバージョンアップする際は、スクリプトを停止してから onecomme_voicepeak_threading_ws.py を上書きしてください。.env の内容は最新の .env.example を参考にして適宜調整してください。  

v2.0.1 （2023/12/23） コメントを重複して読み上げる不具合に対応しました  
v2.0.0 （2023/12/17） 公式WebSocket APIを使って連携する方法に変更しました  
v1.0.4 （2023/12/14） YouTube等でまれにコメントが読まれない場合がある不具合を修正しました  
v1.0.3 （2023/12/12） pandasを利用しなくなっていたので削除しました  
v1.0.2 （2023/12/11） 読み上げボリュームをわんコメの「連携」→「読み上げ」→「読み上げボリューム」のスライダーと連動するように変更  
v1.0.1 （2023/12/10） わんコメと重複する機能を削除  
v1.0.0 （2023/12/10） リリース

# Author

悲しさ  
X（旧Twitter）：https://x.com/KanashisaBlue （連絡はアカウントフォローの上、こちらのDMへ）  
ブログ：https://kanashisa.blue  
YouTube：https://www.youtube.com/@KanashisaBlue

# License

Released under the MIT license  
https://opensource.org/licenses/mit-license.php

