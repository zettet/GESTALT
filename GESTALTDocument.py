import os.path

def get_language_from_path(path):
    """Retuns a language code based on the extension"""
    language = None;
    fileName, fileExt = os.path.splitext(path);    
    if fileExt == '.cpp':
        language = 'CPP';
    elif fileExt == '.c':
        language = 'C';
    elif fileExt == '.py':
        language = 'PY';
    else:
        language = None;    
    return language;



class GESTALTDocument:
    """Represents all of the necessary information for holding a document in GESTALT"""
    # Properties
    #   File path
    #   Lauguage (C/C++/Java/Python ect...) (Should this only be based on extension?)
    #   Reference to parser class
    #   Containers for method names/definitions, member variables

    def __init__(self,path,tab):
        self.path = path;
        self.language = get_language_from_path(self.path);
        self.parser = None;
        self.tab = tab;

	print "Language: ", self.language
