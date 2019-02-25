package com.example.michal.client;
import java.io.FileOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.io.PrintWriter;
import java.io.StringWriter;



public class Connection {

    final int PORT = 50000;
    final String IP = "100.91.125.121";
    private Socket clientSocket;
   // private PrintWriter out;
   // private BufferedReader inHost;
    private	OutputStream outs;
    private InputStream ins;

    public String setupConnection(String username, String password)
    {
        String io = "git";
        String ex = "git";

        try
        {
            clientSocket = new Socket(IP, PORT);
            outs = clientSocket.getOutputStream();
            ins = clientSocket.getInputStream();
        } catch (java.io.IOException e) {
            io = e.getMessage();
        }
          catch (Exception e)
        {
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
            String sStackTrace = sw.toString(); // stack trace as a string
            ex = sStackTrace;
        }

        if (outs == null){
            return "outs is null monkaS";
        }

        //return io + ex;

        return register(username, password);
    }

    public final String register(String username,
                                  String password)
    {
        byte[] cmd = "ADU".getBytes(StandardCharsets.UTF_8); //TODO
        byte[] msg = ("NAME:" + username + "/PASSWORD:" + password).getBytes(StandardCharsets.UTF_8);

        try {
            outs.write(cmd);
            outs.write(msg);
        } catch (java.io.IOException e)
        {
            return e.getMessage();
        }  catch (Exception e){
            return "sending err " + e.getMessage();
        }

        byte[] res = new byte[5];
        int count = 0;
        while (count == 0) {
            try {
                count = ins.read(res);
            } catch (java.io.IOException e){
                return e.getMessage();
            }
        }

        String response = new String(res);
        login(username, password);
        return response;
    }

    public final void login(String username,
                            String password)
    {
        byte[] cmd = "VER".getBytes(StandardCharsets.UTF_8); //TODO
        byte[] msg = ("NAME:" + username + "/PASSWORD:" + password).getBytes(StandardCharsets.UTF_8);

        try {
            outs.write(cmd);
            outs.write(msg);
        } catch (java.io.IOException e)
        {
            //todo return e.getMessage();
        }  catch (Exception e){
            //todo return "sending err " + e.getMessage();
        }

        byte[] res = new byte[5];
        int count = 0;
        while (count == 0) {
            try {
                count = ins.read(res);
            } catch (java.io.IOException e){
                //todo return e.getMessage();
            }
        }

    }

}
