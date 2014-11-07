/**
 * Class that handles the top level game logic.
 */

package primary;

import javax.swing.*;
import java.util.*;
import java.util.Timer;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.regex.*;


//maps propositions to truth values
class EmotionModel extends HashMap<String,Boolean>
{
    HashMap<String,Boolean> truthTable;
    static Boolean answerIsYes(String answer)
    {
	Pattern p = Pattern.compile("^[Yy]es.*"); //note this is oversimplified
	Matcher m = p.matcher(answer);
	Boolean b = m.matches();
	return b;
    }
    static Boolean answerIsNo(String answer)
    {
	Pattern p = Pattern.compile("^[Nn]o.*"); //note this is oversimplified
	Matcher m = p.matcher(answer);
	Boolean b = m.matches();
	return b;
    }

}

//maps emotions to their models
class Knowledge extends HashMap<String,EmotionModel>
{
    Knowledge(){
    	try {
	    BufferedReader readbuffer = new BufferedReader(new FileReader("src/primary/data/humanHumanResults_2011-10-31.txt"));
	    String strRead;

		System.out.println("Human-human data read");
	    while ((strRead=readbuffer.readLine())!=null){
		String splitarray[] = strRead.split("\t");
		String emotion = splitarray[0];
		String qgloss = splitarray[1];
		String answer = splitarray[2];
		//System.out.println(emotion + " " + qgloss + " " + answer);
		//check if emotion is recorded
		if(this.containsKey(emotion)){
		    EmotionModel m = this.get(emotion);
		    if(m.answerIsYes(answer)) {
			m.put(qgloss, true);
		    }
		    if(m.answerIsNo(answer)) {
			m.put(qgloss, false);
		    }
		}else{
		    EmotionModel m = new EmotionModel();
		    if(m.answerIsYes(answer)) {
			m.put(qgloss, true);
		    }
		    if(m.answerIsNo(answer)) {
			m.put(qgloss, false);
		    }
		    this.put(emotion,m);
		}
		
	    } 
	    readbuffer.close();
	}
	catch(java.io.FileNotFoundException e)
	    {
		System.out.println("Error: "+e.getMessage());
	    }
	catch(java.io.IOException e)
	    {
		System.out.println("Error: "+e.getMessage());
	    }
	
    }	

}

//maps semantic meaning to text forms
//like a phrase table
class LexicalAccess extends HashMap<String,HashSet<String> >
{
    LexicalAccess(){
	try {
	    BufferedReader readbuffer = new BufferedReader(new FileReader("src/primary/data/lexicalAccess_2011-10-31.txt"));
	    String strRead;

		System.out.println("Lexical data read");
	    while ((strRead=readbuffer.readLine())!=null){
		String splitarray[] = strRead.split("\t");
		String question = splitarray[0];
		String qgloss = splitarray[1];
		//System.out.println(question + " " + qgloss);
		//check if emotion is recorded
		if(this.containsKey(qgloss)){
		    HashSet<String> set = this.get(qgloss);
		    set.add(qgloss);
		}else{
		    HashSet<String> set = new HashSet<String>();
		    set.add(qgloss);
		    this.put(qgloss,set);
		}
		
	    } 
	    readbuffer.close();
	}
	catch(java.io.FileNotFoundException e)
	    {
		System.out.println("Error: "+e.getMessage());
	    }
	catch(java.io.IOException e)
	    {
		System.out.println("Error: "+e.getMessage());
	    }
	
    }	

}


public class Agent {

	AgentState state;
	
	enum AgentState {INITIAL, PRE_20Q, WAIT, RESPOND};
	
    Knowledge knowledge;
    LexicalAccess lexicalAccess;
    JTextArea textArea;
         /**
	 * Constructor
	 */
    Agent(JTextArea ta)
    {
        state = AgentState.INITIAL;
        	 
        //read data from human-human matches
        knowledge = new Knowledge();
        //read data from human-computer matches
        //read semantic to text mappings
	    lexicalAccess = new LexicalAccess();
	    textArea = ta;
	 }
	/**
	 * Receives a message from the player and processes it
	 */
	public void getMsg (String message) {
		// Process Message
	   if (state == AgentState.PRE_20Q) {
		   if (message.toLowerCase().contains("yes")) {
			   state = AgentState.RESPOND;
		   } else {
			   sendMsg("I don't understand.");
		   }
		   return;
	   }
	   
	   if (state == AgentState.WAIT) {
		   state = AgentState.RESPOND;
	   }
	}
	
	/**
	 * Sends a message to the player
	 */
	public void sendMsg (String message) {
		textArea.append("<20Q>: "+ message + "\n");
	}
	
	/**
	 * Command taken every step of the timer
	 */
	public void stepCommand () {
		
		if (state == AgentState.INITIAL) {
			sendMsg("Welcome to Emotion Twenty Questions.  Are you ready to begin?");
			state = AgentState.PRE_20Q;
		}
		
		if (state == AgentState.RESPOND) {
			sendMsg("Question");
			state = AgentState.WAIT;
		}
	}
}
