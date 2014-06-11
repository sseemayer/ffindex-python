# ffindex for Python

This module enables Python reading support for Andy Hauser's `ffindex` format in Python using `mmap` and python generators. It was tested on Python 2.7.7, Python 3.4.1 and pypy 2.4.0

## Installation

	$ pip install ffindex

## Demo

From a clone of the git repo, you can generate 10 random files and compare their `sha1sum` outputs with the SHA1 checksums calculated by the Python script:

	$ for i in {1..10}; do dd if=/dev/urandom of=file-$i bs=1M count=5
	$ sha1sum file-*
	[ some SHA1 hashes ]
	$ ffindex_build demo-archive{,.index} file-*
	$ ./demo.py demo-archive
	[ some SHA1 hashes ]
	$ diff <( sha1sum file-* ) <( ./demo.py demo-archive  )
	[ no diff output! ]

Please note that the current `ffindex_apply` (as bundled with HH-suite 2.0.16) seems to include an additional \x00 at the end of the file so the result of running `sha1sum` with `ffindex_apply` will differ from the above checksums.

## License
MIT

