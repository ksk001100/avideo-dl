from avideo_dl.scripts.command import main
import pytest
import sys
import os



def test_xvideos():
    sys.argv = ['', 'https://www.xvideos.com/video52267033/awalnya_nolak_setelah_blowjob_malah_keenakan']
    main()


def test_tube8():
    sys.argv = ['', 'https://jp.tube8.com/%E9%9B%86%E5%9B%A3%E3%82%BB%E3%83%83%E3%82%AF%E3%82%B9/subtitled-uncensored-japanese-naked-party-blowjob-game-in-hd/55585181/']
    main()


def test_redtube():
    sys.argv = ['', 'https://jp.redtube.com/1694953']
    main()


os.system('rm -rf *.mp4')