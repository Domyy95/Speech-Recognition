from pydub import AudioSegment
import speech_recognition as sr 
import sys
import os


def main():
    
    # Confirm the script is called with the required param
    if len(sys.argv) != 2:
        print('Usage: python Speechtotext.py FILE_NAME')
        print('or:    python Speechtotext.py DIRECTORY_NAME')
        exit(1)
 
    file_path = sys.argv[1]

    # rename file if contain spaces
    os.rename(file_path, file_path.replace(" ", "_"))
    file_path = file_path.replace(" ", "_")    

    try:
        if not os.path.exists(file_path):
            print('file "{}" not found!'.format(file_path))
            exit(1)

    except OSError as err:
        print(err.reason)
        exit(1)

    #checks if path is a file
    isFile = os.path.isfile(file_path)

    #checks if path is a directory
    isDirectory = os.path.isdir(file_path)

    if isFile:
        text = mp4_to_text(file_path)
        print(text)
    
    elif isDirectory:

        dir_path = os.path.dirname(os.path.realpath(__file__))
        directory_results = file_path + '_results'

        # creation of a directory for the results
        try:
            os.mkdir(directory_results)

        except OSError:
            print ("Creation of the directory %s failed" % directory_results)

        else:
            print ("Created the directory %s" % directory_results)

        files = []
        for path in os.listdir(file_path):
            files.append(path)
        
        os.chdir(file_path)
            
        for f in files:
            os.rename(f, f.replace(" ", "_"))
            newname = f.replace(" ", "_") 
            mp4_to_text(newname)


def mp4_to_text(file_path):
    audio = from_video_to_audio(file_path)
    text = from_audio_to_text(audio)
    write_to_txt(audio,text)
    return text


""" Write content into a text file """
def write_to_txt(mp3,content):

    name = str(mp3.split(".")[0]) + '.txt'
    with open(name,"w") as f:
        f.write(content)
        

""" Transforms video file into a wav file """
def from_video_to_audio(file_name):
    
    try:
        file, extension = os.path.splitext(file_name)
        # Convert video into .wav file
        os.system('ffmpeg -i {file}{ext} {file}.wav'.format(file=file, ext=extension))
        print('"{}" successfully converted into wav!'.format(file_name))

    except OSError as err:
        print(err.reason)
        exit(1)
    
    return str(file) + ".wav"


"""Divide the audio in pieces of 60 seconds to be able to compute it with Google API"""
def divide_audio(audio):

    ten_seconds = 10 * 1000 
    fifty_seconds = ten_seconds * 5

    full = AudioSegment.from_wav(audio)
    duration = round(full.duration_seconds)

    n = 0

    while duration > 0:
        if duration >= 50:
            audios = full[:fifty_seconds]
            audios.export(str(n) + ".wav", format="wav")
            n += 1
            duration -= 50
            full = full[-(duration*1000):]
        
        else:
            audios = full[:(duration*1000)]
            audios.export(str(n) + ".wav", format="wav")
            duration = 0

    return n


def delete_wav(file,n):

    os.remove(file)  
    for i in range(0,n+1):
        os.remove('{}.wav'.format(i))  


""" Recognize text from a wav audio file """
def from_audio_to_text(file_name):

    r = sr.Recognizer()

    audios = divide_audio(file_name)
    text = ""

    for a in range(0,audios):

        with sr.AudioFile(str(a) + '.wav') as source:
            audio = r.record(source)

        result = r.recognize_google(audio, language='it-IT')

        text += result
    
    delete_wav(file_name,audios)

    return text


if __name__ == '__main__':
	
	main()
