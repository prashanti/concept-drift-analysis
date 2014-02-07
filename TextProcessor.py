'''
Created on Feb 5, 2014

@author: Dongye
'''

import re
    
def get_new_line(line, flag):
    if flag == 0:
#         return "[Remove]" + line
        return "\n"
    
    return line

def process_one_line(line):
    line = line.strip()
    if line == "":
        print "case 0"
        return "\n"
    special_characters = "\*<>()\[\]{}\-_=\+^\'/"
    
    
    new_line = ""
    pattern_titleID = re.compile("^\s*TitleID:\s*\d+")
    if pattern_titleID.match(line):
        print "case 1"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_itemID = re.compile("^\s*ItemID:\s*\d+")
    if pattern_itemID.match(line):
        print "case 2"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_OCR_not_available = re.compile("^\s*OCR text unavailable for this page.")
    if pattern_OCR_not_available.search(line):
        print "case 3"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_single_integer = re.compile("^\.*\d+(\s*)$")
    if pattern_single_integer.match(line):
        p = pattern_single_integer.match(line)
#         g1 = p.group(1)
#         print ord(g1[0])
#         print ord(line[-1])
        print "case 4"
        new_line = get_new_line(line, 0)
        return new_line
    
    pattern_single_word = re.compile("^\.*[a-zA-Z0-9]+(\s*)$")
    #if len(line) > 2:
        #print line[-3]
    if pattern_single_word.match(line):
        print "case 5"
        new_line = get_new_line(line, 0)
        return new_line
    
    # eg. "3*"
    pattern_digits_and_special_characters = re.compile("^\.*[a-zA-Z0-9"+special_characters+"]+(\s*)$")
    if pattern_digits_and_special_characters.match(line):
        print "case 6"
        new_line = get_new_line(line, 0)
        return new_line
    
    # eg. EMIL BRASS
    max_len = 5
    pattern_words_and_whitespace = re.compile("^[a-zA-Z0-9\s"+special_characters+"]+$")
    pattern_words = re.compile("\w+")
    if pattern_words_and_whitespace.match(line) and pattern_words.search(line):
        words = re.split("\s+", line)
        if len(words) < max_len:
            print "case 7"
            new_line = get_new_line(line, 0)
            return new_line
        
    # If the radio of non-alphabetic characters in a line exceeds a threshold, then remove the line
    threshold = 0.5
    shorted_line = re.sub("[^a-zA-Z\s]", "", line)
    shorted_line = shorted_line.strip()
#     print "short: "+shorted_line
#     print "short len: "+str(len(shorted_line))
#     print ord(shorted_line[0])
#     print ord(shorted_line[1])
#     print ord(shorted_line[-1])
#     print ord(shorted_line[-2]) 
#     print "old: "+line
#     print len(line)
#     print len(shorted_line)
     
#     print "radio: "+str(float(len(shorted_line)) / len(line))
    if float(len(shorted_line)) / len(line) < threshold:
        print "case 8"
#         print "radio: "+str(float(len(shorted_line)) / len(line))
        new_line = get_new_line(line, 0)
        return new_line 
    
    print "case n"
    
    
#     pattern_empty_line = line
#     print ord(pattern_empty_line[0])
    return line


    


def cleanup(dir):

    start = 0
    end = 0

    start = 12
    end = 18
    max_range = 500000

    # line 4579: 3*
    start = 4575
    end = 4580 

    # line 4555: 35 
    start = 4550
    end = 4559

    # line 11647: Ill 
    start = 11645
    end = 11650

    # line: 7338: : ; : . ..,- ~, 
    start = 7335
    end = 7338

    # liine 420531: <^ 
    start = 420531
    end = 420532

    # line 420567: U4 
    start = 420567
    end = 420570

    # line 420619: <T 
    start = 420619
    end = 420620

    # line 420641: .w
    start = 420641
    end = 420642

    # line 420653: >i TJ 
    start = 420653
    end = 420655

    # line 420769: o^ 
    start = 420769
    end = 420770

    # line 420925: CT' 
    start = 420925
    end = 420927

    # line 421325 
    start = 421325
    end = 421327
     
    # line 421419
    start = 421419
    end = 421420
     
    # line 421521
    start = 421521
    end = 421523
     
    start = 421523
    end = 425219
        

    f = open(dir, 'r');



    for i in range(max_range):
        line = next(f)
        if i + 1 >= start and i + 1 <= end:
            print "Line " + str(i + 1) + ":\n" 
            print "\tbefore process: " + line
            new_line = process_one_line(line)
            print "\tafter process: " + new_line

    f.close()




if __name__ == '__main__':
    cleanup("C:\\Users\\Dongye\\Dropbox\\Phenoscape\\EOL\\test.txt")