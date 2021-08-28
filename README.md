# vod-downloader
download videos from video hosting sites by chunks and glue them with ffmpeg

requirments: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z (ffmpeg)
chrome dev tools (ctrl+shift+i)
hands.dll

how to

open some video site, then press ctrl+shift+i, dev panel will popup and in networking
filter *.m3u8 file its a play list where amount of chunks specified
and *.ts its an url than need to be added (right click on *.ts file and (copy full url path))
then download (make sure u are in some directory cuz it will download lots of chunks before ffmpeg will create one video out of it)
notice:
some videos urls contains something called unique identifier u must cut it and put it in to the field
have fun.
