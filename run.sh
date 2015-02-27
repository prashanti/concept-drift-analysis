
# download corpus
python GetBHLCorpus.py

# clean OCR text
python ocrcleanup.py ../data/Corpus/

# check OCR Scores
python checkocrquality.py ../data/CleanedCorpus/ ../data/OCRScores.txt

# separate Low Quality corpora
python removelowquality.py 60

# merge high quality corpora into yearly corpora
python mergehighquality.py

# create yearly original and cleaned files for graphs 
python groupyearly.py ../data/Corpus/ ../data/CleanedCorpus/

# get scores of high quality yearly corpora
python checkocrquality.py /Users/pmanda/Documents/eolbhl_hackathon/data/ScoredCorpus/HighQualityYearlyCorpora/ ../data/Stats_Graph/OCRScores_YearlyHighQuality.txt

# annotate high quality yearly corpora
python anntatetext.py ../data/ScoredCorpus/HighQualityYearlyCorpora/ UBERON

# create comprehensive distribution 
python createcompdist.py ../data/UBERONDistributionsExact/


# get sufficient terms for each bin size. This also creates files of sufficient terms for each bin size
python getbinsizestats.py 


# group yearly corpora into groups based on bin size
python groupannotations-percents.py ../data/UBERONDistributionsExact/PerYearCounts.txt ../data/UBERONAnnotatedFilesExact/ 10

# get context vectors for the appropriate bin size
python getcontextvectors.py ../data/GroupedAnnotations/ ../data/SufficientTerms/9_Bins_Terms.txt

# compare context vectors
python comparecontextvectors.py ../data/ContextVectors/