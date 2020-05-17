import sys
from console_progressbar import ProgressBar

from Compressor.Compressor import Compressor


def main():
    if len(sys.argv) < 3:
        print('3 arguments expected but ' + str(len(sys.argv)) + ' received.\n\nThe required arguments are\n1. Source '
                                                                 'file or folder\n2. Destination file or folder\n3. '
                                                                 'Output quality (1-100)\n\nExample: python compress.py '
                                                                 './source ./output 75')
        return

    compressor = Compressor(sys.argv[0], sys.argv[1], int(sys.argv[2])) #TODO check if valid paths, if quality is integer
    compressor.compress()



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