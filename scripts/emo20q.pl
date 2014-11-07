sub extractMatches
{
    my @lines = @_;
    my @matches;
  MATCH: for(my $i=0; $i<@lines; $i++)
  {
      next unless $lines[$i] =~ /^match/;
      $lines[$i] =~ /^match: *(.+?),/;

      #go back and find the file name:
      my $logfile;
      for(my $b=$i; $b>=0; $b--)
      {
	  next unless $lines[$b] =~ /^file: *"([^"]+)"/;
	  $logfile = $1;
      }

      warn "no answerer at line $i+1" unless $lines[$i] =~ /answerer: *([^,]+)/;
      my $answerer = $1;

      warn "no questioner at line $i+1" unless $lines[$i] =~ /questioner: *([^,]+)/;
      my $questioner = $1;

      warn "no start at line $i+1" unless $lines[$i] =~ /start: *"([^,]+)"/;
      my $start = $1;

      my @match;
      push @match, $lines[$i];
      
      for($i=$i+1; $i<@lines; $i++)
      {
	  push @match, $lines[$i];
	  
	  if ($lines[$i] =~ /^end:/)
	  {
	      warn "no emotion at line $i+1" unless $lines[$i] =~ /emotion: *([^,]+)/;
	      my $emotion = $1;

	      warn "no end at line $i+1" unless $lines[$i] =~ /end: *"([^"]+)"/;
	      my $end = $1;

	      warn "no question count at line $i+1" unless $lines[$i] =~ /questions: *([^"]+)/;
	      my $questions = $1;

	      push @matches, {'turns'=> \@match, 
			      'emotion' => $emotion,
			      'questioner' => $questioner,
			      'answerer' => $answerer,
			      'start' => $start,
			      'end'   => $end,
			      'questionCount' => $questions,
			      'logfile' => $logfile
				  
	      };
	      next MATCH;
	  }
      }
  }
    return @matches;

}

sub extractQAPairs
{
    my @lines = @_;
    my @qas;
  QA: for(my $i=0; $i<@lines; $i++)
  {
      next unless $lines[$i] =~ /^-/;
      #get question
      my $q;
      warn "no qgloss at line $i" if $lines[$i-1] !~ /^gloss:{(.+)}/;
      $q->{gloss} = $1;
      my $p=2;
      my $tmp = "";
      while($lines[$i-$p] !~ /^ *$/)
      {
	  $tmp = $lines[$i-$p] . " " . $tmp;
	  $p++;
      }
      $q->{text} = $tmp;

      #get answer
      my $a;
      $i++;
      warn "no atext at line $i+1" if $lines[$i] =~ /^gloss:{(.+)}/;
      $tmp = "";
      while($lines[$i] !~ /^gloss/)
      {
	  $tmp .= $lines[$i] . " ";
	  $i++;
      }
      $a->{text} = $tmp;
      warn "no agloss at line $i" if $lines[$i] !~ /^gloss:{(.+)}/;
      $a->{gloss} = $1;
      
      next if $q->{gloss} eq "giveup";
      next if $q->{gloss} eq "clarification";
      next if $q->{gloss} eq "non-yes-no";
      push @qas, {"q" => $q,"a" => $a};
      
  }
    return @qas;
}



1;
