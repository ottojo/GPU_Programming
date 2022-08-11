PANDOC_BASE_OPTIONS=--standalone
PANDOC_HTML_OPTIONS=$(PANDOC_BASE_OPTIONS) --toc -w html5 --css=styling.css --mathjax
PANDOC_PDF_OPTIONS=$(PANDOC_BASE_OPTIONS) -V links-as-notes=true --pdf-engine=xelatex


styling.css:
	curl -L -O https://b.enjam.info/panam/styling.css

html: styling.css
	pandoc $(shell cat pandoc_list.txt) -o exercises.html $(PANDOC_HTML_OPTIONS)

pdf-1:
	pandoc Exercise1/pdf_header.md Exercise1/exercise1.md -o exercise1.pdf $(PANDOC_PDF_OPTIONS)

pdf-4:
	pandoc Exercise4/pdf_header.md Exercise4/ex4.md -o exercise4.pdf $(PANDOC_PDF_OPTIONS)

pdf-5:
	pandoc Exercise5/pdf_header.md Exercise5/ex5.md -o exercise5.pdf $(PANDOC_PDF_OPTIONS)

pdf-6:
	pandoc Exercise6/pdf_header.md Exercise6/ex6.md -o exercise6.pdf $(PANDOC_PDF_OPTIONS)

pdf-7:
	pandoc Exercise7/pdf_header.md Exercise7/ex7.md -o exercise7.pdf $(PANDOC_PDF_OPTIONS)

pdf-8:
	pandoc Exercise8/pdf_header.md Exercise8/ex8.md -o exercise8.pdf $(PANDOC_PDF_OPTIONS)

pdf-9:
	pandoc Exercise9/pdf_header.md Exercise9/ex9.md -o exercise9.pdf $(PANDOC_PDF_OPTIONS)

summary-html: styling.css
	pandoc Summary/main.md -o summary.html $(PANDOC_HTML_OPTIONS)

clean:
	rm -f exercise1.pdf exercise4.pdf exercise5.pdf exercise6.pdf exercise7.pdf exercise8.pdf exercise9.pdf index.html exercises.html summary.html
