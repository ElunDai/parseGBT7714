.PHONY: all clean

all:
	xelatex latex
	biber latex
	xelatex latex

clean:
	latexmk -c -silent
