grammar emo20q;

options {
language=Python;
output=AST;
ASTLabelType=CommonTree;
backtrack=true;
memoize=true;
}
// imaginary nodes
tokens {
SMLR;
SBST;
CNSTR;
VAL;
ACT;
DOM;
E;
AskYN;
Guess;
AskExists;
AskList;
Media;
Audio;
Video;
Image;
Text;
Blog;
Story;
MiscData;
EmoInventory;
}

@header {
import time
import sys
sys.path.append("/home/abe/thesis/hudson/python/")
import EmotionVocab
v = EmotionVocab.EmotionVocab("/home/abe/thesis/hudson/iemocapFuzzySets.csv")

print "Let's play emotion 21 questions"
#time.sleep(1)
print "Just wait while I think of an emotion......"
#time.sleep(3)
print "Okay, I got one.  You may start guessing"
}

@lexer::header {
#package test;
#print "hey there I'm a lexer!"
}

@members {
}

dialog:   (sentence  
//{print "sentence: " + $sentence.tree.toStringTree();} 
NEWLINE?)+ ;

sentence:   statement ('.'|'!')?   -> statement
        |   question '?'?        {print $question.tree.toStringTree();}  -> question 
        |   request ('.'|'!')?     -> request
        |   COMMENT               
        ;
        
COMMENT	:	'#' .*  NEWLINE {$channel=HIDDEN;} 
       ;        
                
statement  : 'banana' ;	       
    
request 
    	: askExists emotion miscMedia -> ^(AskExists ^( CNSTR emotion miscMedia) )
    	;
    
askExists 
          : 'is' 'there' ('any'|'some'|'a'|'an')? 
          | 'are' 'there' ('any'|'some')?
          | 'do' 'you' 'have' ('any'|'some')?
          ;
          
miscMedia 
	: ('recording'| 'recordings')  ->  ^(Media MiscData)
	| ('file'|'files')             ->  ^(Media MiscData)
	| ('datum'|'data')             ->  ^(Media MiscData)
	| ('instance'| 'instances')    ->  ^(Media MiscData)
	| ('object'| 'objects')        ->  ^(Media MiscData)
	| ('image'|'images')           ->  ^(Media Image)
	| ('blog' | 'blogs' | 'weblog' | 'weblogs') -> ^(Media Blog)
	| ('story' | 'stories')        ->  ^(Media Story)
	;
    
question 
        : askYN -> ^(AskYN askYN) 
        | askList -> ^(AskList askList)
        ;

askYN    
        : 'are' conjP simConjPred                      -> ^(SMLR conjP )
	| 'is' (e1=emotion->$e1) sim (e2=emotion->$e2) -> ^(SMLR $e1 $e2)
	| 'is' 'it' sim emotion  -> ^(SMLR emotion E)
	| 'is' ('it'|'the' 'emotion') emotion {$emotion.text == 'happy'}?         -> ^(CNSTR emotion E)
	| 'is' emotion ('the' 'emotion')?     {$emotion.text == 'happy'}?         -> ^(CNSTR emotion E)
//	| 'is' ('it'|'the' 'emotion') emotion {$emotion.text == 'happy'}?         -> ^(Guess emotion)
//	| 'is' emotion ('the' 'emotion')?     {$emotion.text == 'happy'}?         -> ^(Guess emotion)
	| 'is' 'it' det? constraint+ 'emotion'?        -> ^(CNSTR constraint+ E)
	| 'does' 'it' 'have' constraint+               -> ^(CNSTR constraint+ E)
	| 'does' 'it' 'make' 'you' 'feel' constraint+  -> ^(CNSTR constraint+ E)
	| 'is' 'it' det 'emotion' 'that' ('makes'|'would' 'make' | 'will' 'make' | 'could' 'make') abstractPerson 'feel' constraint+  -> ^(CNSTR constraint+ E)
	| 'is' 'it' det 'emotion' 'that' ('makes'|'would' 'make' | 'will' 'make' | 'could' 'make') abstractPerson constraint+ -> ^(CNSTR constraint+ E)
	| 'is' 'it' det 'emotion' 'that' 'is' constraint+  -> ^(CNSTR constraint+ E)
	| 'is' 'it' det 'emotion' 'with' constraint+  -> ^(CNSTR constraint+ E)
	| 'does' 'it' (constraint)+                      -> ^(CNSTR constraint+ E)
   ;
abstractPerson 
	:	('you'|'one'|'someone'|'a' 'person'|'somebody'|'me')
	;

conjP:	(e1=emotion->$e1) 'and' (e2=emotion->$e2)      -> $e1 $e2;
   
askList  : 'what' 'emotions' 'are' sim emotion 
 	| 'what' ('are' 'the'?)? 'emotions' 'that'? ('exist' | 'do'? 'you' 'know' 'about'?) -> EmoInventory

;


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
	| 'neutral' | 'neutrality' |'sad' | 'sadness' | 'surprise' | 'surprised' 
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
	| 'fearful'
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

ID  :   ('a'..'z'|'A'..'Z'|'-')+ ;
INT :   '0'..'9'+ ;
NEWLINE:'\r'? '\n' ;
WS  :   (' '|'\t')+ {$channel=HIDDEN;} ; 
