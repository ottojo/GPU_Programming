PANDOC_BASE_OPTIONS=--standalone
PANDOC_HTML_OPTIONS=$(PANDOC_BASE_OPTIONS) --toc -w html5 --css=styling.css --mathjax
PANDOC_PDF_OPTIONS=$(PANDOC_BASE_OPTIONS) -V links-as-notes=true --pdf-engine=xelatex


styling.css:
	curl -L -O https://b.enjam.info/panam/styling.css

html: styling.css
	pandoc $(shell cat pandoc_list.txt) -o index.html $(PANDOC_HTML_OPTIONS)

pdf-1:
	pandoc Exercise1/pdf_header.md Exercise1/exercise1.md -o exercise1.pdf $(PANDOC_PDF_OPTIONS)

pdf-4:
	pandoc Exercise4/pdf_header.md Exercise4/ex4.md -o exercise4.pdf $(PANDOC_PDF_OPTIONS)

clean:
	rm -f exercise1.pdf exercise4.pdf index.html
