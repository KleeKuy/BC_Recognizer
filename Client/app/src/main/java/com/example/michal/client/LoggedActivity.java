package com.example.michal.client;

import android.content.Intent;
import android.graphics.Bitmap;
import android.icu.text.SimpleDateFormat;
import android.net.Uri;
import android.os.Environment;
import android.os.health.SystemHealthManager;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;

import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class LoggedActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private RecordAdapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;
    private EditText searchText;
    private String password;
    private String username;

    static final int REQUEST_TAKE_PHOTO = 1;
    String currentPhotoPath;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged);

        Intent intent = getIntent();
        username = intent.getStringExtra(MainActivity.USERNAME);
        password = intent.getStringExtra(MainActivity.PASSWORD);

        recyclerView = (RecyclerView) findViewById(R.id.MainList);

        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);
        mAdapter = new RecordAdapter();
        recyclerView.setAdapter(mAdapter);

        searchText = (EditText) findViewById(R.id.searchText);

        searchText.addTextChangedListener(new TextWatcher() {

            public void afterTextChanged(Editable s) {

            }

            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            public void onTextChanged(CharSequence s, int start, int before, int count) {
                System.out.print("onTextCanged");
                System.out.print(s.toString());
                mAdapter.filter(s.toString());
            }
        });

        getData();

    }

    private void parse_reposnse(JSONObject res)
    {
        int len = res.length();
        String[] myDataset = new String[len];
        Iterator<String> keys = res.keys();
        int i = 0;
        while(keys.hasNext())
        {
            String key = keys.next();
            myDataset[i] = key;
            i++;
        }
        System.out.print(myDataset[0]);
    }

    public void logout(View view) { finish(); }

    public void reload(View view) { getData(); }

    private void getData()
    {
        String url = "http://192.168.0.14:8000/get_data";

        JsonObjectRequest postRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>()
                {
                    @Override
                    public void onResponse(JSONObject response) {
                        parse_db(response);
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
            public Map<String, String> getHeaders()
            {
                HashMap<String, String> params = new HashMap<String, String>();
                String creds = String.format("%s:%s",username,password);
                params.put("Authorization", creds);
                return params;
            }
        };

        Connection.getInstance(this).addToRequestQueue(postRequest);
    }

    private void parse_db(JSONObject res)
    {
        System.out.println(res);
        System.out.println(res.keys());
        ArrayList<JSONObject> records = new ArrayList<>();
        Iterator<String> keys = res.keys();
        System.out.println(res);
        System.out.println(res.length());
        for (int i = 0; i < res.length(); i++) {
            String name = keys.next();
            try {
                JSONObject record = new JSONObject();
                record.put(name, res.get(name));
                records.add(record);
            } catch (org.json.JSONException e) {
                System.out.println(e);
            }
        }
        System.out.println(records);
        mAdapter.setData(records);
        mAdapter.notifyDataSetChanged();
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        System.out.println("to dispacz");
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
            System.out.println("activity started");
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_TAKE_PHOTO && resultCode == RESULT_OK) {
            Bundle extras = data.getExtras();
            Bitmap imageBitmap = (Bitmap) extras.get("data");
            System.out.println("activity result");
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
            byte[] byteArray = stream.toByteArray();
            post_image(byteArray);
        }
    }


    public static String convertStreamToString(InputStream is) throws IOException {
        // http://www.java2s.com/Code/Java/File-Input-Output/ConvertInputStreamtoString.htm
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();
        String line = null;
        Boolean firstLine = true;
        while ((line = reader.readLine()) != null) {
            if(firstLine){
                sb.append(line);
                firstLine = false;
            } else {
                sb.append("/n").append(line);
            }
        }
        reader.close();
        return sb.toString();
    }

    public static String getStringFromFile (String filePath) throws IOException {
        File fl = new File(filePath);
        FileInputStream fin = new FileInputStream(fl);
        String ret = convertStreamToString(fin);
        //Make sure you close all streams.
        fin.close();
        return ret;
    }

    byte[] fullyReadFileToBytes(File f) throws IOException {
        int size = (int) f.length();
        byte bytes[] = new byte[size];
        byte tmpBuff[] = new byte[size];
        FileInputStream fis= new FileInputStream(f);;
        try {

            int read = fis.read(bytes, 0, size);
            if (read < size) {
                int remain = size - read;
                while (remain > 0) {
                    read = fis.read(tmpBuff, 0, remain);
                    System.arraycopy(tmpBuff, 0, bytes, size - remain, read);
                    remain -= read;
                }
            }
        }  catch (IOException e){
            throw e;
        } finally {
            fis.close();
        }

        return bytes;
    }

    private void post_image(final byte[] image)
    {
        String url = "http://192.168.0.14:8000/handle_image ";

        System.out.println("post image");


       /* System.out.println("we got file");

        String url = "http://192.168.0.16:8000/add";
       // byte[] encoded = Files.readAllBytes(currentPhotoPath);      //sdk api 26!
        FileInputStream fin;
        String strFile;
        try{
            System.out.println("getting stream");
            fin = new FileInputStream(file);
        } catch (FileNotFoundException e){
            System.out.println("File not found");
            return;
        }
        try{
            System.out.println("getting string from " + currentPhotoPath);
            strFile = getStringFromFile(currentPhotoPath);
        } catch (java.io.IOException e){
            System.out.println("exception in getting string from fin " + e.getMessage());
            return;
        }
        System.out.println("we got stringed file");

        HashMap<String,String> params = new HashMap<String,String>();
        params.put("file", strFile);*/

        JsonObjectRequest postRequest = new JsonObjectRequest(Request.Method.POST, url, null,
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
                        System.out.println("error monkaS");
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
                    }
                });
                return super.parseNetworkResponse(response);
            }
            @Override
            public byte[] getBody(){
                return image;
            }

            };

        Connection.getInstance(this).addToRequestQueue(postRequest);
    }

    public void add_image(View view)    //todo delete those file
    {
        dispatchTakePictureIntent();
    }


    private File createImageFile() throws IOException {
        // Create an image file name
  //      String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "BCR_FILE";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

}
