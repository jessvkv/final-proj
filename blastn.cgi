#!usr/local/bin/blastn

import os
from os import path

thisCommand = ' '.join(['blastn', '-query', seq_text, '-out', "blastn_results.csv", '-dbtype', 'nucl', "-outfmt 10 qseqid qacc qlen sacc slen qstart qend \
                         qseq evalue length pident mismatch", '-max_target_seqs', '10'])
