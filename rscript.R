#R things

mySeqFile <- blast_results.csv 
mySeq <- readDNAStringSet(mySeqFile)

myAlignment <- msa(mySeq)
msaPrettyPrint(myAlignment, output="pdf", file="myBLAST_alignment" y=c(164, 213), subset=c(1:6), showNames = "none", showLogo = "none", consensusColor = "ColdHot", showLegend = FALSE, askForOverwrite = FALSE)

