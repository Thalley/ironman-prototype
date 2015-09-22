package com.example.thalley.sensorprototype;

/**
 * A Point is a point in a coordinate system
 */
public class Point {
    private int mX, mY;
    public Point(int X, int Y){
        mX = X;
        mY = Y;
    }

    public int getX() {
        return mX;
    }

    public void setX(int X) {
        this.mX = X;
    }

    public int getY() {
        return mY;
    }

    public void setY(int Y) {
        this.mY = Y;
    }

    @Override
    public String toString(){
        return "(" + mX + "," + mY + ")";

    }
}
