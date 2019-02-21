package com.example.michal.client;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.PopupWindow;

public class RegisterActivity extends AppCompatActivity {

    PopupWindow popUp;
    EditText usernameEdit;
    EditText passEdit;
    EditText passEditConfirm;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        popUp = new PopupWindow(this);
        usernameEdit = findViewById(R.id.RegisterUsernameEdit);
        passEdit = findViewById(R.id.RegisterPasswordEdit);
        passEditConfirm = findViewById(R.id.PasswordConfirmEdit);
    }

    public void RegisterRequest(View view){
         String username = usernameEdit.getText().toString();
         String password = passEdit.getText().toString();
         String passwordConfirm = passEditConfirm.getText().toString();

         if (password.equals(passwordConfirm))
        {
            this.show_popup(view);
            return;
        }

    }

    private void show_popup(View view)
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

        // dismiss the popup window when touched
        popupView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                popupWindow.dismiss();
                return true;
            }
        });
    }
}
