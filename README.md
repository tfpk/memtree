# Memtree

<img src="resources/favicon.jpg"/>

## What is it?

This project aims to integrate with gdb, so that from the commandline you can visually inspect data-structures.

The aim is to get it to be useful in teaching, and demonstrating errors in student code.

## How do I install it?

The code isn't fully set-up yet, so there's no simple install script.

That said, if you have some C code (for instance, the code in `example/tree/`), you can use a one-liner like:

```sh
$ <your-c-compiler> -g -o program <file>.c
$ gdb -q -ex="source ~/<path-to-memtree>/gdb_ext/gdb_commands.py" -ex="b main" -ex="r" ./tree
...
(gdb) jserve <variable>
```

## How do I use it?

Go to the webserver (probably at `0.0.0.0:8000`) and look around!

## Examples

<img src="resources/example_photos/Memtree_tree.png"/>
<img src="resources/example_photos/Memtree_complex_tree.png"/>
