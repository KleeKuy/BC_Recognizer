package com.example.michal.client;

public enum CmdType {
    VERIFY((String)"VER"),
    ADD_USER((String)"ADU"),
    ADD_RECORD((String)"ADR"),
    REGISTER((String)"REG"),
    LOGIN((String)"LOG"),
    END((String)"END");

    private final String value;

    CmdType(String val)
    {
        value = val;
    }

    public String getVal() {
        return value;
    }

}


