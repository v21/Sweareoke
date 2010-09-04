import pykar


def parse_midi(filename):
    with open(filename) as f:
        fdata = f.read()
        midifile = pykar.midiParseData(fdata, None, 'cp1252')
        return midifile.lyrics.list

def clean_syllables(lyric_list):
    #remove lines

    #at the very start (title/artist lines)
    lyric_list = [lyric for lyric in lyric_list if lyric > 0]

    #and concatenate syllables beloning to a single word

    #that means they don't end in a space
    #and aren't the last word on a line.

"""    for i, lyric in enumerate(lyric_list):
        if (lyric.text[-1:] != " ") and (lyric_list[i + 1].line != lyric.line):
            lyric.lone_syllable = True
"""


    #finally, process to simpler format for joe's tiny mind


