.PHONY: all clean

all: out.bib
	xelatex latex
	biber latex
	xelatex latex

out.bib: input.txt ../parseGBT7714.py
	ipython ../parseGBT7714.py input.txt out.bib

clean:
	latexmk -c -silent
