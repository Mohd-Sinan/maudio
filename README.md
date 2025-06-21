<pre>
███╗   ███╗ █████╗ ██╗   ██╗██████╗ ██╗ ██████╗ 
████╗ ████║██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗
██╔████╔██║███████║██║   ██║██║  ██║██║██║   ██║
██║╚██╔╝██║██╔══██║██║   ██║██║  ██║██║██║   ██║
██║ ╚═╝ ██║██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ 
**Minimal Morse code audio encoder**
</pre>                                            

## About

**maudio** is a command-line tool that converts text to Morse code and can generate audio output. You can control tone frequency, sample rate, amplitude, bit depth, WPM, and more.

## Getting Started

### Installation

```bash
git clone https://github.com/Mohd-Sinan/maudio.git
cd maudio
pip install .
```

### Usage

Use the tool like this:

```bash
maudio "your message here" [options]
```

To display the help menu:

```bash
maudio -h
```

You can also pipe input from another command:

```bash
echo "hello world" | maudio --noaudio
```

### Example

```bash
maudio "SOS HELP" -f 700 -w 20 -v
```

### CLI Options

| Option                  | Description                                              |
|-------------------------|----------------------------------------------------------|
| `message`               | Positional argument: the message to convert to Morse     |
| `-h`, `--help`          | Show help message and exit                               |
| `-v`, `--verbose`       | Enable verbose output                                    |
| `-o`, `--output`        | Output WAV file name (default: `temp.wav`)               |
| `-f`, `--frequency`     | Tone frequency in Hz (default: `600`)                    |
| `-s`, `--sample-rate`   | Audio sample rate in Hz (default: `44100`)               |
| `-b`, `--bits`          | Bit depth (default: `16`)                                |
| `-w`, `--wpm`           | Words per minute (speed) (default: `18`)                 |
| `-a`, `--amplitude`     | Tone amplitude (0.0 to 1.0) (default: `0.5`)             |
| `--noaudio`             | Prints Morse code without generating audio.              |
| `--farns`               | Apply Farnsworth timing with given WPM for spacing       |

## Python Example

```python
from maudio import get_cipher, get_audio

# Convert message to Morse code
msg = "hello world"
cipher = get_cipher(msg)
print("Morse code:", cipher)

# Generate audio from Morse code
get_audio(
    cipher,
    output="output.wav",
    wpm=18,
    freq=600,
    bits=16,
    rate=44100,
    amp=0.5,
    farns=None
)
```


### Uninstall?

```bash
pip uninstall maudio
```
