# append-zip

Appends a file to a zip file, overwriting the existing file there if necessary

## Performance
Not efficient; extracts all the files in the zip, copies over the new file, and compresses a brand new zip replacing the original one. You will need enough disk space to duplicate the zip file.

## Caveats
for some reason, windows has a different file length after unzipping (by 10-20 bytes). So beware how this works on windows

## Getting started

install (on Mac)
`$ python3 -m pip install appendzip`

```py
from appendzip.appendzip import appendzip
# before appendzip calendar.txt in the zip archive test.zip contains 2021-01-02
# before appendzip calendar.txt outside the zip contains 2022-02-03
appendzip(
            pathlib.Path('test.zip'),
            pathlib.Path('calendar.txt'),
            'calendar.txt'
)
# after appendzip calendar.txt inside the zip contains 2022-02-03
# after, there is still only one file in the zip archive test.zip
```