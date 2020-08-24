#!/usr/local/bin/python3

import cgi
import json
import os
import mysql.connector
import subprocess
import pandas as pd
from pdf2image import convert_from_path
import tarfile
from os import path

#variables n stuff
blastn_path = os.path.join("/var/www/html/jvo5/final/final-proj/blastn.py")

def main():
    results = blastn_path

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
    
    print(json.dumps(results))
   
if __name__ == '__main__':
    main()
    
#myBLAST_alignment is the R output as pdf. This will save to the server.
pages = convert_from_path('myBLAST_alignment', 500)
for page in pages:
    page.save('myBLAST_alignment.png', 'PNG')
       
#I guess if you wildin' here's a tar.gz file of the blastn DB
def make_tarfile(BLAST_results, source_dir):
    with tarfile.open(BLAST_results, "w:gz") as tar:
        tar.add(source_dir, arcname = os.path.basename(source_dir))
