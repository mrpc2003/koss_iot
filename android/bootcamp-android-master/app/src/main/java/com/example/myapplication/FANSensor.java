package com.example.myapplication;

import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;

import java.util.HashMap;
import java.util.Map;

public class FANSensor extends StringRequest {
    final static private String URL = "http://192.168.43.4:3000/devices/led";
    private Map<String, String> parameters;

    public FANSensor(String led, Response.Listener<String> listener){
        super(Method.POST, URL, listener,null);
        parameters = new HashMap<>();
        parameters.put("flag",led);
    }
    @Override
    protected Map<String, String> getParams(){
        return parameters;
    }
}
