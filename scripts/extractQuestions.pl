#!/usr/bin/perl -w

require "scripts/emo20q.pl";
use Data::Dumper;

open IN, "annotate/emo20q.txt";
my @lines = map {chomp; $_} <IN>;
close IN;

my @matches = extractMatches(@lines);
my $matchNum = 0;
foreach (@matches){
    $matchNum ++;
    my @qas = extractQAPairs(@{$_->{turns}});
    my $emotion = $_->{emotion};
    print Dumper( $_)
	if not $emotion;
    die "$matchNum\n" 
	if not $emotion;
    for (@qas) {
	print $matchNum, "\t";
	print  $emotion, "\t";
	print $_->{q}->{text}, "\t";
	print $_->{q}->{gloss}, "\t";
	print quantizeYN($_->{a}->{gloss}), "\t";
	#print $_->{q}->{text};
	print "\n" ;
    }
}



sub quantizeYN
{
    $_ = shift;
    die "no input to quantizeYN" if not $_;
    my $out = 0;
    #normalize:
    s/hint,//;
    s/cheer,//;
    s/jeer,//;
    s/clarification:t-\d,//;
    s/clarification,//;
    s/done,//;
    s/judgement:difficult,//;
    s/qualification:(?:un)?certain,//;
    s/qualification:subjective,//;
    s/status(?:Request)?,//;
    s/humor,//;

    s/,hint//;
    s/,cheer//;
    s/,jeer//;
    s/,clarification:t-\d//;
    s/,clarification//;
    s/,done//;
    s/,judgement:difficult//;
    s/,qualification:(?:un)?certain//;
    s/,qualification:subjective//;
    s/,status(?:Request)?//;
    s/,humor//;
    $out = 1 if /^yes$/;
    $out = -1 if /^no$/;
    $out = 1 if /(?:frequently|general|usually|hedge|probably):yes/;
    $out = -1 if /no,close/;
    $out = -1 if /(?:frequently|general|usually|hedge|probably):no/;
    $out = 0 if /possible:yes,necessary:no/;
    #print $out, "\n";
    #return $_;
    return $out;
}



