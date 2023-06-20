
import os
import sys

import openai
import argparse
from dotenv import load_dotenv

from pydub import AudioSegment


def chunk_pod(folder, file, minutes = 10):
    """
    Some files are too large to be transcribed, so we cut them into 10 minute chunks
    """
    file_path = os.path.join(folder, file)
    pod = AudioSegment.from_mp3(file_path)
    ## milliseconds
    chunk_length = minutes * 60 * 1000
    num_chunks = int(len(pod)/(10*60*1000))+1
    chunk_paths = []
    for i in range(1, num_chunks+1):
        chunk_path = os.path.join(folder, f"{file}_{i}.mp3")
        if i == num_chunks:
            chunk = pod[((i-1)*chunk_length):]
        else:
            chunk = pod[((i-1)*chunk_length):((i)*chunk_length)]
        chunk.export(chunk_path, format="mp3")
        chunk_paths.append(chunk_path)
    return chunk_paths


def make_transcript(file_list, params={}, delete_chunks=True):

    print(f"There are {len(file_list)} parts to transcribe...")
    transcript=''
    for i, file_path in enumerate(file_list):
        print(f"Transcribing part {i+1}...")
        with open(file_path, "rb") as fp:
            transcript += openai.Audio.translate("whisper-1", fp, **params).text
            transcript += '\n Transcript break \n'
    if delete_chunks:
        for x in file_list:
            os.remove(x)
    return transcript

def main():

    parser = argparse.ArgumentParser(description='Transcribe a folder of audio files')
    parser.add_argument('--folder', type=str, help='Folder containing audio files')
    parser.add_argument('--output_folder', type=str, help='Output folder to dump transcripts')
    parser.add_argument('--finished_folder', type=str, help='Folder to move finished files to')

    ## prompts were not helpful, in fact they caused errors
    # parser.add_argument('--prompt', type=str, help='Prompt to use for transcription')

    args = parser.parse_args()

    env = load_dotenv()
    openai.api_key = os.getenv("OPEN_API_KEY")

    if args.folder is None:
        print("Please specify a folder")
        return
    
    if args.output_folder is None:
        print("Please specify an output folder")
        return
    
    if not os.path.exists(args.output_folder):
        print("Output folder does not exist, creating it")
        os.makedirs(args.output_folder)

    if not os.path.exists(args.folder):
        print("Input folder does not exist")
        return
    

    
    file_list = os.listdir(args.folder)
    params = {
        # 'prompt': args.prompt
    }

    for file in file_list:
        file_path = os.path.join(args.folder, file)
        file_size = sys.getsizeof(file_path)
        ## max file size is 25MB
        # if file_size > 25000000:
        chunk_paths = chunk_pod(args.folder, file)
        transcript = make_transcript(chunk_paths)
        # else:
            # transcript = make_transcript([file_path])

        output_file_path = os.path.join(args.output_folder, file.replace('.mp3','.txt'))
        with open(output_file_path , "w") as text_file:
            text_file.write(transcript)

        if args.finished_folder is not None:
            os.rename(file_path, os.path.join(args.finished_folder, file))

    return

if __name__ == "__main__":
    main()





