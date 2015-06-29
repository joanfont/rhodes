PROJECT=MemoriaTFG
TEX=pdflatex -synctex=1 -interaction=nonstopmode
BIBTEX=bibtex
BUILDTEX=$(TEX) $(PROJECT).tex
BUNDLE=$(PROJECT).pdf

all:
	$(BUILDTEX)
	$(BIBTEX) $(PROJECT)
	$(BUILDTEX)
	$(BUILDTEX)

clean:
	rm -f *.dvi *.log *.bak *.aux *.bbl *.blg *.idx *.ps *.eps *.pdf *.toc *.out *.log *.lot *.brf *.synctex.gz *.lof *~
