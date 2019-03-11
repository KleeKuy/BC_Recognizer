package com.example.michal.client;

import android.content.Intent;
import android.icu.text.SimpleDateFormat;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;

import org.apache.commons.io.IOUtils;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class LoggedActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private RecordAdapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;
    private String password;
    private String username;
    private JSONObject dataBase;

    static final int REQUEST_TAKE_PHOTO = 1;
    String currentPhotoPath;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged);

        Intent intent = getIntent();
        username = intent.getStringExtra(MainActivity.USERNAME);
        password = intent.getStringExtra(MainActivity.PASSWORD);
        String[] myDataset = {" "};

        recyclerView = (RecyclerView) findViewById(R.id.MainList);

        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        recyclerView.setHasFixedSize(true);

        // use a linear layout manager
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);
        mAdapter = new RecordAdapter(myDataset);
        recyclerView.setAdapter(mAdapter);

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

    public void upload(View view) { post_image(); }

    private void getData()
    {
        String url = "http://192.168.0.16:8000/download";

        JsonObjectRequest postRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>()
                {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("we built this json objecton rock and roll");
                        parse_db(response);
                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.out.println("error monkaS");
                        System.out.println(error.getMessage());
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
        };

        Connection.getInstance(this).addToRequestQueue(postRequest);
    }

    private void parse_db(JSONObject res)
    {
        int len = res.length();
        String[] myDataset = new String[len];
        Iterator<String> keys = res.keys();
        int i = 0;
        while(keys.hasNext())
        {
            String key = keys.next();
            String val = " ";
            try{
                val = res.getString(key);
            } catch (org.json.JSONException e){
                System.out.println(e.getMessage());
            }
            myDataset[i] = key + "/n" + val;
            i++;
        }
        mAdapter.updateDataSet(myDataset);
        mAdapter.notifyDataSetChanged();
        dataBase = res;
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // Ensure that there's a camera activity to handle the intent
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            // Create the File where the photo should go
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                System.out.println(ex.getMessage());
            }
            // Continue only if the File was successfully created
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(this,
                        "com.example.android.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
            }
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
                sb.append("\n").append(line);
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

    private void post_image()
    {
        String url = "http://192.168.0.16:8000/add";

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
                File file = new File(currentPhotoPath);
                try {
                   return fullyReadFileToBytes(file);
                } catch (IOException e)
                {
                    System.out.println(e.getMessage());
                    return null;
                }
            }

            };

        Connection.getInstance(this).addToRequestQueue(postRequest);
    }

    public void add_image(View view)    //todo delete those file
    {
        dispatchTakePictureIntent();
        Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
        System.out.println(currentPhotoPath);
        File f = new File(currentPhotoPath);
        Uri contentUri = Uri.fromFile(f);
        mediaScanIntent.setData(contentUri);
        this.sendBroadcast(mediaScanIntent);

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
