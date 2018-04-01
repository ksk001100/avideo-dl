import os
import argparse
from .aa import ascii_moji
from .AVideoDownloader import AVideoDownloader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Specify URL')
    parser.add_argument('-t', '--thread', help='Specify the number of threads',
                        type=int, default=10,
                        choices=range(100))
    args = parser.parse_args()
    print(ascii_moji['start'] + '\r')
    av = AVideoDownloader(args.url, args.thread)
    try:
        av.download()
    except KeyboardInterrupt:
        os.system('rm *.toyota')
    print('\n\n{}\n\n'.format(ascii_moji['finish']))


if __name__ == '__main__':
    main()