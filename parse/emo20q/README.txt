these are the basic commands used to compile and run a grammar

java -jar antlr3.1.2.wDep.jar nlEmoQuery.g
python nlEmoQueryParser.py  --rule=sentence -i

note that the jar is actually a link (svn copy) to one of the libs in the
antlr directory.  Using the default one is finicky: you need to have some
extra jars on the class path, and you need to call org.antlr.Tool


hello elly!
wtf
