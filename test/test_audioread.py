# This file is part of audioread.
# Copyright 2018, Sam Thursfield
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
import platform

import pytest

import audioread


# The 'audiofile' fixture is defined in conftest.py.


def test_audioread_early_exit(audiofile):
    """Abort the read before it is completed.

    This test guards against regressions such as
    https://github.com/beetbox/audioread/pull/78

    """
    with audioread.audio_open(audiofile.path) as a:
        assert int(a.duration) == int(audiofile.duration)
        assert a.channels == audiofile.channels
        assert a.samplerate == audiofile.samplerate
        # Now we exit the context manager without reading any data.


def test_audioread_full(audiofile):
    """Read the audio data from the file."""
    with audioread.audio_open(audiofile.path) as a:
        assert int(a.duration) == int(audiofile.duration)
        assert a.channels == audiofile.channels
        assert a.samplerate == audiofile.samplerate

        # Now read all the data and assert that it's the correct type.
        for block in a:
            assert type(block) == bytes


@pytest.mark.skipif(not audioread.ffdec.available(), reason="FFMPEG not available")
def test_ffdec(audiofile):
    with audioread.ffdec.FFmpegAudioFile(audiofile.path) as a:
        assert int(a.duration) == int(audiofile.duration)
        assert a.channels == audiofile.channels
        assert a.samplerate == audiofile.samplerate

        # Now read all the data and assert that it's the correct type.
        for block in a:
            assert type(block) == bytes


@pytest.mark.skipif(
    platform.system() != "Darwin", reason="CoreAudio is only available on macos"
)
def test_macca(audiofile):
    from audioread.macca import ExtAudioFile

    with ExtAudioFile(audiofile.path) as a:
        assert int(a.duration) == int(audiofile.duration)
        assert a.channels == audiofile.channels
        assert a.samplerate == audiofile.samplerate

        # Now read all the data and assert that it's the correct type.
        for block in a:
            assert type(block) == bytes


@pytest.mark.skipif(not audioread._gst_available(), reason="Gstreamer not available")
def test_gstdec(audiofile):
    # can only import gstdec if available
    from audioread.gstdec import GstAudioFile

    with GstAudioFile(audiofile.path) as a:
        assert int(a.duration) == int(audiofile.duration)
        assert a.channels == audiofile.channels
        assert a.samplerate == audiofile.samplerate

        # Now read all the data and assert that it's the correct type.
        for block in a:
            assert type(block) == bytes


@pytest.mark.skipif(not audioread._mad_available(), reason="pymad not available")
def test_maddec(audiofile):
    # can only import mad if available
    from audioread.maddec import MadAudioFile

    with MadAudioFile(audiofile.path) as a:
        assert int(a.duration) == int(audiofile.duration)
        assert a.channels == audiofile.channels
        assert a.samplerate == audiofile.samplerate

        # Now read all the data and assert that it's the correct type.
        for block in a:
            assert type(block) == bytes
