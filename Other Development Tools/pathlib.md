* [Creating path objects](#creating)
* [Getting path components](#components)
* [Getting path information](#info)
* [Joining paths](#join)
* [Manipulating files and directories](#manipulation)
* [Links](#links)
* [Reading and writing files](#read-write)
* [Globs](#globs)
* [Other useful methods](#other)



<a id="creating"></a>
# Creating path objects

* `Path.cwd()`: get current working directory
* `Path.home()`: home directory
* `Path(__file__)`: current module's file path
  * current module is the file that Python is currently importing or executing
* `Path('path')`: instantiating Path with a string
  * use raw string literals to avoid problems with slashes: `Path(r'C:\Users\GreatUser\folder\file.txt')`
* `p.absolute()`: get absolute path



<a id="components"></a>
# Getting path components

The following examples are based on the file `/opt/data/file.txt`

* `.name`: (str) filename (without directories)
  * `Path('/opt/data/file.txt').name == 'file.txt'`
* `.stem`: (str) filename without file extension
  * Removes the part after the last dot: `Path('/a/b/c.d.e.f').stem == 'c.d.e'`
* `.suffix`: (str) file extension
  * `Path('/opt/data/file.txt').suffix == '.txt'`
* `.suffixes`: (List[str]) list of all after-dot-parts of the filename:
  * `Path('/opt/data/file.txt.gz').suffixes == ['.txt', '.gz']`
* `.anchor`: (str) part of the path before the directories
  * `Path('/opt/data/file.txt').anchor == '/'`
  * `Path('opt/data/file.txt').anchor == ''`
* `.parent`: (Path) directory containing the file, or the parent directory if the path is a directory
  * given `p = Path('/opt/data/file.txt')'`
  * `p.parent == Path('/opt/data/')`
  * `p.parent.parent == Path('/opt/')`
  * `p.parent.parent.parent == Path('/')`
* `.parents`: (Iterable[Path]) an iterable of all parents
```
>>> list(p.parents)
[PosixPath('/opt/data/HPO_NLP'), PosixPath('/opt/data'), PosixPath('/opt'), PosixPath('/')]
```
* `.parts`: (Tuple[str]) all components of the path:
```
Path('/opt/data/file.txt.gz').parts 
('/', 'opt', 'data', 'file.txt.gz')
```



<a id="info"></a>
# Getting path information

Below, `p = Path('/opt/data/file.txt.gz`.

* `p.exists`: whether the path exists
* `path.stat()`: return the result of `stat()` system call on this path, like `os.stat()` does
* `path.lstat()`: same as `stat()` but if the path points to a symlink, the symlink's
    status information is returned, rather than its target's
* `p.is_absolute()`: whether path is absolute (has both a root and, if applicable, a drive)
* `p.is_dir()`: whether path is a directory
  * returns False if no object in the filesystem exists with such path
* `p.is_file()`: whether path is a regular file (or a symlink pointing to regular file)
  * returns False if no object in the filesystem exists with such path
* `p.is_symlink()`: whether path is a symbolic link
* `p.group()`: the group name of the file gid
* `p.owner()`: the login name of the file owner



<a id="join"></a>
# Joining paths

You can use `/` to join paths together (even on Windows): `new_path = path_1 / path_2 / path_3` where `path_1` is `Path`
object, and the others can be simple strings or also Path objects.

Example:
```
Path('../tmp/') / 'xyz' / 'a'              # PosixPath('../tmp/xyz/a')
Path('../tmp/') / Path('xyz') / Path('a')  # PosixPath('../tmp/xyz/a')
```

Another option: `p.joinpath(path_1, path_2, ...)`.



<a id="manipulation"></a>
# Manipulating files and directories

* `p.mkdir(mode=511, parents=False, exist_ok=False)`: create a new directory at the given path
* `p.rmdir()`: remove the directory (it must be empty)
* `p.touch(mode=438, exist_ok=True)`: create file at the given path
* `p.replace`: rename the current path to the target path, overwriting if the target path exists.
  * Relative paths are interpreted relative to the current working directory, *not* the directory of the Path object.
* `p.unlink`: remove the file or link
  * if the path is a directory, use `p.rmdir()` instead
* Pathlib doesn't have support for copying files, so `shutil` or `os` should be used
  * `shutil` can also be used to remove full directory tree including intermediate directories (`p.rmdir()` deletes one
  at a time)



<a id="links"></a>
# Links

* `p.hardlink_to(target)`: make the path a hard link to target
* `p.is_symlink()`: return True if the path points to a symbolic link, False otherwise
* `p.lchmod(mode)`: like Path.chmod() but, if the path points to a symbolic link, the symbolic link’s mode is changed 
  rather than its target’s.
* `p.lstat()`: like Path.stat() but, if the path points to a symbolic link, return the symbolic link’s information 
  rather than its target’s.
* `p.readlink()`: return the path to which the symlink points
* `p.resolve()`: make the path absolute, resolving any symlinks
  * `..` components are also eliminated (this is the only method to do so)
* `p.symlink_to(target)`: make the path a symbolic link to target
* `p.unlink(missing_ok=False)`: remove file or symbolic link



<a id="read-write"></a>
# Reading and writing files

Method `p.open(mode='r', buffering=-1, encoding=None, errors=None, newline=None)` is almost identical to the built-in
`open` and returns a file object just as `open` does.

* `p.read_text(encoding=None, errors=None)`: open the file in text mode, read it, and close the file.
* `p.read_bytes()`: open the file in bytes mode, read it, and close the file.
* `p.write_text(data, encoding=None, errors=None)`: open the file in text mode, write to it, and close the file.
* `p.write_bytes(data)`: open the file in bytes mode, write to it, and close the file.



<a id="globs"></a>
# Globs

* `p.glob(pattern)`: glob the given relative pattern in the directory represented by this path, yielding all matching 
  files (of any kind)
  * Patterns are the same as for fnmatch, with the addition of “**” which means “this directory and all subdirectories, 
    recursively”. In other words, it enables recursive globbing
  * Using the “**” pattern in large directory trees may consume an inordinate amount of time.
* `p.rglob(pattern)`: this is like calling Path.glob() with “**/” added in front of the given relative pattern.



<a id="other"></a>
# Other useful methods

* `p.chmod(mode, *, follow_symlinks=True`: change the file mode and permissions
  * This method normally follows symlinks. Some Unix flavours support changing permissions on the symlink itself; 
  on these platforms you may add the argument follow_symlinks=False, or use lchmod().
* `p.expanduser()`: return a new path with expanded ~ and ~user constructs, as returned by os.path.expanduser().
  * If a home directory can’t be resolved, RuntimeError is raised.
* `p.iterdir()`: iterate over the files in this directory. Does not yield any result for the special paths '.' and '..'.
* `p.lchmod(mode)`: like Path.chmod() but, if the path points to a symbolic link, the symbolic link’s mode is changed 
  rather than its target’s.
* `p.match(path_pattern)`: whether path matches the given pattern
```
>>> p = Path('/opt/data/files/file.json.gz')
>>> p.match('*.gz')
True
>>> p.match('*.json*')
True
>>> p.match('*.json.gz')
True
>>> p.match('/opt/*')
False
>>> p.match('/opt/data/*')
False
>>> p.match('/opt/data/*/*')
True
>>> p.match('/opt/data/*/*.json.gz')
True
```
* `p.samefile(other_path)`: whether this path points to the same file as *other_path* which can be either a Path
  object, or a string.\
* `p.with_name(name)`:
```
>>> p = Path('/opt/data/files/file.json.gz')
>>> p.with_name('dataset.jsonl')
PosixPath('/opt/data/files/dataset.jsonl')
```
* `p.with_stem(stem)`:
```
>>> p = Path('/opt/data/files/file.json.gz')
>>> p.with_stem('dataset')
PosixPath('/opt/data/files/dataset.gz')
```
* `p.with_suffix(suffix)`: return a new path with the file suffix changed. If the path has no suffix, add given suffix. 
  If the given suffix is an empty string, remove the suffix from the path.
```
>>> p = Path('/opt/data/files/file.json.gz')
>>> p.with_suffix('')
PosixPath('/opt/data/files/file.json')
>>> p.with_suffix('.jsonl')
PosixPath('/opt/data/files/file.json.jsonl')
```
