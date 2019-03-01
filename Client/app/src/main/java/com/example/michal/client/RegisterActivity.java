package com.example.michal.client;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;

public class RegisterActivity extends AppCompatActivity implements Runnable {

    PopupWindow popUp;
    EditText usernameEdit;
    EditText passEdit;
    EditText passEditConfirm;
    EditText mailEdit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        popUp = new PopupWindow(this);
        usernameEdit = findViewById(R.id.RegisterUsernameEdit);
        passEdit = findViewById(R.id.RegisterPasswordEdit);
        passEditConfirm = findViewById(R.id.PasswordConfirmEdit);
        mailEdit = findViewById(R.id.EmailEdir);

    }

    public void RegisterRequest(View view){
         final String username = usernameEdit.getText().toString();
         final String password = passEdit.getText().toString();
         String passwordConfirm = passEditConfirm.getText().toString();

         if (!password.equals(passwordConfirm))
        {
            this.show_popup(view,"Passwords do not match!");
            return;
        }

        RegisterActivity t1 = this; //waiting thread
        (new Thread(t1)).start();
        register(username, password);
        try {
            Thread.sleep(1500);     //TODO delet this sleep later (or sooner if needed)
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        //login("Magnus", "DidNothingWrong"); TODO we can login

       // Connection.getInstance().accessOutput(Message.endMessage(), false);

      //  usernameEdit.setText("Failed to register");

        //String res = conn.register(username, password);
        //mailEdit.setText(res);

    }

    public void register(String username,
                         String password)
    {
        Message msg = new Message(CmdType.REGISTER,username, password);
        Connection.getInstance().accessOutput(msg, false);
        System.out.println("register now");
    }

    private void show_popup(View view,
                            String text)
    {
        LayoutInflater inflater = (LayoutInflater)
                getSystemService(LAYOUT_INFLATER_SERVICE);
        View popupView = inflater.inflate(R.layout.popup_window, null);

        // create the popup window
        int width = LinearLayout.LayoutParams.WRAP_CONTENT;
        int height = LinearLayout.LayoutParams.WRAP_CONTENT;
        boolean focusable = true; // lets taps outside the popup also dismiss it
        final PopupWindow popupWindow = new PopupWindow(popupView, width, height, focusable);

        // show the popup window
        // which view you pass in doesn't matter, it is only used for the window tolken
        popupWindow.showAtLocation(view, Gravity.CENTER, 0, 0);

        TextView txt = findViewById(R.id.PopupPass);
        txt.setText(text);

        // dismiss the popup window when touched
        popupView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                popupWindow.dismiss();
                return true;
            }
        });
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
          /*      if (inp.contains("T"));
                    this.show_popup(getWindow().getDecorView().findViewById(android.R.id.content)
                            ,"Passwords do not match!");
                if (inp.contains("F"));
                    this.show_popup(getWindow().getDecorView().findViewById(android.R.id.content)
                            ,"Passwords do not match!");*/

                conn.accessIntput(null, false);
                break;
            }
        }

    }
}
