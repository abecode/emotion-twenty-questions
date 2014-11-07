grammar qaFromAnnotation;


options {
    language=Python;
    //output=template;
    backtrack=true;
    output=AST;
    ASTLabelType=CommonTree;

}

tokens {
Emo20q;
Session;
Match;
QA;
Question;
Answer;
Text;
QGloss;
AGloss;
Gloss;
}

@header {
import time
import sys 

print "Let's process the emo20q annotations"   
}          

annotation :	(unit {print $unit.tree.toStringTree();}  )+  -> ^(Emo20q)
	;
unit 	:
	fileStart {print "filestart: " + $fileStart.text} NL
	blankLine  
	matchStart {print "matchstart: " + $matchStart.text} NL
	//matchStart NL
	blankLine  
	( qa	   |
	  blankLine
	 )*
	 attributeList? {print "attributelist; "}
	;

qa	:	qcomp '-' NL acomp -> ^(QA qcomp acomp)
	;
glossStmt
	: 	('gloss' ':' '{' gloss '}' NL)? -> Gloss
	;
gloss 	:	~'}'*
	;
	
qcomp	: 	q  glossStmt -> ^(Question q )
;
q	:      misc (NL misc)? NL  -> ^(Text misc)
	;
acomp	: 	a glossStmt  -> ^(Answer a  )
;
a	: 	misc (NL misc)? NL  -> ^(Answer  ^(Text misc)  )
;

list	:	(ID | ID ':' val) (',' (ID | ID ':' val) )*  
	;
fileStart 
	:	'file' ':' STRING
	;


matchStart
	:	attributeList {print "attributelist: "}
	;	
	
attributeList 
	:	ID ':' val (',' ID ':' val )*
	;
val	:
		(ID('.' ID)* | STRING | INT | ~(','|NL)+ )
		;
	
misc   	:	
	(ID|pUNCT|STRING|INT) (ID|pUNCT|STRING|INT)* 
	;	
	
blankLine
	:
	NL+
	;

fragment	pUNCT
 	:	('.'|'?'|':'|'{'|'}'|','|'!'|'\''|'('|')'|'<'|'>'|'/'|';'|'$'|'='|'&'|'-')
	;


ID  :	('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
    ;

INT :	'0'..'9'+
    ;

NL 	:	'\r'? '\n' 
	;

COMMENT
    :   '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    |   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;

STRING
    :  '"' ( ESC_SEQ | ~('\\'|'"') )* '"'
    ;

fragment
EXPONENT : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

fragment
HEX_DIGIT : ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
ESC_SEQ
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    |   UNICODE_ESC
    |   OCTAL_ESC
    ;

fragment
OCTAL_ESC
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

fragment
UNICODE_ESC
    :   '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT
    ;

//WS  : (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;}
WS  : (' '|'\t'|'\u000C') {$channel=HIDDEN;}
    ;
