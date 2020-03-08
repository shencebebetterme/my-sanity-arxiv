#!/bin/sh
#cd /Users/cary/Documents/DesktopCopy/arXiv/arxiv-sanity-preserver-master
# ./download_pdfs_hyperthreading.sh

python3 fetch_papers.py
python3 download_pdfs.py
python3 parse_pdf_to_text.py
python3 thumb_pdf.py
python3 analyze.py 
python3 buildsvm.py
python3 make_cache.py

#sudo service mongod start
python3 serve.py
