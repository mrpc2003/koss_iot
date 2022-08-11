package com.example.myapplication;

import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;

import java.util.HashMap;
import java.util.Map;

public class Sensors_ extends StringRequest {
    final static private String URL = "http://192.168.43.4:3000/devices/device";
    private Map<String, String> parameters;

    public Sensors_(String sensor, Response.Listener<String> listener){
        super(Method.POST, URL, listener, null);
        parameters=new HashMap<>();
        parameters.put("sensor",sensor);
    }

    @Override
    protected Map<String, String> getParams() {
        return parameters;
    }
}
