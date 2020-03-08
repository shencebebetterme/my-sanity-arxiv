#!/bin/sh
#chmod +x test_pdf.sh


# clear corrupted files

 cd ../data/txt
 for txtfile in *.txt; do
 	filesize=`du -b "$txtfile" | cut -f1`
 	if [ "$filesize" -eq 0 ]; then
	 	pdffile=${txtfile%.txt}
		jpgfile=$pdffile.jpg
 		echo "$txtfile" corrupted, removing "$txtfile", "$pdffile", "$jpgfile"
 		rm "$txtfile"
		rm "../pdf/$pdffile"
		rm "../../codes/static/thumbs/$jpgfile"
 	else
 		: Nothing
 	fi
 done










