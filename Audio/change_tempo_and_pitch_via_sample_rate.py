""" Python Script: change_tempo_and_pitch_via_sample_rate.py

Author: Stefan Behrens
Version (Date): 1.0 (2025-02-21)
Language: Python 3.13.1

Description:
The goal is to mimic the behavior of speeding up music on vinyl or tape 
where tempo and pitch change simultaneously. This is achieved by copying a 
given WAV file sample by sample and only changing the sample rate.
The new file will than play back the same material as the old file at a
higher or lower tempo depending on old and new sample rates.
For example, if the sample rate changes from 48.000 Hz to 50.400 Hz, the
tempo and pitch change by a factor of 50.400/48.000 = 1.05.
The effect is the same a setting the pitch adjustment on a turtable to +5%.

Instructions:
The script requires the installation of a python interpreter and the wave
module. It is executed from a command line interface with the prompt:
    python <script name> <input WAV file> <new sample rate>

The default <script name> is: change_tempo_and_pitch_via_sample_rate.py
This only changes if you rename the file.

As an example using the default script name, the command line prompt
    python change_tempo_and_pitch_via_sample_rate.py input.wav 50400
tells the script to look for a WAV file called 'input.wav' in the same folder
as the script file and writes a new file.
If the file is in a different folder, say on a Windows system, the prompt
    python change_tempo_and_pitch_via_sample_rate.py "C:\Folder\input.wav" 50400
the script writs the new file in "C:\Folder".
For Unix based systems (Linux, MacOS), this would look like
    python change_tempo_and_pitch_via_sample_rate.py "/home/folder/input.wav" 50400
Relative file paths are possible as well.

Disclaimer:
Some of the code below was generated using ChatGPT. 
"""


import wave
import sys

def get_path_name(path_name_wav:str):
    """Extracts the path and name of a .wav file.
    Expects input in one of the following formats:
        '<name>.wav'
        '<path>\<name>.wav'
        '<path>/<name>.wav'
    Returns the tuple (<path>,<name>). 
    First entry is None in case '<name>.wav'
    """
    # get end of path name (last occurence of '/' or '\' in path_name_wav)
    # returns -1 if no path information is included
    end_of_path = max([path_name_wav.rfind('/'), path_name_wav.rfind('\\')])
    
    # extract file name (located between path and '.wav')
    name = path_name_wav[end_of_path + 1 : -4]
    
    # extract file path if information is included 
    if end_of_path > -1:
        path = path_name_wav[:end_of_path + 1]
    else:
        path = None

    return path, name


def change_sample_rate(input_wav:str, new_sample_rate:int):
    """Reads a WAV file and writes a copy which has exactly the same samples
    but a different sample rate as specified. 
    Arguements:
        input_wav: string of the form '<name>.wav', '<path>\<name>.wav', 
            or '<path>/<name>.wav'
        new_sample_rate: integer indicated the new sample rate
    Return Values:
        n/a (no return values)
    """
    try:
        # Open the input WAV file
        with wave.open(input_wav, 'rb') as in_wav:
            # Get the parameters of the original WAV file
            params = in_wav.getparams()
            
            # Extract the number of channels, sample width, and number of frames
            num_channels = params[0]
            sample_width = params[1]
            old_sample_rate = params[2]
            num_frames = params[3]
            
            # Set the output file name
            path, input_wav_name = get_path_name(input_wav)
            output_wav_name = input_wav_name + f"--sample_rate_changed__{old_sample_rate}_to_{new_sample_rate}"
            output_wav = path + output_wav_name + '.wav'
            
            # Open the output WAV file for writing
            with wave.open(output_wav, 'wb') as out_wav:
                # Set the new parameters for the output file
                out_wav.setparams((num_channels, sample_width, new_sample_rate, num_frames, params[4], params[5]))
                
                # Read the frames from the original WAV file and write them to the new file
                frames = in_wav.readframes(num_frames)
                out_wav.writeframes(frames)
        
        print(f"Sample rate changed from {old_sample_rate} Hz to {new_sample_rate} Hz and saved as {output_wav}")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main routine. Receives command line input and calls change_sample_rate()
    to change the sample rate of a WAV file as desired"""
    if len(sys.argv) != 3:
        print("Usage: python change_tempo_and_pitch_via_sample_rate <input_wav> <new_sample_rate>")
        sys.exit(1)
    
    input_wav = sys.argv[1]
    
    try:
        new_sample_rate = int(sys.argv[2])
    except ValueError:
        print("Error: The sample rate must be an integer.")
        sys.exit(1)
    
    # Output file name (this can be modified to append _modified or similar)
    output_wav = "output_audio.wav"
    
    # Call the function to change the sample rate
    change_sample_rate(input_wav, new_sample_rate)

if __name__ == "__main__":
    main()
