package com.example.testsuite;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.slider.LabelFormatter;
import com.google.android.material.slider.Slider;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;
import org.eclipse.paho.client.mqttv3.MqttException;

public class SecondActivity extends AppCompatActivity {
    Button btn0;
    Switch btnLight;
    MQTTHelper mqttHelper;
    Button mode1Button;
    Button mode2Button;
    Button mode3Button;
    Button[] modeButtons;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_two);
        btn0 = (Button) findViewById(R.id.btn0);
        btn0.setOnClickListener(e -> {
            Intent intent = new Intent(this, FirstActivity.class);
            startActivity(intent);
        });

        btnLight = (Switch) findViewById(R.id.btn_light);

        mode1Button = findViewById(R.id.mode1);
        mode2Button = findViewById(R.id.mode2);
        mode3Button = findViewById(R.id.mode3);
        modeButtons = new Button[]{mode1Button, mode2Button, mode3Button};
        for (Button modeButton : modeButtons) {
            modeButton.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    handleModeSelection((Button) v);

                }
            });
        }
        btnLight.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    //btnLight.setImageResource(R.mipmap.bulb_on);
                    sendDataMQTT("Junnn123/feeds/start-button", "1");
                } else {
                    //btnLight.setImageResource(R.mipmap.bulb_off);
                    sendDataMQTT("Junnn123/feeds/start-button", "0");
                }
            }
        });

        startMQTT();
    }
    private void handleModeSelection(Button selectedButton) {
        // Assuming modeButtons are in the order of mode1, mode2, mode3 in the array
        for (int i = 0; i < modeButtons.length; i++) {
            if (modeButtons[i] == selectedButton) {
                // Disable the selected button to indicate it's active
                modeButtons[i].setEnabled(false);
                modeButtons[i].setBackgroundColor(getResources().getColor(R.color.selectedColor));

                // Sending the number (i + 1) as a string
                sendDataMQTT("Junnn123/feeds/mode", String.valueOf(i + 1));
            } else {
                // Enable all other buttons
                modeButtons[i].setEnabled(true);
                modeButtons[i].setBackgroundColor(getResources().getColor(R.color.deselectedColor));
            }
        }
    }

    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);
        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic,msg);
        }catch (MqttException e){
            e.printStackTrace();
        }
    }

    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("Test",topic+ "***"+ message.toString());
                if (topic.endsWith("start-button")) {
                    btnLight.setChecked(message.toString().equals("1"));
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }

        });
    }
}