#!/usr/bin/perl -w

use strict;
 
use POSIX;  #for floor function
use Storable;

my $knowledge;                  # data is stored emotion->question->answer
my $lexicalAccess;          # maps from logical question to text form
my $evidence;                   # keeps track of evidence for emotions

my $shortTermMemory;                        # store info from current dialog
 
my $understanding;   


#read in the data from the annotated question answer pairs
for(`scripts/extractQuestions.pl`)
{
    chomp;
    die unless /^(.+?)\t(.+?)\t(.+?)\t(.+?)\t(.+?)$/;
    my($matchNum,$emotion,$rawQ,$question,$answer) = ($1,$2,$3,$4,$5);
    #print join("\t", $matchNum, $emotions{$emotion},$questions{$question},$answer);
    #print "\n";
    next if $question =~ /^e==/;
    $emotion =~ s|/.*||;      #remove synonyms
    #$knowledge->{$emotion}->{$question} = $answer;
    $knowledge->{$emotion}->{$question}->[$answer+1]++;
    push @{$lexicalAccess->{$question}}, $rawQ;
}

store $knowledge, 'knowledge';
store $lexicalAccess, 'lexicalAccess';


