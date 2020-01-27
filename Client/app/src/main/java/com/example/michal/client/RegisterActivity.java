package com.example.michal.client;

import android.content.Intent;
import android.os.Looper;
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

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONObject;

import java.util.HashMap;

public class RegisterActivity extends AppCompatActivity{

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
         final String mail = mailEdit.getText().toString();
         String passwordConfirm = passEditConfirm.getText().toString();

         if (!password.equals(passwordConfirm))
        {
            this.show_popup(view, "Hasła nie są identyczne!");
            return;
        }
        register(username, password, mail);
    }

    public void register(String username,
                         String password,
                         String mail)
    {
        //todo this is register more like
        String url = "http://192.168.0.14:8000/add_user";
        HashMap<String,String> params = new HashMap<String,String>();
        params.put("name", username);
        params.put("password", password);
        params.put("email", mail);

        JsonObjectRequest postRequest = new JsonObjectRequest
                (
                    Request.Method.POST,
                    url,
                    new JSONObject(params),
                    new Response.Listener<JSONObject>()
                    {
                        @Override
                        public void onResponse(JSONObject response) {
                            // response
                        }
                    },
                    new Response.ErrorListener()
                    {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            // error
                        }
                    }
                )
        {
            @Override
            protected Response<JSONObject> parseNetworkResponse(NetworkResponse response)
            {
                final int mStatusCode = response.statusCode;
                System.out.println("response is " + mStatusCode);
                runOnUiThread(new Runnable(){
                    public void run(){
                        parse_response(mStatusCode);
                    }
                });
                return super.parseNetworkResponse(response);
            }
        };

        Connection.getInstance(this).addToRequestQueue(postRequest);
    }

    private void parse_response(int res)
    {
        if(res == 200)
        {
            this.show_popup(this.findViewById(android.R.id.content)
                    , "Zarejestrowano!");
        }
        else //todo
        {
            this.show_popup(this.findViewById(android.R.id.content)
                    , "Nazwa użytkownika zajęta!");
        }
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

        TextView txt = popupView.findViewById(R.id.PopupPass);
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

}
