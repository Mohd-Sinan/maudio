import time
import wave,struct
from .MorseTable import forwardTable

def get_cipher(message):
    cipher = ''
    for letter in " ".join(message.upper().split()):
        if letter != ' ':
            try:
                cipher += forwardTable[letter] + ' '
            except KeyError:
                pass
        else:
            cipher += ' '
    return cipher

def get_audio( cipher , filename , wpm , fwpm=None , frequency=600 ):

    start = time.time()

    CHANNEL_NO = 1
    BITS = 16
    RATE = 4410
    AMP = 0.5

    try:
        fwpm = int(wpm) if fwpm is None else int(fwpm)
    except ValueError:
        raise ValueError(" wpm ,fwpm should be a numeric value")

    if filename[-4:] != '.wav':
        filename +='.wav'

    if  600 < frequency > 1000:
        raise Exception("frequency should be between 600 and 1000 (in Hz)")

    if not all(x in ('-', '.' ,' ' ) for x in cipher):
        raise Exception("cipher should only contain fullstops(dits) ,hyphens(dah) and spaces")

    dit_dur = float(60 / (50 * wpm))
    fdit_dur = (60 / fwpm - 31 * dit_dur) / 19

    period  = int( RATE / frequency )
    sqr_sample = period * [0]

    for i in range(period):
        if i < period/2:
            sqr_sample[i] = 1
        else:
            sqr_sample[i] = -1

    max_amplitude = float((int((2 ** BITS) / 2) - 1) * AMP)

    nframes = RATE / period    #frames per second
    sqr_bin = b''.join(struct.pack('h', int(i * max_amplitude)) for i in sqr_sample)
    dit = sqr_bin * int( nframes * dit_dur )
    dah = sqr_bin * int( nframes * dit_dur * 3)

    zero = struct.pack('h',0 )
    intra_char = zero * period * int( nframes * dit_dur )
    inter_char = zero * period * int( nframes * fdit_dur * 3 )
    word_space = zero * period * int( nframes * fdit_dur * 7 )

    bins = [ dit , dah , intra_char , inter_char , word_space ]

    w = wave.open(filename, 'wb')
    w.setnchannels (CHANNEL_NO ) # Mono
    w.setsampwidth( int(BITS / 8) ) # Sample is 1 Bytes
    w.setframerate( RATE ) # Sampling Frequency
    w.setcomptype('NONE','Not Compressed')

    waveform = []

    count = 0
    for signal in cipher:
        if signal == '-':
            waveform += [1]
            if cipher[count + 1] != ' ':
                    waveform += [2]
        elif signal == '.':
            waveform += [0]
            if cipher[count + 1] != ' ':
                waveform += [2]
        elif signal == ' ' and cipher[count + 1] != ' ':
            waveform += [3]
        elif signal == ' ' and cipher[count + 1] == ' ':
            waveform += [4]
        else:
            #Do nothing
            pass
        count += 1
        if count == (len(cipher) -1):
            waveform += [3]
            break

    #divide_chunks
    chunk_size = 5
    chunks = [waveform[i * chunk_size:(i + 1) * chunk_size] for i in range((len(waveform) + chunk_size - 1) // chunk_size )]


    for chunk in chunks:
        frames = b''.join(bins[sample] for sample in chunk)
        w.writeframesraw(frames)

    try:
        w.close()
    except:
        raise RuntimeError("wave.close() error , failed to write wav file during execution")

    end = time.time()
    print("Time elapsed: {}ms".format(round((end - start) *1000,2)))
