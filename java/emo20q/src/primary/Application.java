/**
 * Class that the application is run from.
 */
package primary;

import javax.swing.*;

public class Application {

	public static void main(String args[]) {
        final MainFrame emotwentyq = new MainFrame();
		SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                emotwentyq.setVisible(true);
            }
		});
	}
	
}