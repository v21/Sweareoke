import pykar
import word

def parse_midi(filename):
    with open(filename) as f:
        fdata = f.read()
        midifile = pykar.midiParseData(fdata, None, 'cp1252')
        return midifile.lyrics.list

def clean_syllables(lyric_list):
    #remove lines
    #print lyric_list
    #at the very start (title/artist lines)
    lyrics = [lyric for lyric in lyric_list if lyric.ms > 0]
    #print lyrics
    #and concatenate syllables beloning to a single word
    
    #that means they don't end in a space
    #and aren't the last word on a line.

    new_lyrics = []
    accum = None
    for i, lyric in enumerate(lyrics):
        #print "input : " + lyric.text
        if (accum != None):
            accum.text += lyric.text
            lyric = accum
            accum = None

        try:
            if (lyric.text[-1:] == " ") or (lyrics[i+1].text[0] == " "):
                new_lyrics.append(lyric)
                #print "spaced :  " + lyric.text
            elif (lyrics[i+1].line != lyric.line):
                new_lyrics.append(lyric)
                #print "new line: " + lyric.text
            else:
                accum = lyric
                #print "accumed : " + lyric.text
        except: #if the lookahead fails, we're on the last lyric
            new_lyrics.append(lyric)

        #print "\n"

    #finally, process to simpler format for joe's tiny mind
    return [word.Word(lyric.ms, lyric.text) for lyric in new_lyrics]


