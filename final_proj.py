#!/usr/local/bin/env python
#!/usr/local/bin/blastn

import cgi
import json
import os
import mysql.connector
import subprocess
import pandas as pd
from pdf2image import convert_from_path

def blastn():

    #define variables and paths
    print("Content-Type: text/html\n\n")
    print("It worked\n")
    form = cgi.FieldStorage()
    file = form.getvalue("search_file")
    base_path = os.path.join("/var/www/html/jvo5/final")
    out_file = os.path.join(base_path, "blastn_results.csv")
    
    #connect to sql database
    conn = mysql.connector.connect(user='hopkins', password='fakepass', host='localhost', database='xxx')
    cursor = conn.cursor()

    #generate BLASTn output as csv
    print("...generating BLASTn matches...")
    thisCommand = ' '.join(['blastn', '-query', file, '-out', out_file, '-dbtype', 'nucl', "-outfmt 10 qseqid qacc qlen sacc slen qstart qend \
                             qseq evalue length pident mismatch", '-max_target_seqs', '10'])
    blast_run = subprocess.run(thisCommand)

    #create dataframe of BLASTn output
    data = pd.read_csv(r "blast_results.csv")
    #df = pd.DataFrame(data, columns = ["qseqid", "qacc", "qlen", "sacc", "slen", "qstart", "qend", "qseq", "evalue", "length", "pident", "mismatch"])

    #print(json.dumps(df)) #not sure abt this

    print("...creating BLASTn database...")

    #create DB in SQL
    cursor.execute("CREATE TABLE blastn_info (qseqid varchar(50), qacc varchar(50), qlen int, sacc varchar(50), slen int, qstart int, \
                    qend int, qseq varchar(50), evalue int, length int, pident int, mismatch int)")

    #insert pd df data into table
    results= {}
    for row in data.itertuples():
        cursor.execute('''
                    INSERT INTO XXX.dbo.blastn_info (qseqid, qacc, qlen, sacc, slen, qstart, qend, qseq, evalue, length, pident, mismatch) #xxx is database make a name for it
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    '''),
                    row.qseqid,
                    row.qacc,
                    row.qlen,
                    row.sacc,
                    row.slen,
                    row.qstart,
                    row.qend,
                    row.evalue,
                    row.length,
                    row.pident,
                    row.mismatch
                    )

        results[row.qseqid] = [row.qseqid,
                    row.qacc,
                    row.qlen,
                    row.sacc,
                    row.slen,
                    row.qstart,
                    row.qend,
                    row.evalue,
                    row.length,
                    row.pident,
                    row.mismatch]

    conn.close()         
    return results

def main():
    results = blastn()

    #I guess I'm running R here
    command = "Rscript"
    R_path = "path/to/rscript.R"

    #do I have args
    #args = ["X"]

    #Build subproccess command
    cmd = [command, R_path] + args

    #check_output runs command and store result
    R_check = subprocess.check_output(cmd, universal_newlines=True)
    R_run = subprocess.run(cmd)
    #reference r-run in html?
    
    print(json.dumps(results))

    pages = convert_from_path('myBLAST_alignment', 500)
    for page in pages:
        page.save('myBLAST_alignment.png', 'PNG')
        
if __name__ == '__main__':
    main()