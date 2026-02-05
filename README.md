# PDF Sorter

A script using PyMuPDF which takes in a pdf with codes annotated on each page using a text annotation, splits the pdf into files for each code and adds them to a subdirectory for each code.

# Usage

Run main.py with the filename, and an optional --watermark flag to have the source file be watermarked on each page with "SORTED" for ease of identifying already sorted files, as the source file is not deleted after the sorting process.

To prepare a PDF for sorting, open any PDF editor (Microsoft Edge will suffice), and add a text annotation onto a page. If the pages are not oriented correctly, ensure that the text on each page is facing the correct orientation, I.E. if page 1 is upside down, the added text should be upside down also on that page. The script will re-orient all pages with text in the final sorted version based on the orientation of the annotation.

If one does not exist, a subdirectory will be created automatically for each unique annotation, for example a page with "AE000" will result in the creation of a folder called "AE000", should one not already exist. Each page containing an annotation with "AE000" in the source document will be combined into one new PDF, named as a timestamp, which will be moved into the folder "AE000". Any pages containing "AE001" will be combined together and moved into the folder "AE001", etc. 

Should a page contain multiple text boxes, it will appear in multiple of the output documents, for example a page with "AE001" and "AE000" will appear in the files added to both those folders. It should be noted the orientation feature will not work properly should there be text boxes with differing orientations on one page.

As the labels are detected using the annotation feature, typed documents and documents processed with OCR should be supported.
