import sys
import argparse
from maudio import get_cipher,get_audio

def main():
    parser = argparse.ArgumentParser(description="description and help coming soon",prog="maudio", usage="%(prog)s \"message\" [options]")

    if sys.stdin.isatty():
        parser.add_argument("message",type=str,help="message to convert to morse")

    parser.add_argument("-v","--verbose",action="store_true")
    parser.add_argument("-o","--output",type=str,default="temp.wav",metavar="")
    parser.add_argument("-f","--frequency",type=int,default=600,metavar="")
    parser.add_argument("-s","--sample-rate",type=int,default=44100,metavar="")
    parser.add_argument("-b","--bits",type=int,default=16,metavar="")
    parser.add_argument("-w","--wpm",type=int,default=18,metavar="")
    parser.add_argument("-a","--amplitude",type=float,default=0.5,metavar="")
    parser.add_argument("--noaudio",action="store_true")
    parser.add_argument("--farns",type=int,metavar="")

    args=parser.parse_args()

    message = args.message if hasattr(args,"message") else sys.stdin.read()

    args.farns_desc = f"{args.farns} WPM" if args.farns else "disabled"

    if args.noaudio:
            print(cipher if not args.verbose else f"\ncipher : {cipher}")
            sys.exit(0)

    try:
        if args.verbose:
            print("Parsed arguments:")

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

        print(f"{'output':12}: {args.output}")
        get_audio( get_cipher(message) , args.output , args.wpm , args.frequency , bits=args.bits , rate = args.sample_rate , amp=args.amplitude , farns=args.farns )

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
