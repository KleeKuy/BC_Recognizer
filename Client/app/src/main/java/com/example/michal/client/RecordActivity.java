package com.example.michal.client;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.TextView;

public class RecordActivity extends AppCompatActivity {

    private TextView emailEdit;
    private TextView phoneEdit;
    private TextView websiteEdit;
    private TextView nameView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_record);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        Intent intent = getIntent();
        String name = intent.getStringExtra("NAME");
        String email = intent.getStringExtra("EMAIL");
        String phone = intent.getStringExtra("PHONE");
        String website = intent.getStringExtra("WEBSITE");

        nameView =  findViewById(R.id.nameView);
        nameView.setText(name);

        emailEdit =  findViewById(R.id.emailEdit);
        emailEdit.setText(email);

        phoneEdit =  findViewById(R.id.phoneEdit);
        phoneEdit.setText(phone);

        websiteEdit =  findViewById(R.id.websiteEdit);
        websiteEdit.setText(website);

    }

}
