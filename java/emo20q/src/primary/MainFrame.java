package primary;

import java.awt.*;
import java.awt.event.*;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Formatter;

import javax.swing.*;

public class MainFrame extends JFrame implements ActionListener {

	private JMenuBar menuBar;
	private JMenu fileMenu;
	private JMenuItem closeItem, startNewItem, saveItem;
	
	private JPanel mainPanel;
	private JScrollPane scrollPane;
	JTextArea textArea = new JTextArea();
	private JTextField textField;
	private JButton sendButton;
	
	private Agent agent = new Agent(textArea);
	
	private Timer t;
	
	public MainFrame() {
		
		initUI();
		t = new Timer(50, this);
		t.start();
	}
	
	public void initUI() {
		menuBar = new JMenuBar();
		
		fileMenu = new JMenu("File");
		menuBar.add(fileMenu);
		
		startNewItem = new JMenuItem("New 20Q", KeyEvent.VK_N);
		startNewItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				startNewGame();
			}
		});
		fileMenu.add(startNewItem);
		
		saveItem = new JMenuItem("Save to Text", KeyEvent.VK_S);
		saveItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				saveToText();
			}
		});
		fileMenu.add(saveItem);
		
		closeItem = new JMenuItem("Exit", KeyEvent.VK_X);
		closeItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		fileMenu.add(closeItem);
		
		mainPanel = new JPanel();
		mainPanel.setLayout(new BoxLayout(mainPanel, BoxLayout.Y_AXIS));
		mainPanel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10));
		add(mainPanel);

		    //textArea = new JTextArea();
		textArea.setEditable(false);
		scrollPane = new JScrollPane(textArea);
		scrollPane.setPreferredSize(new Dimension(600, 350));
		mainPanel.add(new JPanel() {
			{
				add(scrollPane);
			}
		});
		
		textField = new JTextField();
		textField.setPreferredSize(new Dimension(493,30));
		textField.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				sendMsg();
			}
		});
		sendButton = new JButton();
		sendButton.setText("Send");
		sendButton.setPreferredSize(new Dimension(100,30));
		sendButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				sendMsg();
			}
		});
		mainPanel.add(new JPanel() {
			{
				add(textField);
				add(sendButton);
			}
		});
		
		setJMenuBar(menuBar);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setTitle("Emotion Twenty Questions");
		setSize(new Dimension(640, 480));
		setLocationRelativeTo(null);
		setResizable(false);
	}
	
	public void sendMsg() {
		if (!textField.getText().matches("")) {
			textArea.append("<User> " + textField.getText() + "\n");
			agent.getMsg(textField.getText());
		        textArea.selectAll();
			textField.setText(null);
		}
	}

	public void startNewGame() {
		textArea.setText(null);
		textField.setText(null);
	}
	
	public void saveToText() {
		try {
			FileWriter fileOut = new FileWriter("print.txt");
			PrintWriter scoreOut = new PrintWriter(fileOut);
			scoreOut.append(textArea.getText());
			scoreOut.close();
			fileOut.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	// Timer action preformed for real time answers
	public void actionPerformed(ActionEvent e) {
		agent.stepCommand();
	}
}
