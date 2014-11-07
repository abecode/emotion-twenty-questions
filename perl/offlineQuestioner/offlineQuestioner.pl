#!/usr/bin/perl -w

#use Data::Dumper;


my $knowledge;       
my $lexicalAccess;   


#####################################################
# The data is the secret sauce: read it in
#####################################################

#read in human-human data
open IN, "humanHumanResults_2011-10-31.txt";
while (<IN>)
{
    chomp;
    next if /^ *$/;
    my ($emo,$q,$a) = split /\t/, $_;
    $emo = lc($emo);
    next if $emo =~ /^ *$/;
    next if $q =~ /^e==/;
    $knowledge->{$emo}->{$q}->[classifyYN($a)+1]++;
}
close IN;

#logical to lexical mapping
open IN, "lexicalAccess_2011-10-31.txt";
while (<IN>)
{
    chomp;
    next if /^ *$/;
    my ($qtext,$qgloss) = split /\t/, $_;
    next if $qtext =~ /^ *$/;
    next if $qgloss =~ /^ *$/;
    next if $qgloss =~ /^e==/;
    push @{$lexicalAccess->{$qgloss}}, $qtext;

}
close IN;

#read from past online data
open IN, "onlineResults_2011-10-28.txt";
while (<IN>)
{
    chomp;
    next if /^ *$/;
    my ($emo,$q,$a) = split /\t/, $_;
    $emo = lc($emo);
    next if $emo =~ /^ *$/;
    $knowledge->{$emo}->{$q}->[classifyYN($a)+1]++;
}
close IN;




#####################################################
# set up the list of questions and emotions
#####################################################

my @stimuli = keys %$lexicalAccess;  #the questions are the stimuli
my @emotions = keys %$knowledge;
my $unkEmo;   #keep a vector of values for each asked question
@stimuli = sortQuestionsByEntropy(\@stimuli,$knowledge);
#fisher_yates_shuffle(\@stimuli,4); 



#####################################################
# start asking
#####################################################
while (1)
{
    print generateTextRealization($stimuli[0]), "\n";
    my $response = <STDIN>;
    my $eval = classifyYN($response);
    #print $eval;
    $unkEmo->{$stimuli[0]}->[$eval+1] ++; 
    
    my $compatibility = calcEmoCompatibility($knowledge,$unkEmo);
    shift @stimuli;

    my @compatibilities;
    push @compatibilities, [$_,$compatibility->{$_}] 
	for sort{$compatibility->{$b} <=> $compatibility->{$a} } keys %$knowledge;
    
    #check the front runner
    #if(($similarities[0][1] - 0.5 * $distance->{$similarities[0][0]}) > $similarities[1][1])

    #check if there is an emotion with high similarity to distance ratio
    # (ie compatibility)

    if($compatibilities[0][1] > $compatibilities[1][1])
    {
	my $e = $compatibilities[0][0];
	print $e, "?...", "\n";
	my $response = <STDIN>;
	my $eval = classifyYN($response);
	$unkEmo->{"e==$e"}->[$eval+1] ++; 
	
	if( $eval == 1 )
	{
	    print "did I get it?\n";
	    my $response = <STDIN>;
	    my $eval = classifyYN($response);
	    if($eval == 1)
	    {
		print "Cool!\n";
		exit(0);
	    }
	}
	else   #delete the emotion
	{
	    print "okay, I'll scratch $e off my list\n";
	    delete $knowledge->{$e};
	}
    }
    
    my %focalKnowledge = %$knowledge;
    delete $focalKnowledge{$_} for grep {$compatibility->{$_} < 2} keys %$knowledge;
    @stimuli = reorderQuestions(\@stimuli,\%focalKnowledge,$unkEmo);
    
}

sub calcEmoCompatibility
{
    my $knowledge = shift;
    my $unkEmo = shift;

    my $distance;
    my $similarity;
    my $compatibility;
    $distance->{$_->{emo}} = $_->{val} for 
	map { 
	    { 'emo' => $_,
	      'val' => emotionDistance($unkEmo,$knowledge->{$_}) }} 
    keys %$knowledge;  
    $similarity->{$_->{emo}} = $_->{val} for 
	map { 
	    { 'emo' => $_,
	      'val' => emotionSimilarity($unkEmo,$knowledge->{$_}) }} 
    keys %$knowledge;  
    $compatibility->{$_->{emo}} = $_->{val} for 
	map { 
	    { 'emo' => $_,
	      'val' => $similarity->{$_}/($distance->{$_}+ 0.25) }} 
    keys %$knowledge;  


    my (@similarities,@distances,@compatibilities);
    push @similarities, [$_,$similarity->{$_}] 
	for sort{$similarity->{$b} <=> $similarity->{$a} } keys %$knowledge;
    push @distances,   [$_,$distance->{$_}] 
	for sort{$distance->{$b}   <=> $distance->{$a}   } keys %$knowledge;
    push @compatibilities, [$_,$compatibility->{$_}] 
	for sort{$compatibility->{$b} <=> $compatibility->{$a} } keys %$knowledge;
    

    #print $_->[0], ":", $_->[1], ", " for @similarities;
    #print "\n\n";
    #print $_->[0], ":", $_->[1], ", " for @distances;
    #print "\n\n";
    #print $_->[0], ":", $_->[1], ", " for @compatibilities;
    #print "\n\n";
    
    return $compatibility;
}



#this is questionable: can be improved
sub reorderQuestions
{
    my $arrayRef = shift;
    my $knowledge = shift;
    my $unkEmo = shift;
    
    my $distance;
    my $similarity;
    my $compatibility;

    $distance->{$_->{q}} = $_->{val} for 
	map { 
	    { 'q' => $_,
	      'val' => questionDistance($unkEmo,$_,$knowledge) }} 
    @$arrayRef;  
    # $similarity->{$_->{q}} = $_->{val} for 
    # 	map { 
    # 	    { 'q' => $_,
    # 	      'val' => questionSimilarity($unkEmo,$_,$knowledge) }} 
    # @$arrayRef;  
    # $compatibility->{$_->{q}} = $_->{val} for 
    # 	map { 
    # 	    { 'q' => $_,
    # 	      'val' => $similarity->{$_}/($distance->{$_}+ 0.25) }} 
    # @%arrayRef;  


    my (@similarities,@distances,@compatibilities);
    #push @similarities, [$_,$similarity->{$_}] 
    #   for sort{$similarity->{$b} <=> $similarity->{$a} } keys %$knowledge;
    # push @distances,   [$_,$distance->{$_}] 
    # 	for sort{$distance->{$b}   <=> $distance->{$a}   } keys %$knowledge;
    # push @compatibilities, [$_,$compatibility->{$_}] 
    # 	for sort{$compatibility->{$b} <=> $compatibility->{$a} } keys %$knowledge;
    #die;
    my (@new) = sort { $distance->{$b} <=> $distance->{$b} } @$arrayRef;
    #print $_, ", " for @new;
    #print "\n";
    @new;
}

#this is questionable: can be improved
sub questionDistance
{
    my $unkEmo = shift;
    my $q = shift;
    my $knowledge = shift;

    my $tmpDist = 0;
    foreach my $askedQ (keys %$unkEmo)
    {
	foreach my $emo (keys %$knowledge)
	{
	    $tmpDist    +=  
		$knowledge->{$emo}->{$q}->[0] * $knowledge->{$emo}->{$askedQ}->[2]
		if (defined $knowledge->{$emo}->{$q}->[0] 
		    and defined $knowledge->{$emo}->{$askedQ}->[2] );
	    $tmpDist    +=  
		$knowledge->{$emo}->{$q}->[2] * $knowledge->{$emo}->{$askedQ}->[0]
		if (defined $knowledge->{$emo}->{$q}->[2] 
		    and defined $knowledge->{$emo}->{$askedQ}->[0] );

	    $tmpDist    +=  
		$knowledge->{$emo}->{$q}->[0] * $knowledge->{$emo}->{$askedQ}->[0]
		if (defined $knowledge->{$emo}->{$q}->[0] 
		    and defined $knowledge->{$emo}->{$askedQ}->[0] );

	    $tmpDist    +=  
		$knowledge->{$emo}->{$q}->[2] * $knowledge->{$emo}->{$askedQ}->[2]
		if (defined $knowledge->{$emo}->{$q}->[2] 
		    and defined $knowledge->{$emo}->{$askedQ}->[2] );

	}
    }
    return $tmpDist;
}




sub emotionDistance
{
    my $e1 = shift;  #assuming that first arg has subset of attributes
    #print Dumper($e1);
    my $e2 = shift;  #compared to the second arg 
    my $tmpDist = 0;
    foreach my $askedQ (keys %$e1)
    {

	$tmpDist    +=  $e1->{$askedQ}->[0] * $e2->{$askedQ}->[2]
	    if defined $e1->{$askedQ}->[0] and defined $e2->{$askedQ}->[2];
	$tmpDist    +=  $e1->{$askedQ}->[2] * $e2->{$askedQ}->[0]
	    if defined $e1->{$askedQ}->[2] and defined $e2->{$askedQ}->[0];

    }
    return $tmpDist;
}

sub emotionSimilarity()
{
    my $e1 = shift;  #assuming that first arg has subset of attributes
    #print Dumper($e1);
    my $e2 = shift;  #compared to the second arg 
    my $tmpSim = 0;
    foreach my $askedQ (keys %$e1)
    {

	$tmpSim    +=  $e1->{$askedQ}->[0] * $e2->{$askedQ}->[0]
	    if defined $e1->{$askedQ}->[0] and defined $e2->{$askedQ}->[0];
	$tmpSim    +=  $e1->{$askedQ}->[2] * $e2->{$askedQ}->[2]
	    if defined $e1->{$askedQ}->[2] and defined $e2->{$askedQ}->[2];
	$tmpSim    +=  $e1->{$askedQ}->[1] * $e2->{$askedQ}->[1]
	    if defined $e1->{$askedQ}->[1] and defined $e2->{$askedQ}->[1];

    }
    return $tmpSim;
}

sub fisher_yates_shuffle {  #for randomizing the stimuli
    my $array = shift;
    my $limit = @_ ? shift : @$array;
    $limit = @$array if $limit > @$array;
    my $i;
    for ($i = $limit; $i>=0; $i--) {
        my $j = int rand ($i+1);
        next if $i == $j;
        @$array[$i,$j] = @$array[$j,$i];
    }
}

sub generateTextRealization
{
  my $logicQ = shift;
  my @g = @{$lexicalAccess->{$logicQ}};
  my $q = $g[rand(scalar(@g))];
  $q =~ s/(:?number )?\d\d? *[.)]*//;   # remove question numbers
  $q =~ s/^ *//;                        # and other junk ... 
  $q =~ s/ *$//; 
  return $q;
}

#this is bullshit and should be improved when other things are fine
sub sortQuestionsByEntropy
{

  my $qs = shift; # get reference to question list
  my $k = shift; # get knowledge
  my $turnCount;
  my $questionCounts;
  my $questionOutcomeCounts;
  
  # set up counts
  foreach my $e (keys %$k)
  {
      foreach my $q (keys %{$k->{$e}})
      {
	  for my $x (-1 .. 1)
	  {
	      $turnCount += $k->{$e}->{$q}->[$x+1]
		  if defined $k->{$e}->{$q}->[$x+1];
		$questionCounts->{$q} += $k->{$e}->{$q}->[$x+1]
		    if defined $k->{$e}->{$q}->[$x+1];
	      $questionOutcomeCounts->{$q}->[$x+1] += $k->{$e}->{$q}->[$x+1]
		  if defined $k->{$e}->{$q}->[$x+1];
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
	  $questionEntropy->{$q} += (- $p * $log);
      }
  }

    my @sortedQuestions = sort {$questionEntropy->{$b} <=> $questionEntropy->{$a}} @$qs;
    return @sortedQuestions;
}

sub classifyYN
{
   my $in = shift;
   return 0 if not defined $in;
   $in =~ s/[^A-Za-z ]//g;               # remove punctuation 
   $in =~ s/^ *//;
   $in =~ s/ *$//;
   #decide whether it's yes/no/other (1/-1/0)
   my $ans = 0;
   $ans = 1 if $in =~ /^(:?yes|yea|yeah|yep|yup|yes*|definitely) *(:?it is)?$/;
   $ans = -1 if $in =~ /^(:?no|nope|no*|nono) *(:?it is not|it isn'?t)?$/;
   return $ans;
}


