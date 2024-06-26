package com.example.testsuite;

import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;


import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.IntentFilter;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;
import com.github.mikephil.charting.components.YAxis;
import android.view.View;


import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.widget.Toast;

import java.nio.charset.Charset;
import org.eclipse.paho.client.mqttv3.MqttException;

public class FirstActivity extends AppCompatActivity {
    Button btn1, btn2, btn3;
    TextView txtTemp, txtHumi, txtIllu, txtDeviceStatus;
    LineChart mChartTemp, mChartHumi, mChartIllu;

    MQTTHelper mqttHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_one);

        btn1 = (Button) findViewById(R.id.btn1);
        btn1.setOnClickListener(e -> {
            Intent intent = new Intent(this, SecondActivity.class);
            startActivity(intent);
        });

        txtTemp = (TextView) findViewById(R.id.txt_temp);
        txtHumi = (TextView) findViewById(R.id.txt_humi);
        txtIllu = (TextView) findViewById(R.id.txt_illu);
        mChartTemp = findViewById(R.id.lineChartTemp);
        mChartHumi = findViewById(R.id.lineChartHumi);
        //mChartIllu = findViewById(R.id.lineChartIllu);
        txtDeviceStatus = findViewById(R.id.txtDeviceStatus);
        startMQTT();
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
                Log.d("First",topic+ "***"+ message.toString());
                if (topic.contains("temp")) {
                    txtTemp.setText("Temperature: " + message.toString() + "°C");
                    Log.d("temp",topic+ "***"+ message.toString());

                    float tempValue;
                    try {
                        tempValue = Float.parseFloat(message.toString());
                        displayChart(tempValue, mChartTemp);
                    } catch (NumberFormatException e) {
                        Log.d("MainActivity", "Failed to parse temperature: " + message.toString());
                        return;
                    }
                }
                else if (topic.contains("humid")) {
                    txtHumi.setText("Humidity: " + message.toString() + "%");
                    Log.d("humid",topic+ "***"+ message.toString());

                    float tempValue;
                    try {
                        tempValue = Float.parseFloat(message.toString());
                        displayChart(tempValue, mChartHumi);
                    } catch (NumberFormatException e) {
                        Log.d("MainActivity", "Failed to parse temperature: " + message.toString());
                        return;
                    }

                }
                else if (topic.contains("sonar")) {
                    txtIllu.setText("Illumination: " + message.toString() + "lx");
                    Log.d("light",topic+ "***"+ message.toString());

                    float tempValue;
                    try {
                        tempValue = Float.parseFloat(message.toString());
                        displayChart(tempValue, mChartIllu);
                    } catch (NumberFormatException e) {
                        Log.d("MainActivity", "Failed to parse temperature: " + message.toString());
                        return;
                    }

                }
                else if (topic.contains("current_device")) {
                    Log.d("current_device", "current_device ");
                    displayDeviceStatus(message.toString());
                }
            }

            private LineDataSet createSet() {
                LineDataSet set = new LineDataSet(null, "Sensor1 Data");
                set.setAxisDependency(YAxis.AxisDependency.LEFT);
                // Customize the dataset appearance here
                return set;
            }
            private void displayDeviceStatus(String deviceName) {
                txtDeviceStatus.setVisibility(View.VISIBLE); // Make sure the TextView is visible
                txtDeviceStatus.setText("Current Device: \n" + deviceName);
            }
            private void displayChart(float tempValue, LineChart mChart) {
                    LineData data = mChart.getData();
                    if (data == null) {
                        data = new LineData();
                        mChart.setData(data);
                    }
                    ILineDataSet set = data.getDataSetByLabel("Sensor1 Data", true);
                    if (set == null) {
                        set = createSet(); // A method to create a new dataset.
                        data.addDataSet(set);
                    }
                    data.addEntry(new Entry(set.getEntryCount(), tempValue), 0);
                    data.notifyDataChanged();

                    mChart.notifyDataSetChanged();
                    mChart.invalidate();
            }


            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}
