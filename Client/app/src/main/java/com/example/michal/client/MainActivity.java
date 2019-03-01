package com.example.michal.client;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class MainActivity extends AppCompatActivity implements Runnable { //todo redundand code

    private EditText loginEdit;
    private EditText passwordEdit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
        loginEdit = findViewById(R.id.LoginUsernameEdit);
        passwordEdit = findViewById(R.id.LoginPasswordEdit);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void register(View view)
    {
        Intent intent = new Intent(this, RegisterActivity.class);
       // EditText editText = (EditText) findViewById(R.id.editText);
       // String message = editText.getText().toString();
       // intent.putExtra(EXTRA_MESSAGE, message);
        startActivity(intent);
    }

    public void loginButton(View view)
    {
        MainActivity t1 = this; //waiting thread
        (new Thread(t1)).start();
        final String username = loginEdit.getText().toString();
        final String password = passwordEdit.getText().toString();

        login(username, password);
    }

    public void login(String username,
                      String password)
    {
        Message msg = new Message(CmdType.VERIFY,username, password);
        Connection.getInstance().accessOutput(msg, false);
        System.out.println("login now ");
    }

    public void run() {
        Connection conn = Connection.getInstance();
        while(true)
        {
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            String inp = conn.accessIntput(null, true);
            if (inp != null)
            {
                System.out.println(inp);
                if (inp.contains("T")) {
                    Intent intent = new Intent(this, LoggedActivity.class);
                    startActivity(intent);
                }
                if (inp.contains("F"))
                    loginEdit.setText("Niewłaściwe dane logowania"); //todo it breaks app
                conn.accessIntput(null, false);
                break;
            }
        }

    }
}
