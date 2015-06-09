all:
	export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
	bin/nutch inject urls/ranurag
	bin/nutch generate -topN 80
	bin/nutch fetch -all
	bin/nutch parse -all
	bin/nutch updatedb -all


generate:
	bin/nutch generate -topN 80
	bin/nutch fetch -all
	bin/nutch parse -all
	bin/nutch updatedb -all


dropnutchdb:
	python dropdatabase.py
