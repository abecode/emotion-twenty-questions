package primary;

import java.awt.Dimension;

import javax.swing.*;

public class GetStringFrame extends JFrame {
	public GetStringFrame () {
		add(new JPanel() {
			{
				add(new JButton("OK"));
			}
		});
		
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setTitle("Options");
		setSize(new Dimension(300, 100));
		setLocationRelativeTo(null);
		setResizable(false);
	}
}
