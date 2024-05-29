#!/usr/bin/env python
'''Prompt the user for personal information and display a web page.'''
import cgi
import cx_Oracle
import find_max

def main():
    form = cgi.FieldStorage()
    theFile = form.getfirst('filePath')
    contents = processInput(theFile)
    print(contents)

def processInput(theFile):
    con = cx_Oracle.connect('C##Xinru', '123456', 'localhost:1521/XE')
    cur = con.cursor()
    try:
        cur.execute('DROP TABLE beeGenes')
    except cx_Oracle.DatabaseError:
        pass  # Assume error due to table not existing
    cur.execute('''
        CREATE TABLE beeGenes (
            gi VARCHAR2(10),
            sequence CLOB,
            freq_A NUMBER,
            freq_C NUMBER,
            freq_G NUMBER,
            freq_T NUMBER,
            freq_GC NUMBER
        )
    ''')
    cur.bindarraysize = 50
    max_sequence_length = find_max.find_max(theFile)

    cur.setinputsizes(10, max_sequence_length+100, float, float, float, float, float)
    
    myStr = ''
    infile = open(theFile, 'r')
    for aline in infile:
        if aline.startswith('>'):
            myStr = myStr + aline + '_**gene_seq_starts_here**_'
        else:
            myStr = myStr + aline
    strL = myStr.replace('\n', '')
    records = strL.split('>')[1:]

    for record in records:
        start = record.find('gi|') + 3
        end = record.find('|', start)
        gi = record[start:end]
        
        start = record.find('**gene_seq_starts_here**_') + 25
        sequence = record[start:]

        freq_A = sequence.count('A') / len(sequence)
        freq_C = sequence.count('C') / len(sequence)
        freq_G = sequence.count('G') / len(sequence)
        freq_T = sequence.count('T') / len(sequence)
        freq_GC = freq_G + freq_C

        # Insert data into database
        cur.execute('''
            INSERT INTO beeGenes (gi, sequence, freq_A, freq_C, freq_G, freq_T, freq_GC) VALUES
            (:gi, :sequence, :freq_A, :freq_C, :freq_G, :freq_T, :freq_GC)''', (gi, sequence, freq_A, freq_C, freq_G, freq_T, freq_GC))

    con.commit()
    cur.close()
    con.close()
    return makePage('done_submission_Template.html', "Thank you for uploading.")

def fileToStr(fileName):
    """Return a string containing the contents of the named file."""
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitutions):
    """Generate HTML page from template and substitutions."""
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitutions


try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()

