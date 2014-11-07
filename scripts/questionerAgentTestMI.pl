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
    #$knowledge->{$emotion}->{$question} = $answer;
    $knowledge->{$emotion}->{$question}->[$answer+1]++;
    push @{$lexicalAccess->{$question}}, $rawQ;
}

#store $knowledge, 'knowledge';
#store $lexicalAccess, 'lexicalAccess';
#die;

$evidence->{$_} = 1 for keys %$knowledge;

$understanding = makeSense($knowledge,$evidence);

sub makeSense
{
    my ($knowledge,$evidence) = @_;
    my $turnCount;
    my $questionCounts;
    my $questionOutcomeCounts;
    
    # set up counts
    foreach my $e (keys %$knowledge)
    {
	foreach my $q (keys %{$knowledge->{$e}})
	{
	    for my $x (-1 .. 1)
	    {
		$turnCount += $knowledge->{$e}->{$q}->[$x+1]
		    if defined $knowledge->{$e}->{$q}->[$x+1];
		$questionCounts->{$q} += $knowledge->{$e}->{$q}->[$x+1]
		    if defined $knowledge->{$e}->{$q}->[$x+1];
		$questionOutcomeCounts->{$q}->[$x+1] += $knowledge->{$e}->{$q}->[$x+1]
		    if defined $knowledge->{$e}->{$q}->[$x+1];
	    }
	}
    }
    
    # calculate question entropy
    my $questionEntropy;
    foreach my $q (keys %$questionOutcomeCounts)
    {
	for my $x (-1 .. 1)
	{
	    $questionOutcomeCounts->{$q}->[$x+1] = 0 
		if not defined $questionOutcomeCounts->{$q}->[$x+1];
	    #my $p = $questionOutcomeCounts->{$q}->[$x+1]/$questionCounts->{$q};
	    my $p = $questionOutcomeCounts->{$q}->[$x+1]/$turnCount;
	    my $log = ($p==0) ? 0 :log($p)/log(2);
	    $questionEntropy->{$q} += - $p * $log;
	}
    }

    my @sortedQuestions = sort {$questionEntropy->{$b} <=> $questionEntropy->{$a}} keys %$questionOutcomeCounts;

    foreach my $q (sort {$questionEntropy->{$b} <=> $questionEntropy->{$a}} keys %$questionEntropy)
    {
	print $q, "\t", $questionEntropy->{$q}, "\n";
	print "\t$_:", $questionOutcomeCounts->{$q}->[$_+1] for (-1 .. 1);
	print "\n";
    }
    
    # calculate emotion entropy
    my $emotionEntropy;
    my $emotionCount;
    $emotionCount += $evidence->{$_} for keys %$evidence;
    foreach my $e (keys %$evidence)
    {
	my $p = $evidence->{$e}/$emotionCount;
	$emotionEntropy->{$e} = - $p * log($p)/log(2);
    }

    my @sortedEmotion = sort {$emotionEntropy->{$b} <=> $emotionEntropy->{$a}} keys %$emotionEntropy;
    
    my $etot =0; $etot += $emotionEntropy->{$_} for keys %$emotionEntropy;
    print "total emotion entropy: ", $etot, "\n";
    
    
    my $i = 0;
    while (my $logicQ = shift @sortedQuestions)
    {
	$i++;
	#my @q = keys %$questionCounts;
	#my @g = @{$lexicalAccess->{$q[floor(rand(scalar @q))]}};
	my @g = @{$lexicalAccess->{$logicQ}};
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
	my $ans = 0;
	$ans = 1 if $in =~ /^(:?yes|yea|yeah|yep|yup|yes*|definitely) *(:?it is)?$/;
	$ans = -1 if $in =~ /^(:?no|nope|no*|nono) *(:?it is not|it isn'?t)?$/;
	print "$ans\n";
	
	#update short term memory
	foreach my $emotion (keys %$knowledge)
	{
	    if(exists $knowledge->{$emotion}->{$logicQ})
	    {
		my ($yesFactor,$noFactor);
		
		$noFactor = 
		    (defined $knowledge->{$emotion}->{$logicQ}->[0]) ?
		    $knowledge->{$emotion}->{$logicQ}->[0] :
		    0;
		
		$yesFactor =  
		    (defined $knowledge->{$emotion}->{$logicQ}->[2]) ?
		    $knowledge->{$emotion}->{$logicQ}->[2] :
		    0;
		$shortTermMemory->{$emotion}->{$logicQ} = 
		    $ans * ($yesFactor - $noFactor);
		# ToDo: go thru and make inference 
		#print $emotion, "\t";
		#print $shortTermMemory->{$emotion}->{$logicQ}, "\t";
		$evidence->{$emotion} *= 2**$shortTermMemory->{$emotion}->{$logicQ};	    
	    }else{
		$shortTermMemory->{$emotion}->{$logicQ} = 0;
	    }
	}
	
	# calculate emotion entropy from evidence
	# *comment out: try calc entropy from shortTermMemory
	my $evidenceCount = 0;
	my $evidenceEntropy;
	$evidenceCount += $evidence->{$_} for keys %$evidence;
	foreach my $e (keys %$evidence)
	{
	    my $p = $evidence->{$e}/$evidenceCount;
	    $evidenceEntropy->{$e} = - $p * log($p)/log(2);
	}
	
	#calc emotion entropy from shortTermMemory:
	my $memoryCount=0;
	my $memoryEntropy;
	foreach my $e (keys %$shortTermMemory) {
	    foreach my $q (keys %{$shortTermMemory->{$e}}) {
		$memoryCount += (defined $shortTermMemory->{$e}->{$q}) ?
		    abs($shortTermMemory->{$e}->{$q}) : 0;
		    #1 : 0;
	    }
	}
	foreach my $e (keys %$shortTermMemory) 
	{
	    foreach my $q (keys %{$shortTermMemory->{$e}})
	    {
		my $p = ($memoryCount==0)? 
		    0 : abs($shortTermMemory->{$e}->{$q}) / $memoryCount;
		    #0 : 1 / $memoryCount;
		print $p, "\t";
		$memoryEntropy->{$e} += 
		    ($p==0) ? 0 : - $p * log($p)/log(2); 
	    }
	    print "\n";
	}

	print "memory count: ", $memoryCount, "\n";
	print $_, "\t", $memoryEntropy->{$_}, "\n" for 
	    sort { $memoryEntropy->{$b} <=> $memoryEntropy->{$a} } 
	keys %$memoryEntropy;
	print "\n";

	print $_, "\t", $evidenceEntropy->{$_}, "\n" for 
	    sort { $evidenceEntropy->{$b} <=> $evidenceEntropy->{$a} } 
	keys %$evidenceEntropy;
	$etot =0; $etot += $evidenceEntropy->{$_} for keys %$evidenceEntropy;
	print "total emotion entropy: ", $etot, "\n";


	# for (sort { $evidence->{$b} <=> $evidence->{$a} } keys %$evidence)
	# {
	#     print $_, "\t";
	#     print 	$evidence->{$_}, "\n";
	#}
	last if $i > 10;
	# update evidence/question list
	# add up the evidence in short term memory

	# the idea i'm trying here is to sort the questions by their possibility to raise
	# the entropy of the memory, given the knowledge
	# (also try joint entropy of memory & questions)

	# calculate question vs memory entropy
	my $questionVsMemoryEntropy;
	foreach my $q (keys %$questionOutcomeCounts)
	{
	    # for the question part, we just use question entropy
	    #calc the memory part, ie, the entropy increase expected from asking q
	    my %copyMemoryEntropy; 
	    %copyMemoryEntropy = %{$memoryEntropy};  #shallow copy
	    my $copyMemoryCount = $memoryCount;
	    foreach my $e (keys %$knowledge) {
		my $count = 0;
		for my $x (-1 .. 1)
		{
		    $count += (defined $knowledge->{$e}->{$q}->[$x+1]) ?
			abs($knowledge->{$e}->{$q}->[$x+1]*$x) : 0;
			#1 : 0;
		    
		}
		$copyMemoryCount += $count;
		#my $p = (exists $knowledge->{$e}->{$q}->[0] and exists $knowledge->{$e}->{$q}->[2])? 
		#    ($knowledge->{$e}->{$q}->[2] +  $knowledge->{$e}->{$q}->[0]) / $copyMemoryCount
		#    : 0;
		my $p = $count/$copyMemoryCount;
		$copyMemoryEntropy{$e} += ($p == 0) ?
		    0 : ( - $p * log($p)/log(2)); 
	    }
	    my $totalPredictedEntropy;
	    my $totalPredictedEntropyChange;
	    $totalPredictedEntropy += $copyMemoryEntropy{$_} for keys %copyMemoryEntropy;
	    $totalPredictedEntropyChange += ($copyMemoryEntropy{$_}-$memoryEntropy->{$_})
		for keys %copyMemoryEntropy;
	    #$questionVsMemoryEntropy->{$q} *= $totalPredictedEntropy;
	    #print $q, "\t", $totalPredictedEntropy, "\t", $totalPredictedEntropyChange, "\n";
	    $questionVsMemoryEntropy->{$q} = $totalPredictedEntropy;
	}
	
	
	my @newSortedQuestions;
	
	#shift @sortedQuestions;  #get rid of current question
	
	@newSortedQuestions =
	    sort 
	{
	    $questionVsMemoryEntropy->{$b} <=> $questionVsMemoryEntropy->{$a}
	}
	@sortedQuestions;
	#keys %$questionVsMemoryEntropy;
	@sortedQuestions = @newSortedQuestions;
	fisher_yates_shuffle(\@sortedQuestions,$i*$i);
	print $_, "\t", $questionVsMemoryEntropy->{$_}, "\n" for reverse @sortedQuestions
	
	#printShortTermMemory($shortTermMemory);
    }
}

sub printShortTermMemory 
{
    my $in = shift;
    foreach my $e (keys %$in)
    {
	print $e, "\n";
	foreach my $q (keys %{$in->{$e}})
	{
	    print $q, "\t";
	    print $in->{$e}->{$q}, "\n";
	}
	print "\n";
    }
}

# fisher_yates_shuffle( \@array ) : generate a random permutation # of @array in place 
# extra parameter limits shuffle to first n elements
sub fisher_yates_shuffle 
{  
    my $array = shift; 
    my $limit = scalar @$array;
    my $altLimit = shift if @_;
    $limit = $altLimit if $altLimit < $limit;
    my $i; 
    for ($i = $limit; --$i; ) 
    { 
	my $j = int rand ($i+1); 
	next if $i == $j; 
	@$array[$i,$j] = @$array[$j,$i]; 
    } 
} 

my (@guesses) = sort {$evidence->{$b} <=> $evidence->{$a}} keys %$evidence;

print $_, "\t", $evidence->{$_}, "\n" for @guesses;
