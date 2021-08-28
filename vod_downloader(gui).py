import PySimpleGUI as btw
import configparser
import subprocess
import threading
import requests
import fnmatch
import os.path
import time
import glob
import os

####

cwd = os.getcwd()
configList = fnmatch.filter(os.listdir(cwd), "*.C-137")

####

###

def glueVideo(name, formatt):

    run = subprocess.Popen([cwd + "\\ffmpeg.exe", '-y', '-f', 'concat', '-safe', '0', '-i', 'chunks.txt', '-c', 'copy', '%s.mp4' % name])
    run.communicate()


def download(target, i, formatt,chunk_file):

    r = requests.get(target, allow_redirects=True)
    with open(str(i) + formatt, 'wb') as f:
        f.write(r.content)
        pattern = "file '" + str(i) + formatt + "'"
        chunk_file.write("%s\n" % pattern)

def runMain(url,formatt,rangee,identifier,name):

    with open("chunks.txt", 'w') as chunk_file:

        for i in range(int(rangee)):

            if not identifier:
                target = url + str(i) + formatt
                download(target, i, formatt,chunk_file)

            elif identifier:
                target = url + str(i) + formatt + identifier
                download(target, i, formatt,chunk_file)

    chunk_file.close()

def savePatterFile(url,formatt,rangee,identifier,name,cwd):
        savePattern = "[Download_PARAMS]\n url=%s\n formatt=%s\n rangee=%s\n identifier=%s\n name=%s\n" % (url, formatt, rangee, identifier, name)
        file = "%s\\%s.C-137" % (cwd, name)
        with open(file, 'w') as f:
            f.write(savePattern)
            f.close()

def checkFiles(url,rangee,formatt,identifier):

    for i in range(int(rangee)):

        target = url + str(i) + formatt + identifier
        r = requests.head(target)

    return r.status_code

def loadConfig(cwd, config):
    conf = configparser.ConfigParser(empty_lines_in_values=False)
    conf.read("%s\\%s" % (cwd, config))

    url = conf['Download_PARAMS']['url']
    formatt = conf['Download_PARAMS']['formatt']
    rangee = conf['Download_PARAMS']['rangee']
    identifier = conf['Download_PARAMS']['identifier']
    name = conf['Download_PARAMS']['name']
    return url, formatt, rangee, identifier, name

###

####

btw.theme('Black')
layout = [
                [btw.Image(filename="256x256.png")],
                [btw.Text('Enter traget url :', font=('Verdana', 8), size=(15, 1)), btw.InputText(key='url', size=(30, 1))],
                [btw.Text('Format :', font=('Verdana', 8), size=(15, 1)), btw.InputText(key='formatt', size=(30, 1))],
                [btw.Text('Chunks range :', font=('Verdana', 8), size=(15, 1)), btw.InputText(key='rangee', size=(30, 1))],
                [btw.Text('Unique Identifier :', font=('Verdana', 8), size=(15, 1)), btw.InputText(key='identifier', size=(30, 1))],
                [btw.Text('Name your video :', font=('Verdana', 8), size=(15, 1)), btw.InputText(key='name', size=(30, 1))],
                [btw.Text('Load from file :', font=('Verdana', 8), size=(15, 1)), btw.Combo(configList, enable_events=True, key='configName', size=(21, 1)), btw.Button('Load', font=('Verdana', 10))],
                [btw.Text('', size=(36, 2), key='Notification')], [btw.Button('Download', font=('Verdana', 10)), btw.Button('Exit', font=('Verdana', 10))]
            ]

window = btw.Window('vod_downloader', layout, icon= cwd + "\\256x256.ico",)

####

def main_window(layout,window):

# Event Loop to process "events" and get the "values" of the inputs
    while True:

        event, values = window.read(timeout=100)
      
        try:
            url = values['url']
        except Exception as e:
            pass
        try:
            formatt = values['formatt']
        except Exception as e:
            pass
        try:
            rangee = values['rangee']
        except Exception as e:
            pass
        try:
            identifier = values['identifier']
        except Exception as e:
            pass
        try:    
            name = values['name']
        except Exception as e:
            pass

        if event == 'Load' and len(values['configName']) > 0:

            config = values['configName']
            loadConfig(cwd, config)
            window['url'].update(url)
            window['formatt'].update(formatt)
            window['rangee'].update(rangee)
            window['identifier'].update(identifier)
            window['name'].update(name)
            
            window['Notification'].update('[ i ] Download params loaded from a file.')

        if event == 'Download' and len(values['url']) > 0 and len(values['formatt']) > 0 and len(values['rangee']) > 0 and len(values['name']) > 0:
            
            if checkFiles(url,rangee,formatt,identifier) == 200:

                    thread = threading.Thread(target=runMain ,args=(url,formatt,rangee,identifier,name))
                    thread.start()
                    thread.join()

                    if os.path.exists("%s\\chunks.txt" % cwd):

                        if os.path.exists("%s\\ffmpeg.exe" % cwd):

                            if not os.path.exists("%s\\%s" % (cwd, name)):
                                savePatterFile(url,formatt,rangee,identifier,name,cwd)
                            glueVideo(name, formatt)
                            window['Notification'].update('[ i ] Done.')

                        else:
                            window['Notification'].update('[ i ] Error no ffmpeg.exe in working folder: %s' % cwd)                    
                    else:
                        window['Notification'].update('[ i ] Error no chunks.txt in working folder: %s' % cwd)
            else:
                window['Notification'].update('[ i ] Requested files not available, url has expired, scout for new values.')

        window.refresh()

        if event == btw.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            window['Notification'].update('[ i ] Exiting...')
            break

    window.close()

if __name__ == '__main__':
    main_window(layout,window)