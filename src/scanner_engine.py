#! /usr/bin/env python

#main gestalt engine 

#I propose that the the scanner maintain a 
#(forgive me for my java syntax here) hash map 
#of scanned words. The scanner should exist independantly
#and scan through all library files and included files.
# --EDIT--
# library files would only have to be examined every so often
# so, maybe gestalt could run these at some random time and store
# the results in a text file, then whenever gedit is opened, 
# it could just load the results in
# --------
# Then, it would create a "cache" of identifiers. If a
# file is modified, it would only have to "rescan" that file. 

# also, if user has multiple languages open, scanner_engine
# could have a thread/process running for each language detected
#although at this point this is a "could have" goal. Let's get it
#working for c++ first : )
 
# other thoughts:
# Maybe we should build our own custom "cache-map" data structure?
# Also, we need a way to dynamically evoke syntax highlighting 
# based on the language. Obviously, this would be based on the 
# file extension, but how should we run the code? 
# perhaps the scanner should load in a "definitions" file or
# something using the template design method or something similar

print "hello world!"
