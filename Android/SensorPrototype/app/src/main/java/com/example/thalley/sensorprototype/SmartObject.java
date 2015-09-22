package com.example.thalley.sensorprototype;

/**
 * A smart device
 */
public class SmartObject {
    private String mName;
    private Point mLocation; //as a degree
    public SmartObject(String name, Point location){
        mName = name;
        mLocation = location;
    }

    public String getName(){
        return mName;
    }

    public Point getLocation(){
        return mLocation;
    }
}
