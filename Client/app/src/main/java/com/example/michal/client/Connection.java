package com.example.michal.client;;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.io.PrintWriter;
import java.io.StringWriter;


public class Connection implements Runnable{

    final int PORT = 5000;
    final String IP = "10.0.2.2";
    //final String IP = "100.91.125.121";
    private Socket clientSocket;
    // private PrintWriter out;
    // private BufferedReader inHost;
    private	OutputStream outs;
    private InputStream ins;
    private Message output;
    private String input;
    private static Connection instance;

    public static Connection getInstance() //todo if socket times out we should smhow delet instance
    {
        if(instance == null)
            instance = new Connection();
        return instance;
    }

    public Connection()
    {
        (new Thread(this)).start();
    }

    private void setupConnection()
    {
        try
        {
            clientSocket = new Socket(IP, PORT);
            outs = clientSocket.getOutputStream();
            ins = clientSocket.getInputStream();
        } catch (java.io.IOException e) {
            //TODO
        }
        catch (Exception e)
        {
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
            String sStackTrace = sw.toString(); // stack trace as a string
        }
    }

    public synchronized Message accessOutput(Message new_message, boolean read) {
        if(!read)
            output = new_message;
        return output;
    }

    public synchronized String accessIntput(String new_message, boolean read) {
        if(!read)
            input = new_message;
        return input;
    }


    @Override
    public void run()
    {
        setupConnection();
        while (true) {
            try {
                Thread.sleep(300);
            } catch (InterruptedException e) {
                System.out.println("sending err " + e.getMessage());
            }
            Message out = this.accessOutput(null, true);
            if(out != null)
            {
                try {
                    System.out.println("will send cmd " + out.getCommand().getVal());
                    outs.write(out.getCommand().getVal().getBytes(StandardCharsets.UTF_8));
                    System.out.println("will send cmd " + out.getCommand().getVal());
                    outs.write(out.getMessage().getBytes(StandardCharsets.UTF_8));
                } catch (java.io.IOException e)
                {
                    System.out.println(e.getMessage());
                }  catch (Exception e){
                    System.out.println("sending err " + e.getMessage());
                }

                byte[] res = new byte[5];
                int count = 0;
                while (count == 0) {
                    try {
                        count = ins.read(res);
                    } catch (java.io.IOException e){
                        System.out.println(e.getMessage());
                        return;
                    }
                }
                this.accessOutput(null, false);
                input = new String(res, StandardCharsets.UTF_8);
            }

        }

    }

}
