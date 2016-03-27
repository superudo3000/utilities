# -*- coding: utf-8 -*-

from pathlib import Path
import unittest

from create_pls import generate_playlist


class PlaylistCreationTest(unittest.TestCase):

    def test_no_files(self):
        paths = self.to_paths()

        expected = '''\
[playlist]

NumberOfEntries=0
Version=2
'''

        self.assertPlaylistGeneration(paths, expected)

    def test_single_file(self):
        paths = self.to_paths(
            'Artist Name - Song Title.mp3',
        )

        expected = '''\
[playlist]

File1=Artist Name - Song Title.mp3
Title1=Artist Name - Song Title
Length1=-1

NumberOfEntries=1
Version=2
'''

        self.assertPlaylistGeneration(paths, expected)

    def test_multiple_files(self):
        paths = self.to_paths(
            'Foo Man - Foo Song.mp3',
            'Bar Band - Bar Song.ogg',
            'DJ Hipster - Chillout Mix.ogg',
        )

        expected = '''\
[playlist]

File1=Foo Man - Foo Song.mp3
Title1=Foo Man - Foo Song
Length1=-1

File2=Bar Band - Bar Song.ogg
Title2=Bar Band - Bar Song
Length2=-1

File3=DJ Hipster - Chillout Mix.ogg
Title3=DJ Hipster - Chillout Mix
Length3=-1

NumberOfEntries=3
Version=2
'''

        self.assertPlaylistGeneration(paths, expected)

    def to_paths(self, *filenames):
        yield from (Path(fn) for fn in filenames)

    def assertPlaylistGeneration(self, path, expected):
        actual = generate_playlist(path)
        actual_joined = ''.join(actual)
        self.assertEqual(actual_joined, expected)


if __name__ == '__main__':
    unittest.main()
