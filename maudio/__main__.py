import sys
import argparse
from maudio import get_cipher,get_audio

def main():
    parser = argparse.ArgumentParser(description="description and help coming soon",prog="maudio", usage="%(prog)s \"message\" [options]")

    if sys.stdin.isatty():
        parser.add_argument("message",type=str,help="message to convert to morse")

    parser.add_argument("-v","--verbose",action="store_true",help="Enable verbose output")
    parser.add_argument("-o","--output",type=str,default="temp.wav",metavar="",help="Output WAV file name (default: \'temp.wav\')")
    parser.add_argument("-f","--frequency",type=int,default=600,metavar="",help="Tone frequency in Hz (default: 600)")
    parser.add_argument("-s","--sample-rate",type=int,default=44100,metavar="",help="Audio sample rate in Hz (default: 44100)")
    parser.add_argument("-b","--bits",type=int,default=16,metavar="",help="Bit depth (default: 16)")
    parser.add_argument("-w","--wpm",type=int,default=18,metavar="",help="Words per minute (speed) (default: 18)")
    parser.add_argument("-a","--amplitude",type=float,default=0.5,metavar="",help="Tone amplitude (0.0 to 1.0) (default: 0.5)")
    parser.add_argument("--noaudio",action="store_true",help="Prints Morse code without generating audio.")
    parser.add_argument("--farns",type=int,metavar="",help="Apply Farnsworth timing with given WPM for spacing")

    args=parser.parse_args()

    message = args.message if hasattr(args,"message") else sys.stdin.read()

    args.farns_desc = f"{args.farns} WPM" if args.farns else "disabled"

    if args.noaudio:
        cipher = get_cipher(message)
        print(cipher if not args.verbose else f"\ncipher : {cipher}")
        sys.exit(0)

    try:
        if args.verbose:
            print("Audio Encoding Settings\n")

            args_dict = {
                "frequency":   args.frequency,
                "sample_rate": args.sample_rate,
                "bits":        args.bits,
                "wpm":         args.wpm,
                "amplitude":   args.amplitude,
                "farns":       args.farns_desc,
            }

            for k, v in args_dict.items():
                print(f"{k:12}: {v}")

        print(f"{'output_file':12}: {args.output}")
        time_elapsed = get_audio( get_cipher(message) , args.output , args.wpm , args.frequency , bits=args.bits , rate = args.sample_rate , amp=args.amplitude , farns=args.farns )
        print("\nTime elapsed: {}ms".format(time_elapsed))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
