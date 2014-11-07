/**
 * Class that handles the top level game logic.
 */

package primary;

import javax.swing.*;

public class TwentyQ {
	
	private Agent agent;
	
	/**
	 * Receives a message from the player and processes it
	 */
	public void getMsg (String message) {
		// Process Message
	}
	
	/**
	 * Sends a message to the player
	 */
	public void sendMsg (String message, JTextArea textArea) {
		textArea.setText(textArea.getText() + "\n" + message);
	}
	
	/**
	 * Command taken every step of the timer
	 */
	public void stepCommand (JTextArea textArea) {
		//sendMsg("Hello", textArea);
	}
}
