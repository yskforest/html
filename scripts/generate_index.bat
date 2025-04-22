@echo off
setlocal EnableDelayedExpansion

rem 出力ファイル名
set OUTPUT=index.html

rem ヘッダーを書き込む
echo ^<html^>^<head^>^<meta charset="utf-8"^>^<title^>Index</title^>^</head^>^<body^> > %OUTPUT%
echo ^<h1^>HTMLファイル一覧^</h1^> >> %OUTPUT%
echo ^<ul^> >> %OUTPUT%

rem .html ファイルをすべて探す
for /R %%F in (*.html) do (
    set "full=%%F"
    set "rel=%%F"
    rem カレントディレクトリのパスを削除して相対パスに
    set "rel=!rel:%CD%\=!"
    rem HTMLエスケープ処理は省略（通常不要）
    echo ^<li^>^<a href="!rel!"^>!rel!^</a^>^</li^> >> %OUTPUT%
)

echo ^</ul^> >> %OUTPUT%
echo ^</body^>^</html^> >> %OUTPUT%

echo 完了: %OUTPUT% を作成しました。
pause