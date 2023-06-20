# sports_pod_summarizer
Uses open AI to feed me sports information


Steps:

1. Download .mp3 files into a folder
2. Make a .env file that contains OPEN_API_KEY specifying your (Open AI api key)[https://platform.openai.com/docs/quickstart]
3. Create output folders
4. Run the terminal command:
    'python transcribe_folder.py --folder "data/untrans_audio/" --output_folder "data/transcripts" --finished_folder "data/trans_audio"'
    This transcribes every .mp3 file in the data/untrans_audio/ folder at around $0.33 cents per hour. Then it moves the transcribed audio into a finished folder to avoid running the same code on the same audio again.
5. Now that we have the transcription, run the terminal command:
    'python summarize_transcription.py --input_file "data/transcripts/{podcast_name}.txt" --output_file "summary.txt" --output_folder "data/text_summaries" --prepend_query "Can you summarize {some content, i.e. the horse picks} from the following podcast transcription?"
6. Not necessary, but I typically paste into a Google doc to read the summary.

That code worked for me for the few trial cases I've tried. Feel free to open issues, etc if there are issues.




