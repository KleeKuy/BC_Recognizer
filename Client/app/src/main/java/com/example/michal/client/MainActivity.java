package com.example.michal.client;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Base64;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.io.StringWriter;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class MainActivity extends AppCompatActivity { //todo redundand code

    private EditText loginEdit;
    private EditText passwordEdit;
    public static final String USERNAME = "MainActivity.USERNAME";
    public static final String PASSWORD = "MainActivity.PASSWORD";
    public static final String DATA = "MainActivity.DATA";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

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
       // MainActivity t1 = this; //waiting thread
       // (new Thread(t1)).start();
        final String username = loginEdit.getText().toString();
        final String password = passwordEdit.getText().toString();
        login(username,password);

    }

    private void login(final String username,
                       final String password)
    {
        //todo this is register more like
        String url = "http://192.168.0.14:8000/login";


        JsonObjectRequest postRequest = new JsonObjectRequest(Request.Method.GET, url, null,
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
                        System.out.println(error);
                    }
                }
        ) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError
            {
                HashMap<String, String> params = new HashMap<String, String>();
                String creds = String.format("%s:%s",username,password);
                params.put("Authorization", creds);
                return params;
        }
            @Override
            protected Response<JSONObject> parseNetworkResponse(NetworkResponse response)
            {
                final int mStatusCode = response.statusCode;
                runOnUiThread(new Runnable(){
                    public void run(){
                        System.out.println("reponse from post");
                        parse_response(mStatusCode, username, password);
                    }
                });
                return super.parseNetworkResponse(response);
            }
        };

        Connection.getInstance(this).addToRequestQueue(postRequest);


    }

    private void parse_response(int res,
                                String username,
                                String password)    //todo more redundant code
    {
        System.out.println("response is " + res);
        if(res == 200)
        {
            System.out.println("we shall head to the get, POG");
            Intent intent = new Intent(this, LoggedActivity.class);
            intent.putExtra(USERNAME, username);
            intent.putExtra(PASSWORD, password);
            startActivityForResult(intent, -1);

        }
        else
        {
            this.show_popup(this.findViewById(android.R.id.content),
                            "Niepoprawna nazwa użytkownika lub hasło");
        }
    }

    private void show_popup(View view,          //todo redundant code <:(
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

    public void get(String username,
                    String password)
    {
        // login(username, password);

// Instantiate the RequestQueue.
        String url ="http://10.0.2.2:8000/user";

// Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        loginEdit.setText("Response is: "+ response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                loginEdit.setText("That didn't work!");
            }
        });

// Add the request to the RequestQueue.
        Connection.getInstance(this).addToRequestQueue(stringRequest);
    }
}
