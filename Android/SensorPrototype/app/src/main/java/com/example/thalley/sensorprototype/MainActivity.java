package com.example.thalley.sensorprototype;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.app.Activity;
import android.widget.TextView;

import java.util.ArrayList;


public class MainActivity extends Activity implements SensorEventListener{
    private SensorManager mSensorManager;
    private Sensor mAccelerometer;
    private Sensor mMagnetic;
    private TextView tvX, tvY, tvZ, tvDD, tvD, tvTargetableObjects, tvAllObjects;
    private float[] magnetic, acceleration;
    private boolean haveacc, havemag;
    float[] Rm = new float[16];
    float[] I = new float[16];
    ArrayList<SmartObject> smartObjects = new ArrayList<>();
    StringBuilder b;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Get textviews
        setContentView(R.layout.activity_main);
        tvX= (TextView)findViewById(R.id.x_axis);
        tvY= (TextView)findViewById(R.id.y_axis);
        tvZ= (TextView)findViewById(R.id.z_axis);
        tvDD= (TextView)findViewById(R.id.directionDegrees);
        tvD= (TextView)findViewById(R.id.direction);
        tvTargetableObjects = (TextView)findViewById(R.id.targetableObjects);
        tvAllObjects = (TextView)findViewById(R.id.objects);

        // Sensors
        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        mMagnetic = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);

        // Smart Objects
        smartObjects.add(new SmartObject("Lamp 1", 0.0));
        smartObjects.add(new SmartObject("Lamp 2", 35.0));
        smartObjects.add(new SmartObject("Coffee Maker", 45.0));
        smartObjects.add(new SmartObject("Stereo", -85.0));
        smartObjects.add(new SmartObject("TV", 130.0));
        smartObjects.add(new SmartObject("Garage Door", -100.0));

        // Show smart objects on main screen
        b = new StringBuilder();
        for (SmartObject so : smartObjects){
            b.append(so.mName+ "(" + (int)so.mLocation + "), ");
        }
        tvAllObjects.setText(b.toString());
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if(event.sensor.equals(mAccelerometer)){
            haveacc = true;
            // Get and show accelerometer data
            acceleration = event.values.clone();
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];
            tvX.setText(String.format("%.2f", x));
            tvY.setText(String.format("%.2f", y));
            tvZ.setText(String.format("%.2f", z));
        }
        else if (event.sensor.equals(mMagnetic)){
            // Get magnetometer data
            havemag = true;
            magnetic = event.values.clone();
        }

        if (haveacc && havemag) {
            // Using data from accelerometer and magnetometer, get a rotation matrix for the device
            if (SensorManager.getRotationMatrix(Rm, I, acceleration, magnetic)) {
                float[] result = new float[3];
                // Using the rotation matrix, get orientation in radians
                SensorManager.getOrientation(Rm, result);
                // Get degrees from radius along the x-axis
                double directionDegrees = radianToDegree(result[0]);
                //Update direction in the UI
                tvDD.setText((int)directionDegrees +"");
                tvD.setText(degreeToDirection(directionDegrees));
                updateObjects(directionDegrees);
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }

    @Override
    protected void onResume() {
        super.onResume();
        mSensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(this, mMagnetic, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected void onPause() {
        // Be sure to unregister the sensor when the activity pauses.
        super.onPause();
        mSensorManager.unregisterListener(this);
    }

    /**
     * Converts radians to degrees
     * @param radian the degree in radians
     * @return the degree between -180 and 180
     */
    private double radianToDegree(float radian){
        return 180/Math.PI * radian;
    }

    /**
     * Gets a general direction from degrees
     * @param degree
     * @return a direction such as "North", "West" or "Southeast"
     */
    private String degreeToDirection(double degree){
        String direction = "None";
        if(degree > -180)
            direction = "South";
        if(degree > -158.5)
            direction = "Southeast";
        if(degree > -112.5)
            direction = "East";
        if(degree > -67.5)
            direction = "Northeast";
        if(degree > -22.5)
            direction = "North";
        if(degree > 22.5)
            direction = "Northwest";
        if(degree > 67.5)
            direction = "West";
        if(degree > 112.5)
            direction = "Southwest";
        if(degree > 158.5)
            direction = "South";
        return direction;
    }

    /**
     * Updates the UI with targetable objects
     * @param degree the current direction in degrees
     */
    private void updateObjects(double degree){
        double noise = 15; // Adds some space/noise
        double deltaUpDegree = degree + noise;
        double deltaDownDegree = degree - noise;
        ArrayList<SmartObject> targetableObjects = new ArrayList<>();
        for (SmartObject so : smartObjects){
            if(so.mLocation < deltaUpDegree && so.mLocation > deltaDownDegree)
                targetableObjects.add(so);
        }
        b = new StringBuilder();
        for (SmartObject so : targetableObjects){
            b.append(so.mName+"\n");
        }
        tvTargetableObjects.setText(b.toString());

    }
}
