#!/usr/bin/perl -w

use POSIX;  #for floor function

my $knowledge;                  # data is stored emotion->question->answer
my $questionGenerator;          # maps from logical question to text form
my $questionCounts;             # counts numbers of logical questions asked
my $questionCountsDefinite;     # counts definite (yes/no) answers

#read in the data from the annotated question answer pairs
for(`scripts/extractQuestions.pl`)
{
    chomp;
    die unless /^(.+?)\t(.+?)\t(.+?)\t(.+?)\t(.+?)$/;
    my($matchNum,$emotion,$rawQ,$question,$answer) = ($1,$2,$3,$4,$5);
    #print join("\t", $matchNum, $emotions{$emotion},$questions{$question},$answer);
    #print "\n";
    next if $question =~ /^e==/;
    $knowledge->{$emotion}->{$question} = $answer;
    push @{$questionGenerator->{$question}}, $rawQ;
    $questionCounts->{$question} ++;
    $questionCountsDefinite->{$question} ++ if $answer != 0;
}

#sort questions by number of definite answers
@sortedQuestions = sort {$questionCountsDefinite->{$b} <=> $questionCountsDefinite->{$a}} keys %$questionCountsDefinite;

#print $_, ": ", $questionCountsDefinite->{$_}, "\n" for keys %$questionCountsDefinite;

my $shortTermMemory;                        # store info from current dialog

my $i = 0;
while (my $logicQ = shift @sortedQuestions)
{
    $i++;
    #my @q = keys %$questionCounts;
    #my @g = @{$questionGenerator->{$q[floor(rand(scalar @q))]}};
    my @g = @{$questionGenerator->{$logicQ}};
    my $q = $g[rand(scalar(@g))];
    $q =~ s/(:?number )?\d\d? *[.)]*//;   # remove question numbers
    $q =~ s/^ *//;                        # and other junk ...
    $q =~ s/ *$//;
    print $q, "\n";

    #process user input
    my $in = <>;                          # get user input
    $in =~ s/[^A-Za-z ]//g;               # remove punctuation 
    $in =~ s/^ *//;
    $in =~ s/ *$//;
    #decide whether it's yes/no/other (1/-1/0)
    my $a = 0;
    $a = 1 if $in =~ /^(:?yes|yea|yeah|yep|yup|yes*|definitely) *(:?it is)?$/;
    $a = -1 if $in =~ /^(:?no|nope|no*|nono) *(:?it is not|it isn'?t)?$/;
    print "$a\n";
    
    #update short term memory
    foreach my $emotion (keys %$knowledge)
    {
	if(exists $knowledge->{$emotion}->{$logicQ})
	{
	    $shortTermMemory->{$emotion}->{$logicQ} =
		$a * $knowledge->{$emotion}->{$logicQ}
	    ;
	}else{
	    $shortTermMemory->{$emotion}->{$logicQ} = 0;
	}
	
    }
    last if $i > 10;
}

# add up the evidence in short term memory
my $evidence;
foreach my $emotion (keys %$shortTermMemory)
{
    foreach my $question (keys %{$shortTermMemory->{$emotion}})
    {
	$evidence->{$emotion} += $shortTermMemory->{$emotion}->{$question};
    }
}

my (@guesses) = sort {$evidence->{$b} <=> $evidence->{$a}} keys %$evidence;

print $_, "\t", $evidence->{$_}, "\n" for @guesses;
