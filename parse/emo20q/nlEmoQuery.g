grammar nlEmoQuery;

options {
language=Python;
output=AST;
ASTLabelType=CommonTree;
}
// imaginary nodes
tokens {
SMLR;
SBST;
}

@header {
print "hey there I'm a parser"
}

@lexer::header {
#package test;
print "hey there I'm a lexer!"
}

@members {
}

dialog:   (sentence  {print $sentence.tree.toStringTree();}| NEWLINE)+ NEWLINE ;

sentence:   statement ('.'|'!')?  {print "statement:" + $statement.text } 
        |   question '?'?         {print "question:" + $question.text } 
        |   request ('.'|'!')?    {print "request:"  + $request.text }
        ;
                
statement  : 'banana' ;	       
query:   'is' 'it' det constraint 'emotion'? '?'? NEWLINE
    ;
    
request 
    	: askExists emotion miscMedia 
    	;
    
askExists 
          : 'is' 'there' ('any'|'some'|'a'|'an')?
          | 'are' 'there' ('any'|'some')?
          | 'do' 'you' 'have' ('any'|'some')?
          ;
          
miscMedia 
	: ('recording'| 'recordings') 
	| ('file'|'files')
	| ('datum'|'data')
	| ('instance'| 'instances')
	| ('object'| 'objects')
	;
    
question 
        : askYN        -> askYN
        | askList      { print "askList:" }
        | askList1     { print "askList1:" }
        | askExplain   { print "askExplain:" }
        ;

askYN    
        : 'are' conjP simConjPred                      -> ^(SMLR conjP )
	| 'is' (e1=emotion->$e1) sim (e2=emotion->$e2) -> ^(SMLR $e1 $e2)
   ;

conjP:	(e1=emotion->$e1) 'and' (e2=emotion->$e2)          -> $e1 $e2;
   
askList  : 'what' 'emotions' 'are' sim emotion ;


askList1 
	:	'what' 'emotion' 'is' sim emotion ;

sim	
	:  'like'                    
	|  'similar' 'to'? 
	;

simConjPred 
	:	'alike'
	|       sim 'each' 'other'
	;
		
askExplain :  'how' ('would'|'do'|'can'|'could') 'you' 'describe' emotion
	|	'what' 'is' emotion 'like'?
	;

emotion :	 'angry' | 'anger' | 'disgusted' | 'disgust' |'fearful' | 'fear' | 'happy' | 'happiness' 
	| 'neutral' | 'neutrality' |'sad' | 'sadness' | 'surprise' | 'surprised' { print "hey!"}
	;
	
det : 'a' 
   | 'an'
   ;
		
constraint
	: 'positive' 
	| 'negative'
	| 'good'
	| 'bad'
	| 'strong'
	| 'weak'
	| 'passionate'
	| 'calm'
	| 'submissive'
	| 'dominant'
	| 'excited'
	| 'extreme'
	| 'neutral'
	| 'desirable'
	| 'undesirable'
	| 'every' 'day'
	| 'unusual'
	| 'common'
	| 'agitated'
	| 'sad'
	| 'happy'
	| 'angry'
	| ID
	;

ID  :   ('a'..'z'|'A'..'Z')+ ;
INT :   '0'..'9'+ ;
NEWLINE:'\r'? '\n' ;
WS  :   (' '|'\t')+ {$channel=HIDDEN;} ;

