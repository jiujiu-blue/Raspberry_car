package com.hzh.remote;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class StartActivity extends AppCompatActivity {
    private String host="192.168.137.169";
    private int port=6666;

    private TextView textViewIP;
    private TextView textViewPort;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);
        //Get the last IP and port value, and show them
        getInfoFromSharedPreference();
        textViewIP=(TextView)findViewById(R.id.carIP);
        textViewPort=(TextView)findViewById(R.id.carPort);
        textViewIP.setText(host);
        textViewPort.setText(String.valueOf(port));
        Button buttonEnter=(Button)findViewById(R.id.enter);
        buttonEnter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                host=textViewIP.getText().toString();
                port=Integer.parseInt(textViewPort.getText().toString());
                Intent startMainActivityIntent=new Intent(StartActivity.this,MainActivity.class);
                startMainActivityIntent.putExtra("tcpHost",host);
                startMainActivityIntent.putExtra("tcpPort",port);
                startActivity(startMainActivityIntent);
                //Save the ip and port values
                setInfoFromSharedPreference();
                finish();
            }
        });
    }

    private void getInfoFromSharedPreference(){
        SharedPreferences preferences=getSharedPreferences("connectPara",MODE_PRIVATE);
        host=preferences.getString("IP","192.168.137.169");
        port=preferences.getInt("Port",6666);

    }

    private void setInfoFromSharedPreference(){
        SharedPreferences.Editor editor=getSharedPreferences("connectPara",MODE_PRIVATE).edit();
        editor.putString("IP",host);
        editor.putInt("Port",port);
        editor.apply();
    }
}
