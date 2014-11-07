/**
 * Primary class for handling the game
 */

package primary;

import java.awt.*;
import java.awt.event.*;

import javax.swing.*;

import primary.TwentyQ;

public class AppGUI extends JFrame implements ActionListener {

	private JPanel cardPanel, menuPanel, gamePanel, infoPanel;
	
	private JPanel logoPanel, bottomPanel, aboutPanel, buttonPanel;
	private JButton startButton, infoButton, quitButton;
	private JTextPane aboutPane;
	
	private JPanel textPanel, textSmallPanel, helpButtonPanel;
	private JButton prevButton, backButton, nextButton;
	private JTextPane helpTextPane;
	
	private JPanel chatPanel, typePanel;
	private JButton sendButton, back2Button;
	private JScrollBar chatBar;
	private JTextArea chatPane;
	private JScrollPane chatScrollPane;
	private JTextField enterField;
	
	private TwentyQ twentyQ;
	
	private Timer t;
	
	private int helpPage;
	
	private ImageIcon icon = new ImageIcon("img/emoicon.png");
	private Image iconImg = icon.getImage();
	
	public static String MENU = "menu";
	public static String GAME = "game";
	public static String INFO = "info";
	
	/**
	 * Contructor that initializes the user interface, timer, and a few variables
	 */
	public AppGUI () {
		initUI();
		t = new Timer(100, this);
		twentyQ = new TwentyQ();
		helpPage=0;
	}
	
	/**
	 * Initializes the user interface, and displays the menu frame
	 */
	public void initUI() {
		
		// Intialize the panels
		cardPanel = new JPanel(new CardLayout());
		menuPanel = new MenuPanel();
		infoPanel = new InfoPanel();
		gamePanel = new GamePanel();
		
		// Add the side panels to the main card panel, and the then panel itself
		cardPanel.add(menuPanel, MENU);
		cardPanel.add(gamePanel, GAME);
		cardPanel.add(infoPanel, INFO);
		((CardLayout) cardPanel.getLayout()).show(cardPanel, MENU);
		add(cardPanel);
		
		// Set the main options
		setTitle("Emotion Twenty Questions");
		setSize(new Dimension(640, 480));
		setResizable(false);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setLocationRelativeTo(null);
	}

	/**
	 * Called when a message is sent, updates the chat pane and sends the message for processing
	 */
	public void sendMsg (String message) {
		chatPane.setText(chatPane.getText() + "\n" + message);
		
	}
	
	/**
	 * Action event for every time the timer clicks, hard coded to every tenth of a second
	 */
	public void actionPerformed(ActionEvent e) {
		twentyQ.stepCommand(chatPane);
	}
	
	/**
	 * Inner class for the main menu
	 */
	class MenuPanel extends JPanel {
		public MenuPanel () {
			setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
			
			logoPanel = new JPanel() {
				public void paintComponent (Graphics g) {
					super.paintComponent(g);
					g.drawImage(iconImg, 0, 0, this);
				}
			};
			logoPanel.setPreferredSize(new Dimension(10,300));
			add(logoPanel);
			
			bottomPanel = new JPanel();
			bottomPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
			
			aboutPanel = new JPanel();
			aboutPane = new JTextPane();
			aboutPane.setText("Information\n" +
					"Emotion Twenty Questions");
			aboutPane.setBackground(new Color(238,238,238));
			aboutPane.setPreferredSize(new Dimension(450,100));
			aboutPane.setEditable(false);
			
			aboutPanel.setBorder(BorderFactory.createTitledBorder("Info"));
			aboutPanel.add(aboutPane);
			
			bottomPanel.add(aboutPanel);
			
			buttonPanel = new JPanel();
			buttonPanel.setLayout(new GridLayout(3,1,10,15));
			buttonPanel.setBorder(BorderFactory.createEmptyBorder(10,30,10,10));
			
			startButton = new JButton();
			startButton.setText("Play 20Q");
			startButton.addActionListener(new MenuListener());
			buttonPanel.add(startButton);
			
			infoButton = new JButton();
			infoButton.setText("Help");
			infoButton.addActionListener(new MenuListener());
			buttonPanel.add(infoButton);
			
			quitButton = new JButton();
			quitButton.setText("Quit");
			quitButton.addActionListener(new MenuListener());
			buttonPanel.add(quitButton);
			
			bottomPanel.add(buttonPanel);
			
			add(bottomPanel);
		}
	}
	
	/**
	 * Inner class for the actual game
	 */
	class GamePanel extends JPanel {
		public GamePanel () {
			
			setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
			setBorder(BorderFactory.createEmptyBorder(30,30,10,30));
			
			
			chatPanel = new JPanel();
			chatPanel.setLayout(new BorderLayout());
			chatPanel.setBackground(Color.WHITE);
			chatPanel.setAutoscrolls(true);
			chatPanel.setBorder(BorderFactory.createLoweredBevelBorder());
			
			//chatScrollPane = new JScrollPane(chatPane);
			
			chatPane = new JTextArea(10,10);
			chatPane.setText("Hello");
			chatPane.setEditable(false);
			chatPane.setPreferredSize(new Dimension(555,305));
			chatPane.setAutoscrolls(true);
			chatPane.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));

			chatBar = new JScrollBar(JScrollBar.VERTICAL,0,1,0,1);

			//chatScrollPane.add(chatPane);
			//chatPanel.add(chatScrollPane);
			//add(chatPanel);
			
			chatPanel.add(chatPane);
			add(chatPanel);
			
			typePanel = new JPanel();
			typePanel.setLayout(new FlowLayout(FlowLayout.CENTER,20,10));
			typePanel.setBorder(BorderFactory.createEmptyBorder(10,0,10,0));
			FlowLayout fl = new FlowLayout();
			
			enterField = new JTextField();
			enterField.setPreferredSize(new Dimension(390,27));
			enterField.addActionListener(new ChatListener());
			typePanel.add(enterField);
			
			sendButton = new JButton("Send");
			sendButton.addActionListener(new GameListener());
			typePanel.add(sendButton);
			
			back2Button = new JButton(" Exit ");
			back2Button.addActionListener(new GameListener());
			typePanel.add(back2Button);
			
			add(typePanel);
		}
	}
	
	/**
	 * Inner class for the information/help/about panel
	 */
	class InfoPanel extends JPanel {
		public InfoPanel () {

			setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
			
			textPanel = new JPanel();
			textSmallPanel = new JPanel();
			helpTextPane = new JTextPane();
			
			helpTextPane.setEditable(false);
			helpTextPane.setPreferredSize(new Dimension(550,330));
			helpTextPane.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
			helpTextPane.setFont(new Font("Sans Serif", Font.PLAIN, 16));
			helpTextPane.setText("Welcome to Emotion Twenty Questions.");
			
			textSmallPanel.setBorder(BorderFactory.createLoweredBevelBorder());
			textSmallPanel.setBackground(Color.WHITE);
			textSmallPanel.add(helpTextPane);
			
			textPanel.setBorder(BorderFactory.createEmptyBorder(20,20,20,20));
			textPanel.add(textSmallPanel);
			add(textPanel);
			
			helpButtonPanel = new JPanel();

			prevButton = new JButton();
			prevButton.setText("<   Previous Page");
			prevButton.setPreferredSize(new Dimension(150,25));
			prevButton.setEnabled(false);
			prevButton.addActionListener(new HelpListener());
			helpButtonPanel.add(prevButton);
			
			backButton = new JButton();
			backButton.setText("Return to Menu");
			backButton.setPreferredSize(new Dimension(150,25));
			backButton.addActionListener(new HelpListener());
			helpButtonPanel.add(backButton);
			
			nextButton = new JButton();
			nextButton.setText("Next Page   >");
			nextButton.setPreferredSize(new Dimension(150,25));
			nextButton.addActionListener(new HelpListener());
			helpButtonPanel.add(nextButton);
			
			helpButtonPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 50, 10));
			helpButtonPanel.setBorder(BorderFactory.createEmptyBorder(15,10,15,10));
			add(helpButtonPanel);
		}
	}
	
	/**
	 * ActionListener that handles the buttons of the main menu
	 */
	class MenuListener implements ActionListener {

		public void actionPerformed(ActionEvent e) {
			if (e.getSource()==startButton) {
				((CardLayout) cardPanel.getLayout()).show(cardPanel, GAME);
				t.start();
				repaint();
			} else if (e.getSource()==infoButton) {
				((CardLayout) cardPanel.getLayout()).show(cardPanel, INFO);
				repaint();
			} else if (e.getSource()==quitButton) {
				System.exit(0);
			}
		}
	}
	
	/**
	 * ActionListener that handels the buttons of the game
	 */
	class GameListener implements ActionListener {

		public void actionPerformed(ActionEvent e) {
			if (e.getSource()==sendButton) {
				sendMsg(enterField.getText());
				enterField.setText("");
			} else if (e.getSource()==back2Button) {
				((CardLayout) cardPanel.getLayout()).show(cardPanel, MENU);
			}
		}
	}
	
	/**
	 * ActionListener that handles the buttons of the help menu
	 */
	class HelpListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			if (e.getSource()==nextButton) {
				helpPage++;
			} else if (e.getSource()==prevButton) {
				helpPage--;
			} else if (e.getSource()==backButton) {
				helpPage=-1;
				((CardLayout) cardPanel.getLayout()).show(cardPanel, MENU);
			}
			
			if (helpPage==0) {
				prevButton.setEnabled(false);
			} else {
				prevButton.setEnabled(true);
			}
			
			if (helpPage==4) {
				nextButton.setEnabled(false);
			} else {
				nextButton.setEnabled(true);
			}
			
			switch (helpPage) {
			case 0:
				helpTextPane.setText("Welcome to Emotion Twenty Questions.");
				break;
			case 1:
				helpTextPane.setText("Page 1\n\n");
				break;
			case 2:
				helpTextPane.setText("Page 2\n\n");
				break;
			case 3:
				helpTextPane.setText("Page 3\n\n");
				break;
			case 4:
				helpTextPane.setText("Page 4\n\n");
				break;
			}
		}
	}
	
	/**
	 * Action Listener that handles text input
	 */
	class ChatListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			sendMsg(enterField.getText());
			enterField.setText("");
		}
	}
}
