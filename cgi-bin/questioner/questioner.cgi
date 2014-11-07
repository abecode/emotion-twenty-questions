#!/usr/bin/perl -w

BEGIN {
    my $base_module_dir = (-d '/home/compling/perl' ? '/home/compling/perl' : ( getpwuid($>) )[7] .
'/perl/');
    unshift @INC, map { $base_module_dir . $_ } @INC;
}

use CGI;                            # the cgi module
use CGI::Session qw(:standard);     # the session module
use DBI;                            # the database module
use Storable;

no warnings 'redefine';             # to be remove in production (this prevents some anoying warnings

#connect to db  ... see below for db info

#this is the external user for security limitation
my $dbh = DBI->connect("DBI:mysql:compling_emo20qExtern;host=compling.org", "compling_extern", "opensource");

my $cgi = new CGI;                                  # use cgi module to process form data

my $sidp = $cgi->param("CGISESSID");
my $sidc = $cgi->cookie("CGISESSID");

my $session = new CGI::Session (                    # use session to maintain persistant info
				"driver:MySQL",     # store session using mysql
				$cgi,              # use default serializer: Data::Dumper
				{Handle=>$dbh}    
				);
$cgi->param("CGISESSID", $session->id());

print $session->header(-charset => "UTF-8");

$session->flush();

init($cgi, $session, $dbh);  # this checks if the user is logged in (sets session var "~logged-in") and more (see below)

my $focusScript = '
function setFocus()
{
     document.getElementById("response").focus();
}
';

print $cgi->start_html(-title  => "EMO20Q Questioner Agent",
                       -author => "abe.kazemzadeh\@gmail.com",
                       -script => $focusScript,
                       -onload => "setFocus()",
                       -head   => $cgi->Link({-rel=>'icon',-href=>'favicon.ico'}),
                       #-onload => "document.getElement",
);

##################################################
# LOGIN
#################################################

unless ( $session->param("~logged-in") ) {

    #print login_page($cgi, $session);

    print "\n<br>\n";

    print $cgi->h1("EMO20Q Questioner Agent");

    print $cgi->p(
	"Welcome to Emotion Twenty Questions.  Please pick an emotion (not necessarily how you feel right now--it can be any emotion)."),
        $cgi->p("After you fill out the form, I will try to guess the emotion that you have in your mind. "),
        $cgi->p( "Please communicate with me as you would a real life person, for example if we were chatting online."),
        $cgi->p( "Answer the questions to the best of your ability and see if I have high enough verbal emotional intelligence to guess your emotion correctly."),
        $cgi->p( "After you answer each question, just hit return to move on to the next question."),
        $cgi->p( "Each game will take approximately 5 minutes and you are welcome to play as much as you like.");

	

    print $cgi->p("Please log in with your first name, email address, and native language."); 

   
    print $cgi->start_form(-method=>"GET"); #login form

    print $cgi->textfield(-name=>'lg_name', -value=>'', -size=>30, -id => 'response',
    -maxlength=>30); 
    print "(Name)\n"; 
    print "\n<br>\n"; 

    print $cgi->textfield(-name=>'lg_email', -value=>'', -size=>30,
    -maxlength=>30); 
    print "(Email)\n"; 
    print "\n<br>\n"; 

    print $cgi->textfield(-name=>'nativeLang', -value=>'', -size=>30,
    -maxlength=>30); 
    print "(Native language)\n"; 
    print "\n<br>\n"; 

    print $cgi->submit(
		       
		       #-name=>'button_name', #-value=>'value' 
		       
			       );

    
    print "\n<br>\n"; print $cgi->end_form();

    exit(0);
    
}
 


update_data($cgi, $session, $dbh);



##################################################
# LOGOUT
#################################################
#if( $cgi->param('cmd') and $cgi->param('cmd') eq "logout" )
if( $session->param('~logout')  ) 
{
    print 
	$cgi->h1("goodbye", capitalize($session->param("~profile")->{name})),
	$cgi->p("Thanks for playing.."),
	$cgi->p("If you want to tell me something, please send an email to kazemzad\@usc.edu\n"),
	$cgi->p("To restart, click <a href='questioner.cgi'> here </a> or your browser's refresh button\n"),
        
        ;
    
    if($cgi->param("cmd") eq "finish") 
    {
	my($sec,$min,$hour,$mday,$mon,$year,$wday,
	   $yday,$isdst)=localtime(time);
	my $dtEnd = sprintf "%4d-%02d-%02d %02d:%02d:%02d\n",
	$year+1900,$mon+1,$mday,$hour,$min,$sec;

	my $result = $dbh->do("INSERT INTO matches (username,useremail,session,agent,start,end,emotion,success,comment) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
			      undef,
			      $session->param("~profile")->{name},
			      $session->param("~profile")->{email},
			      $session->id(),
			      "v1", undef,$dtEnd,
			      $cgi->param("emotion"),
			      $cgi->param("success"),
			      $cgi->param("comment")
	);	
    }

    
    $session->clear(['stimuli', 'current_guess','~logout', '~logged-in', 'outcome']);
    $session->flush();
    $session->delete;
    exit(0);
}

##################################################
# SUCCESS
#################################################
if( $session->param('outcome') eq 'success'  )
{
  print 
    $cgi->h1("Cool!"),
    $cgi->p("just to make sure I understood correctly and continue to improve my game, could you please fill out the following:"),
    $cgi->start_form(-method =>"get"),
    $cgi->p("what emotion did you pick? "),
    $cgi->textfield( -name => 'emotion', -size => 80, -maxlength=>80),
    "<br/>\n",
    $cgi->p("Are there any observations you'd like to share? "),
    "<br/>",
    $cgi->textarea( -name => 'comment', -rows=>3,  -columns => 80),
    "<br/>",
    $cgi->hidden( -name => 'success', -default => 1, -override => 1),
    $cgi->submit(-name => "cmd", -value => "finish"),
    $cgi->end_form();

    $session->clear('outcome');
    $session->param("~logout", 1);
    $session->flush();

   print $cgi->end_html;
   exit(0);
}
    


##################################################
# FAILURE
#################################################
if( $session->param('outcome') eq 'failure'  )
{
  print 
    $cgi->h1("Darn!"),
    $cgi->p("just to make sure I understood correctly and continue to improve my game, could you please fill out the following:"),
    $cgi->start_form(-method =>"get"),
    $cgi->p("what emotion did you pick? "),
    $cgi->textfield( -name => 'emotion', -size => 80, -maxlength=>80),
    "<br/>\n",
    $cgi->p("Are there any observations you'd like to share? "),
    "<br/>",
    $cgi->textarea( -name => 'comment', -rows=>3,  -columns => 80),
    "<br/>",
    $cgi->hidden( -name => 'success', -default => 0, -override => 1),
    $cgi->submit(-name => "cmd", -value => "finish"),
    $cgi->end_form();

    $session->clear('outcome');
    $session->param("~logout", 1);
    $session->flush();

    print $cgi->end_html;
    exit(0);

}




##################################################
# The Main part
#################################################



print 
    #------------------
    #print the top div
    #------------------
    "<div id='status' style='background-color: #aaaaff;'>\n",
    "<span style='float: left; background: transparent; width: auto; margin: 0; padding:0'>", 
    "Your session :  ", 
    capitalize($session->param("~profile")->{name}),
    " (", $session->param('current_guess'), "/", 20,
    "). ",
    "</span>\n",
    $cgi->start_form(-method=>"get",
		     -style=>'float: right; background: transparent;'),
    $cgi->submit(-name=>'cmd',
		 -value=>'logout'),
    $cgi->end_form(),
    "<br>\n",
    "</div>" ,
    ;

print $cgi->start_form(-method=>"GET"); # input form start

if($session->param('current_guess')<10)   #q/a
{

#my $qid = $session->param('stimuli')->[$session->param('current_guess')];
my $qid = $session->param('stimuli')->[0];
my $q = generateTextRealization( $qid );

my($sec,$min,$hour,$mday,$mon,$year,$wday,
   $yday,$isdst)=localtime(time);
my $dt = sprintf "%4d-%02d-%02d %02d:%02d:%02d\n",
$year+1900,$mon+1,$mday,$hour,$min,$sec;

print 
    #------------------
    #print the stimuli
    #------------------
    "<br>",
    "<div id='stimulus-area' style='background-color: #aaffaa;width: 80% '>\n",
    "The question is: ", 
    "<br>",
    "<div id='stimulus' style='margin-left:20%'>",
    "<b>",
    $q,
    $cgi->hidden( -name => 'stimulus', -default => $q, -override => 1),
    $cgi->hidden( -name => 'qid', -default => $qid, -override => 1),
    $cgi->hidden( -name => 'startTime', -default => $dt, -override => 1),
    #    $cgi->hidden( -name => CGISESSID, -default => $session->id()),
    $cgi->hidden( -name => 'cmd', -default => 'next'),
	
    "</b>",
    "</div>",
    "<br>",
    "</div>",
    ;
    
    print 
    "<br/>",
    #------------------
    # the text box
    #------------------ 
    #$cgi->textarea( -name => 'response', -id => 'response',
    #                -rows => 3,
    #                -columns => 80),
    
    $cgi->textfield( -name => 'response', -id => 'response',
                     -override => 1,
                     -size => 80,
                     -maxlength => 200,
	             -tabindex =>1),
    "<br/",
    ;

    #print 
    #------------------
    # the submit button
    #------------------ 
    #"<br/>",
    #$cgi->submit(-name => "cmd", 
    #         -value => "next",
    #            );

}else{  #start guessing

   #my $qid = $session->param('stimuli')->[$session->param('current_guess')];
   my $evidence = $session->param('evidence');
   my ($topEmo) = sort { $evidence->{$b} <=> $evidence->{$a} } keys %$evidence;
   my $qid = "e==$topEmo";
   my $q = "Did you pick $topEmo?";
 
   print
    #------------------
    #print the stimuli
    #------------------
    "<br>",
    "<div id='stimulus-area' style='background-color: #aaffaa;width: 80% '>\n",
    "The question is: ", 
    "<br>",
    "<div id='stimulus' style='margin-left:20%'>",
    "<b>",
    $q,
    $cgi->hidden( -name => 'stimulus', -default => $q, -override => 1),
    $cgi->hidden( -name => 'qid', -default => $qid, -override => 1),
    $cgi->hidden( -name => 'isGuess', -default => 1, -override => 1),
    $cgi->hidden( -name => 'startTime', -default => $dt, -override => 1),
    #    $cgi->hidden( -name => CGISESSID, -default => $session->id()),
    $cgi->hidden( -name => 'cmd', -default => 'next'),
	
    "</b>",
    "</div>",
    "<br>",
    "</div>",
    ;

    print 
    #------------------
    # the submit button
    #------------------ 
    "<br/>",
    $cgi->submit(-name => "response",
	         -value => "yes",
                );
    print 
    #------------------
    # the submit button
    #------------------ 
     $cgi->submit(-name => "response",
	         -value => "no",
                );
}

print $cgi->end_form();

print $cgi->end_html;
exit(0);




#takes the cgi and session vars and returns 1/true if logged in
sub init {
    my ($cgi,$session,$dbh) = @_; # receive three args
    
    if ( $session->param("~logged-in") ) {
	return 1;  # if logged in, don't bother going further
    }
    
    my $lg_name = $cgi->param("lg_name") or return;
    my $lg_email=$cgi->param("lg_email") or return;
    my $nativeLang=$cgi->param("nativeLang") or return;
    
    # if we came this far, user did submit the login form
    # so let's try to load his/her profile into the db
    if ( my $profile = _load_profile($lg_name, $lg_email, $nativeLang,$dbh) ) {
	$session->param("~profile", $profile);
	$session->param("~logged-in", 1);
	$session->flush();
	return 1;
    }
    
    # if we came this far, the login/psswds do not match
    # the entries in the database
    $session->param("~login-error",1);;
    return;
}


sub _load_profile {
    my ($lg_name, $lg_email, $nativeLang, $dbh) = @_;
    #print "$lg_name, $lg_email, $nativeLang\n<br/>\n";
    my $result = $dbh->do("INSERT INTO users (name,email,nativeLang,logins) values (?, ?, ?, 1) ON DUPLICATE KEY UPDATE logins=logins+1;",
			  undef,
			  $lg_name,
			  $lg_email,
			  $nativeLang,
	);
    
    
    if($result) {
	return {name=> $lg_name, email=>$lg_email};
    }else{
	return undef;
    }
}

sub capitalize {
    my $string = shift;
    $string =~ s/^(\w)/uc($1)/e;
    return $string;
}

sub update_data {
    my ($cgi,$session,$dbh) = @_; 
    #when it's the first turn, load the stimuli list
    #if(defined $knowledge){
    if(not $session->param('stimuli')) {
	_load_stimuli($cgi,$session,$dbh);
	return 0;
    }
    
    #check if the user is trying to log out:
    if($cgi->param('cmd') eq "logout") {
	$session->param("~logout", 1);
	$session->flush();
	return 0;
    }
    
    #check if the user is submitting the after action review

 
    #get the data from the prevoius response
    my $response = $cgi->param('response');
    my $stimulus = $cgi->param('stimulus');
    my $qid = $cgi->param('qid');
    
    #validate the previous response:
    if(1) 
    {
	#print $stimulus, "=eq=", $session->param('stimuli')->[$session->param('current_guess')], "\n<br/>\n";
	#print "update_data(): error\n";
	#return(0);
    }    
    
    #put the results of the prevous response into the db:

    my $task = "emo20q";

    my $eval = classifyYN($response);

    my($sec,$min,$hour,$mday,$mon,$year,$wday,
       $yday,$isdst)=localtime(time);
    my $dtEnd = sprintf "%4d-%02d-%02d %02d:%02d:%02d\n",
    $year+1900,$mon+1,$mday,$hour,$min,$sec;

    my $results = $dbh->do("INSERT INTO events (username,useremail,session,matchid,task,start,end,stimuli,qid,response,eval) values (?,?,?,?,?,?,?,?,?,?,?);",
	     undef,
	     $session->param('~profile')->{'name'},
	     $session->param('~profile')->{'email'},
	     $session->id(),
	     undef,
             $task,
	     $cgi->param('startTime'),
	     $dtEnd,
	     #$session->param('stimuli')->[$session->param('current_guess')],
	     #$session->param('stimuli')->[$session->param('current_guess')],
	     $cgi->param('qid'),
	     $cgi->param('stimulus'),
	     $response,             	     
             $eval,
	     ) ;
    

    updateShortTermMemory( $qid,$eval );

    #finally update the current_guess index
    my $currGuess =    $session->param('current_guess');
    $session->param('current_guess', $currGuess+1 ); 

    my @newQList1 = @{$session->param('stimuli')};
    my $knowledge = $session->param('knowledge');
    my $evidence = $session->param('evidence');
    shift @newQList1; 

    #DEBUGGING
    #print $_, ": ", $evidence->{$_}, "<br/>\n" for sort {$evidence->{$b} <=> $evidence->{$a} } keys %$evidence;
    my @newQList = sortQuestionsByEntropy(\@newQList1,$knowledge );;

    #deal with question identity guesses:
    if($cgi->param('isGuess') and $cgi->param('response') eq 'no')
    {
       my ($emo) = $qid =~ m/^e==(.*)$/;
	#print $emo, "<br/>\n";
       delete $evidence->{$emo};
       $session->param('evidence', $evidence);
       $session->flush();
    }
    if($cgi->param('isGuess') and $cgi->param('response') eq 'yes')
    {
       $session->param('outcome','success');
       $session->flush(); 
       return;
    }

    fisher_yates_shuffle(\@newQList,$session->param('current_guess')*3);
    $session->param('stimuli',\@newQList);
    $session->flush();
    #$session->param('current_guess', 14 );
    
    #check if the user is done:
    if($session->param('current_guess') > 20  ) {
	#$session->param("~logout", 1);
	$session->param('outcome', 'failure');
	$session->flush();
	return ;
    }
}

sub _load_stimuli {
    my ($cgi,$session,$dbh) = @_; 
    #open (ST1, "lists/questions.txt");# or die  $!, "cannot open lists/questions.txt\n";
    #my @stimuli = map {chomp; $_;} grep {!/^ *$/} <ST1>;
    #close ST1;

    #fisher_yates_shuffle(\@stimuli);     #randomize array
    #my @new  = @stimuli;
    #@stimuli = @new;

    my $knowledge = retrieve "knowledge";
    my $lexicalAccess = retrieve "lexicalAccess";   
    my @stimuli1 = keys %$lexicalAccess;
    my @stimuli = sortQuestionsByEntropy(\@stimuli1,$knowledge);
    fisher_yates_shuffle(\@stimuli,4);
    my $evidence;  #evidence for each emotion
    $evidence->{$_} = 1 for keys %$knowledge;
    
    $session->param('stimuli',\@stimuli);
    $session->param('current_guess',0);
    $session->param('knowledge',$knowledge);
    $session->param('lexicalAccess',$lexicalAccess);
    $session->param('evidence',$evidence);
    $session->flush();
    #print $_, "\n<br/>\n", for @{$session->param('stimuli')};
    
}

sub fisher_yates_shuffle {  #for randomizing the stimuli
    my $array = shift;
    my $limit = @_ ? shift : @$array;
    $limit = @$array if $limit > @$array;
    my $i;
    for ($i = $limit; --$i; ) {
        my $j = int rand ($i+1);
        next if $i == $j;
        @$array[$i,$j] = @$array[$j,$i];
    }
}

sub generateTextRealization
{
  my $logicQ = shift;
  my @g = @{$session->param('lexicalAccess')->{$logicQ}};
  my $q = $g[rand(scalar(@g))];
  $q =~ s/(:?number )?\d\d? *[.)]*//;   # remove question numbers
  $q =~ s/^ *//;                        # and other junk ... 
  $q =~ s/ *$//; 
  return $q;
}

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
	    $questionEntropy->{$q} += - $p * $log;
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

sub updateShortTermMemory
{
  my $logicQ       = shift;
  my $ans          = shift;
 
  my $shortTermMemory = $session->param('shortTermMemory');
  my $evidence = $session->param('evidence');
  my $knowledge = $session->param('knowledge');

  #foreach my $emotion (keys %$knowledge) 
  foreach my $emotion (keys %{$session->param('evidence')}) 
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
  $session->param('shortTermMemory', $shortTermMemory);
  $session->param('evidence', $evidence);

}

#db info:

" 

CREATE TABLE users ( #id INT NOT NULL AUTO_INCREMENT, 
     name varchar(32), 
     email varchar(100), 
     nativelang varchar(100),
     logins INT, 
     PRIMARY KEY(email) 
);

CREATE TABLE sessions (
              id CHAR(32) NOT NULL UNIQUE,
              a_session MEDIUMTEXT NOT NULL
          );

CREATE TABLE events (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(64),
      useremail VARCHAR(100),
      session CHAR(32),
      matchid INT,
      task VARCHAR(64),
      start DATETIME,
      end DATETIME,
      stimuli TEXT,
      qid TEXT,
      response TEXT,
      eval FLOAT
);

CREATE TABLE matches (
      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(64),
      useremail VARCHAR(100),
      session CHAR(32),
      agent VARCHAR(64),
      start DATETIME,
      end DATETIME,
      emotion TEXT,
      success BOOL,
      comment TEXT
);


";

