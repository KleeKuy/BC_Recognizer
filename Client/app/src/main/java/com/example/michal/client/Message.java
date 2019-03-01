package com.example.michal.client;
import java.io.File;

public class Message {
    private File f;
    private CmdType cmd;
    private String msg;


    public Message(File file,
                   CmdType command,
                   String message)
    {
        f = file;
        cmd = command;
        msg = message;
    }

    public Message(CmdType command,
                   String username,
                   String password)
    {
        cmd = command;
        msg = "NAME:" + username + "/PASSWORD:" + password;
    }

    public static Message endMessage()
    {
        Message msg = new Message(CmdType.END, null, null);
        return msg;
    }

    public final CmdType getCommand()
    {
        return cmd;
    }

    public final File getFile()
    {
        return f;
    }

    public final String getMessage() {
        return msg;
    }
}
