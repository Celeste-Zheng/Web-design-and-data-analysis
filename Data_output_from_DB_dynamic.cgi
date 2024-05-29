import scipy as sp
import cgi
import cx_Oracle

def main():  # NEW
    #form=cgi.FieldStorage() #cgi script line
    #theStr=form.getfirst('theList','')
    contents = processInput()
    print(contents)

def processInput():  # This function extracts data from an Oracle table.
    con = cx_Oracle.connect('C##Xinru', '123456', 'localhost:1521/XE')
    cur=con.cursor()
    nucleotides = ['A', 'C', 'G', 'T']
    fList=[() for t in range(4)]
    for i in range(4):
        myDict={'nt':nucleotides[i]}        
        query = '''select gi, freq_{nt} from beeGenes where freq_{nt} = (select max(freq_{nt}) from beeGenes)'''.format(nt=nucleotides[i])
        cur.execute(query)
        results = cur.fetchall()  # Fetch all results
        #gi_numbers = '\n'.join([str(x[0]) for x in results])
        #gi_numbers = ''.join(f'<li>{gi_number}</li>' for gi_number, _ in substitutions[aa])
        gi_numbers = '<ul>' + ''.join(f'<li>{x[0]}</li>' for x in results) + '</ul>'

        max_freq = results[0][1] if results else None
        fList[i] = (gi_numbers, max_freq)        
    
    myTuple=()
    for t in range(4):
        myTuple = myTuple + fList[t]

    cur.close()
    con.close()

    return makePage('see_result_template.html', myTuple)

def fileToStr(fileName):
    """Return a string containing the contents of the named file."""
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitutions):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitutions

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()




