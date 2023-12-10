# OneComme-VOICEPEAK

# Overview

コメントビューアのわんコメと、読み上げソフトのVOICEPEAKを連携するPythonスクリプトです。  
わんコメのコメントの読み上げをVOICEPEAKのキレイな読み上げで読ませることができます。  

Windowsを利用されている方は「ゆかコネNEO」を利用された方が手軽かと思いますので、そちらをご利用ください。  
https://nmori.github.io/yncneo-Docs/

このスクリプトはゆかコネNEOが利用できない環境（macOS）の利用を想定しています。  

わんコメ、VOICEPEAKともに非公認の野良スクリプトです。両アプリのいずれかで仕様変更が起きた場合、動かなくなる恐れがあります。バージョンアップ等を経緯にして動かなくなった場合、このページの最下部にある連絡先から連絡ください。

# Environment

#### ■macOS（64bit）  
Intel CPUのMacにて動作確認を行っていますが、AppleシリコンのMacでもたぶん動作します。  

#### ■Python（3.11系以降）
動作確認できているのはバージョン3.12.1とバージョン3.11.6です。  
おそらくバージョン3.11以降で動作すると思いますが、動作確認できている3.11.6以降をお勧めします。  
Mac標準で入ってるPythonはバージョンが古いので、3.11系以降のPythonを別途インストールしてください。  
インストーラーで入れる方法もあるようですが、pyenvを使って入れる方法の方が後々の管理も楽ですので、個人的にはこちらをお勧めします。  
（インストーラー版Pythonでは動作確認していません）

以下のライブラリの導入は必須ですので、pipコマンド等でインストールお願いします。

- python-dotenv
- setuptools
- pandas
- websockets

# Requirement

#### ■わんコメ（WebSocketに対応したバージョン）
（バージョン5.0.8で動作確認済み。バージョン4.0以降だとおそらく大丈夫だと思います）  

配信者のためのコメントアプリ わんコメ  
https://onecomme.com/

利用に関しては利用規約の遵守をお願いします（クレジット表記など）  
https://onecomme.com/terms/

#### ■VOICEPEAK 商用可能6ナレーターセット（コマンドラインでの読み上げに対応したアプリケーション及びバージョン）
（バージョン1.2.7で動作確認済み。ただし、バージョン1.2.5だと不具合があるので、バージョン1.2.6以降にしてください）

VOICEPEAK 商用可能6ナレーターセット  
https://www.ah-soft.com/voice/6nare/

利用に関しては利用規約の遵守をお願いします  
https://www.ah-soft.com/voice/6nare/eula.html

※VOICEPEAKのキャラクター版では動作確認しておりませんが、コマンドラインでの読み上げが可能であれば、設定（.env）を調整ことでおそらく使えるとは思います。

# Usage

最新版をダウンロードして任意の場所に配置してください。  
https://github.com/KanashisaBlue/OneComme-VOICEPEAK/archive/refs/heads/main.zip

.env.example ファイルを .env にリネームして、必要に応じて内容を変更してください（変更しなくても動くとは思いますが、VOICEPEAKをデフォルトの場所以外にインストールしてる場合などは変更が必要になります）  

まず、わんコメを終了した状態にしてください。  

次にターミナルアプリ（「ターミナル」「iTerm2」など）を起動し、以下のようなコマンドでonecomme_voicepeak_threading_ws.pyのスクリプトを実行してください。

`cd [pythonスクリプトがあるディレクトリ] && python ./onecomme_voicepeak_threading_ws.py`

「スクリプト起動... 読み上げ開始まで最大30秒程度おまちください...」という文字が出たまま停止します。  
その状態でわんコメを起動してください。

わんコメを起動したら、メニューの「連携」から以下の設定を入れてください。  

- 「ゆかコネNEO / TRANS-THROUGH」の「有効化」にチェックを入れる
- プロトコルは「ws」、ホスト名は「127.0.0.1」、ポート番号は「8765」
- 読み上げタブの「読み上げ連携」にチェックを入れ、読み上げボイスに「悲しさ独自スクリプト」を選択する

以上の設定を行うと、ターミナル上に「読み上げが可能な状態です... このスクリプトを停止する場合は ctrl + c で停止してください」と表示され、連携に必要な最低限の設定は完了します。

メニューから「コメントテスター」を起動し、「読み上げ」のチェックボックスにチェックを入れて、下の「送信」ボタンを押してコメントが読まれれば、連携は成功しています。  

スクリプトを終了する際は、ターミナルで ctrl + c で停止してください。

# FAQ

#### ？.エラーが出て動きません
A. 細かいサポートはしてませんので、各自ググるなどして対応してください。X（旧Twitter）にエラー内容について要点をまとめて連絡いただければ、お返事できる場合はお返事します（必ず返事することは保証できません）。

#### ？.Pythonの環境構築（バージョン3.11系以降のインストール、ライブラリのインストール）が難しいです
A. こちらも細かいサポートはできません。各自で頑張ってバージョン3.11系以降の環境を整えてください。下記のサイトが参考になるかもしれません。  

pyenvでPythonをインストールする方法  
https://tld.holy.jp/2022/12/07/install-python/  

pipを使ってライブラリをインストールする方法  
https://www.sejuku.net/blog/50417

# Contribution

もし不具合など何か気付いたらGitHubのIssueかX（旧Twitter）のDMまでお願いします。  

# Revision history

v1.0.2 （2023/12/11） 読み上げボリュームをわんコメの「連携」→「読み上げ」→「読み上げボリューム」のスライダーと連動するように変更  
v1.0.1 （2023/12/10） わんコメと重複する機能を削除  
v1.0.0 （2023/12/10） リリース

# Author

悲しさ  
X（旧Twitter）：https://x.com/KanashisaBlue  
ブログ：https://kanashisa.blue  
YouTube：https://www.youtube.com/@KanashisaBlue

# License

Released under the MIT license  
https://opensource.org/licenses/mit-license.php

