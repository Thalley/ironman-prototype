package com.example.thalley.sensorprototype;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.TextView;

import java.util.ArrayList;


public class MainActivity extends Activity implements SensorEventListener{
    private SensorManager mSensorManager;
    private Sensor mAccelerometer;
    private Sensor mMagnetic;
    private TextView tvX, tvY, tvZ, tvDD, tvD, tvTargetableObjects, tvAllObjects, tvPosition;
    private float[] magnetic, acceleration;
    private boolean haveacc, havemag;
    float[] Rm = new float[16];
    float[] I = new float[16];
    ArrayList<SmartObject> smartObjects = new ArrayList<>();
    StringBuilder b;
    Point position = new Point(5, 5);

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
        tvPosition = (TextView)findViewById(R.id.position);

        tvPosition.setText(position.toString());

        // Sensors
        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        mMagnetic = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);

        // Smart Objects
        smartObjects.add(new SmartObject("Lamp 1", new Point(0,0)));
        smartObjects.add(new SmartObject("Lamp 2", new Point(2,4)));
        smartObjects.add(new SmartObject("Coffee Maker", new Point(6,7)));
        smartObjects.add(new SmartObject("Stereo", new Point(9,9)));
        smartObjects.add(new SmartObject("TV", new Point(5,0)));
        smartObjects.add(new SmartObject("Garage Door", new Point(0,5)));

        // Show smart objects on main screen
        b = new StringBuilder();
        for (SmartObject so : smartObjects){
            b.append(so.getName() + so.getLocation().toString() + ", ");
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
                double directionDegrees = Math.toDegrees(result[0]);
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
     * Gets a general direction from degrees
     * @param degree
     * @return a direction such as "North", "West" or "Southeast"
     */
    private String degreeToDirection(double degree){
        String direction = "None";
        if(degree > -180)
            direction = "South";
        if(degree > -158.5)
            direction = "Southwest";
        if(degree > -112.5)
            direction = "West";
        if(degree > -67.5)
            direction = "Northwest";
        if(degree > -22.5)
            direction = "North";
        if(degree > 22.5)
            direction = "Northeast";
        if(degree > 67.5)
            direction = "East";
        if(degree > 112.5)
            direction = "Southeast";
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

        // Find all objects in that direction
        for (SmartObject so : smartObjects){
            if(getAngle(so.getLocation()) < deltaUpDegree && getAngle(so.getLocation()) > deltaDownDegree)
                targetableObjects.add(so);
        }

        // Print all objects found
        b = new StringBuilder();
        for (SmartObject so : targetableObjects){
            b.append(so.getName()+"\n");
        }
        tvTargetableObjects.setText(b.toString());
    }

    /**
     * Calculates the angle between our position and a smart device's position
     * @param target the targeted smart device
     * @return the angle in degrees
     */
    private double getAngle(Point target) {
        double angle = Math.toDegrees(Math.atan2(target.getX() - position.getX(),
                                                 target.getY() - position.getY()
                                                 ));
        return angle;
    }

    /**
     * onClick method for direction buttons. Changes the current position up, down, left or right
     * @param view the button being pressed
     */
    public void changePosition(View view){
        switch (view.getId()){
            case R.id.up:
                position.setX(position.getX() + 1);
                break;
            case R.id.down:
                position.setX(position.getX() - 1);
                break;
            case R.id.right:
                position.setY(position.getY() + 1);
                break;
            case R.id.left:
                position.setY(position.getY() - 1);
                break;
        }
        tvPosition.setText(position.toString());
    }
}
