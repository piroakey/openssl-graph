.PHONY: all
all:

.PHONY: make env
env:
	pip install -r requirements.txt

.PHONY: make clearenv
cleanenv:
	pip freeze > freeze.tmp
	pip uninstall -y -r freeze.tmp
	$(RM) freeze.tmp

.PHONY: distclean
distclean:
	$(RM) dist/*

# git archive HEAD
.PHONY: archive
archive:
	git archive HEAD -o sources.zip
