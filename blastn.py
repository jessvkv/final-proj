#!usr/local/bin/blastn

import cgi
import json
import os
import mysql.connector
import subprocess
import pandas as pd
from pdf2image import convert_from_path
import tarfile
from os import path

def blastn():

    #define variables and paths
    form = cgi.FieldStorage()
    seq_text = form.getvalue("search_text")
    base_path = os.path.join("/var/www/html/jvo5/final")
    out_file = os.path.join(base_path, "blastn_results.csv")
    
    #connect to sql database
    conn = mysql.connector.connect(user='jvo5', password='Mor!@2012', host='localhost', database='jvo5')
    cursor = conn.cursor()

    #generate BLASTn output as csv
    print("...generating BLASTn matches...")
    thisCommand = ' '.join(['blastn', '-query', seq_text, '-out', "blastn_results.csv", '-dbtype', 'nucl', "-outfmt 10 qseqid qacc qlen sacc slen qstart qend \
                             qseq evalue length pident mismatch", '-max_target_seqs', '10'])
    blast_run = subprocess.run(thisCommand)

    #create dataframe of BLASTn output
    data = pd.read_csv("blast_results.csv")
    #df = pd.DataFrame(data, columns = ["qseqid", "qacc", "qlen", "sacc", "slen", "qstart", "qend", "qseq", "evalue", "length", "pident", "mismatch"])

    #print(json.dumps(df)) #not sure abt this

    print("...creating BLASTn database...")

    #create DB in SQL
    cursor.execute("CREATE TABLE blastn_info (qseqid varchar(50), qacc varchar(50), qlen int, sacc varchar(50), slen int, qstart int, \
                    qend int, qseq varchar(50), evalue int, length int, pident int, mismatch int)")

    #insert pd df data into table
    results= {}
    for row in data.itertuples():
        cursor.execute(('''
                    INSERT INTO jvo5.dbo.blastn_info (qseqid, qacc, qlen, sacc, slen, qstart, qend, qseq, evalue, length, pident, mismatch) 
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

if __name__ == "__blastn__":
    blastn()