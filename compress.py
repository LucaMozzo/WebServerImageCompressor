import argparse
from console_progressbar import ProgressBar

from Compressor.Compressor import Compressor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='Source folder or file', required=True)
    parser.add_argument('--output', help='Destination folder or file', required=True)
    parser.add_argument('--quality', help='Quality (1-100)', type=int, required=True)
    parser.add_argument('--logs', help='Where to write failure logs', required=False)
    parser.add_argument('--threads', help='The number of threads to use for the compression', type=int, default=10, required=False)
    args = parser.parse_args()

    compressor = Compressor(args.source, args.output, args.quality, args.logs) #TODO cmake it work for single image
    compressor.compress(max_threads=args.threads)

if __name__ == "__main__":
    main()

# pb = ProgressBar(total=500,prefix='Here', suffix='Now', decimals=1, length=50, fill='▍', zfill='∙')
# pb.print_progress_bar(100)
# time.sleep(1)
# pb.print_progress_bar(25.55515)
# time.sleep(1)
# pb.print_progress_bar(50)
# time.sleep(1)
# pb.print_progress_bar(95)
# time.sleep(1)
# pb.print_progress_bar(100)