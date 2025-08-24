# vehicle_arranger
This application is for arranging the vehicle pak file of simutrans.  
## Notification
When modifying simutrans pak files using this program or distributing modified pak files, be sure to obtain permission from the creator of the original pak file to be modified.
## Usage
This program consists of a python file.  

After you select input original pak file and name output pak file, This program ask you whether modify some setting of the vehicle pak. Please input modified values or names. If you not put any values (enter "x" in the connecting setting), or input wrong values, the setting will not be modified.
### Command line usage
python vehicle_arranger.py input_file_path (output_file_path)  

input_file_path : string, a path of original pak file.  
output_file_path : string, a path of modifies pak file. If not writing output_file_path, output_file_path will be the same as input_file_path
## Credit
simupoppo (@simu__poppo)  
If you have any questions, please contact us @simu__poppo or https://simutranshouse.wixsite.com/simutp

## Lisence
CC-BY 4.0  
Modification and redistribution of this program is permitted

## Disclaimer
The author assumes no responsibility for any damages resulting from the downloading, installation, use, or distribution of this program, or from the use, distribution, or any other use or distribution of materials generated using this program.

## release notes
- 14.03.2024 ver.0 release
- 20.03.2024 ver.0.1 correction of misprints
- 27.04.2024 ver.1 arranging vehile paks' versions.
- 24.08.2025 ver.2 Add Building and Factory editing.  

# vehicle_arranger 取扱説明書
このプログラムはsimutransの乗り物アドオンのpakファイルを編集するプログラムです。
## 注意事項
本プログラムを用いてpakファイルを改造、または改造したファイルを公開する場合は、必ず元のアドオンの作者に許可を得て行ってください。
## 使い方
このプログラムはpythonファイルです。

起動し、入力ファイルと出力ファイル名を入力すると、入力ファイル内の乗り物アドオンの詳細な設定事項の一部がコマンドラインに出力されます。コマンドラインより修正が必要な事項を記入してください。何も入力しなかった場合(連結の設定ではxを入力した場合)、または不適当な入力の場合、設定事項は変更されません。
## 著作者
simupoppo(@simu__poppo)  
お気づきの点がございましたら、@simu__poppoまたは https://simutranshouse.wixsite.com/simutp までお問い合わせください。
## ライセンス
CC-BY 4.0  
このプログラムの改造、再配布について制限はございません。
## 免責事項
本プログラムのダウンロード、インストール、使用、頒布および本プログラムを使用し作成したファイルの使用、頒布、その他により発生したいかなる損害について、作者は一切の責任を負いかねます。
## リリースノート
- 2024年3月14日 ver.0 リリース  
- 2024年3月20日 ver.0.1 誤植の修正
- 2024年4月27日 ver.1 pakファイルバージョン変更に対応
- 2025年8月24日 ver.2 建物・産業アドオンに対応  
