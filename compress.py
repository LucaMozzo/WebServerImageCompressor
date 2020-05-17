import argparse
import os

from Compressor.Compressor import Compressor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='Source folder', required=True)
    parser.add_argument('--output', help='Destination folder', required=True)
    parser.add_argument('--quality', help='Quality (1-100)', type=int, required=True)
    parser.add_argument('--logs', help='Where to write failure logs', required=False)
    parser.add_argument('--threads', help='The number of threads to use for the compression', type=int, default=10, required=False)
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        raise ValueError('The source must be an existing directory')

    compressor = Compressor(args.source, args.output, args.quality, args.logs)
    compressor.compress(max_threads=args.threads)

if __name__ == "__main__":
    main()
