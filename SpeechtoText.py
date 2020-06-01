from pydub import AudioSegment
import speech_recognition as sr 
import sys
import os


def main():
    
    # Confirm the script is called with the required param
    if len(sys.argv) != 2:
        print('Usage: python Speechtotext.py FILE_NAME')
        exit(1)
 
    file_path = sys.argv[1]

    try:
        if not os.path.exists(file_path):
            print('file "{}" not found!'.format(file_path))
            exit(1)

    except OSError as err:
        print(err.reason)
        exit(1)


    audio = from_video_to_audio(file_path)
    mp3 = convert_to_wav(audio)
    text = from_audio_to_text(mp3)
    write_to_txt(mp3,text)
    print(text)


""" Write content into a text file """
def write_to_txt(mp3,content):

    name = str(mp3.split(".")[0]) + '.txt'
    with open(name,"w") as f:
        f.write(content)


""" Convert mp3 audio to wav """
def convert_to_wav(file_name):
                                                                         
    name = file_name.split(".")
    dst = str(name[0]) + '.wav'

    sound = AudioSegment.from_mp3(file_name)
    sound.export(dst, format="wav")

    return dst

""" Transforms video file into a MP3 file """
def from_video_to_audio(file_name):
    
    try:
        file, extension = os.path.splitext(file_name)
        # Convert video into .wav file
        os.system('ffmpeg -i {file}{ext} {file}.wav'.format(file=file, ext=extension))
        # Convert .wav into final .mp3 file
        os.system('lame {file}.wav {file}.mp3'.format(file=file))
        os.remove('{}.wav'.format(file))  # Deletes the .wav file
        print('"{}" successfully converted into MP3!'.format(file_name))

    except OSError as err:
        print(err.reason)
        exit(1)
    
    return str(file) + ".mp3"

""" Recognize text from a wav audio file """
def from_audio_to_text(file_name):

    r = sr.Recognizer()

    with sr.AudioFile(file_name) as source:
        audio = r.record(source)

    result = r.recognize_google(audio, language='it-IT')

    return result


if __name__ == '__main__':
	
	main()
