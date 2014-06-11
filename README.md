# ffindex for Python

This module enables Python reading support for Andy Hauser's [ffindex](http://pubshare.genzentrum.lmu.de/scientific_computing/software/ffindex/) format in Python using `mmap` and python generators. The entries returned by ffindex are file-like objects that support `read`, `readline`, `seek`, `tell`, etc. It was tested on Python 2.7.7, Python 3.4.1 and pypy 2.4.0

## Installation

	$ pip install ffindex

Alternatively, you can clone this repository somewhere and create a symbolic link to the `ffindex` subfolder inside of your project.

## Demo

From a clone of the git repo, you can generate 10 random files and compare their `sha1sum` outputs with the SHA1 checksums calculated by the Python script:

	import ffindex
	import sys
	import hashlib

	if len(sys.argv) != 2:
	    print("usage: {prog} ffindex_data".format(prog=sys.argv[0]))
	    sys.exit(1)

	for entry in ffindex.read(sys.argv[1]):
	    m = hashlib.sha1()
	    m.update(entry.read())

	    print("{sha1}  {name}".format(name=entry.name, sha1=m.hexdigest()))

Run it on the shell:

	$ for i in {1..10}; do dd if=/dev/urandom of=file-$i bs=1M count=5; done
	$ sha1sum file-*
	[ some SHA1 hashes ]
	$ ffindex_build demo-archive{,.index} file-*
	$ ./demo.py demo-archive
	[ some SHA1 hashes ]
	$ diff <( sha1sum file-* ) <( ./demo.py demo-archive  )
	[ no diff output! ]

Please note that the current `ffindex_apply` (as bundled with HH-suite 2.0.16) seems to include an additional \x00 at the end of the file so the result of running `sha1sum` with `ffindex_apply` will differ from the above checksums.


## FAQ

  * **I want readline to return Unicode, not byte strings!** - You can specify the `encoding='UTF-8'` setting on the `ffindex.read` command to automatically make `readline()` return Unicode strings: `ffindex.read('my_file', encoding='UTF-8')`

  * **I have a different filename structure than X and X.index!** - You can specify separate filenames for database and index using the first two positional arguments of `ffindex.read`: `ffindex.read('my_file.db', 'my_file.index')`

  * **How is the performance?** - I've tried to be efficient in implementing this (patches welcome!). The `sha1sum` demo above takes ~8s to process 1000x2 MB files on my machine while using `ffindex_apply` to pipe the same data to `sha1sum` takes 12s :)

## License
MIT

