package com.example.myapplication;

import android.app.ProgressDialog;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.ArrayList;
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 스피너
        final String[] sensors={"sensors_","mq2"};
        ArrayAdapter<String> spinnerAdapter= new ArrayAdapter<String>(
                MainActivity.this,
                android.R.layout.simple_spinner_dropdown_item, sensors);
        // Alt+Enter
        Spinner spinner=(Spinner)findViewById(R.id.spinner);
        spinner.setAdapter(spinnerAdapter);
        //스피너 선택시 동작되는 부분 : 센서 데이터 가져오기
        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                final ProgressDialog dialog=new ProgressDialog(MainActivity.this);
                dialog.setMessage("센서 로그 정보 수신 중....");
                dialog.show();
                Response.Listener<String> listener=new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        dialog.dismiss();
                        try {
                            JSONArray array=new JSONArray(response);
                            items.clear();  
                            for(int i=0; i<array.length();i++){
                                JSONObject obj=array.getJSONObject(i);
                                items.add(new Item(
                                        obj.getInt("pm1"),
                                        obj.getInt("pm2"),
                                        obj.getInt("pm10"),
                                        obj.getString("created_at")));
                            }//_for
                            ItemAdapter adapter=new ItemAdapter(MainActivity.this);
                            ListView listView=(ListView)findViewById(R.id.listview);
                            listView.setAdapter(adapter);
                        }catch (Exception e){
                            e.printStackTrace();
                        }
                    }
                };
            StringRequest sensors_ =new Sensors_(sensors[i], listener);
            sensors_.setShouldCache(false);
            RequestQueue requestQueue = Volley.newRequestQueue(MainActivity.this);
            requestQueue.add(sensors_);

        }
        @Override
        public void onNothingSelected(AdapterView<?> adapterView) {
        }
        });
    }
    // 리스트뷰 안에 들어갈 아이템
    class Item{
        int temp, humidity, altitude, pressure,pm1,pm2,pm10; String created_at;
        Item(int pm1, int pm2, int pm10, String created_at){
            this.pm1=pm1;
            this.pm2=pm2;
            this.pm10=pm10;
            this.created_at=created_at;
        }
    }
    ArrayList<Item> items=new ArrayList<Item>();
    class ItemAdapter extends ArrayAdapter{
        public ItemAdapter(Context context) {
            super(context, R.layout.list_sensor_item, items);
        }
        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View view=convertView;
            if(view==null){
                LayoutInflater inflater=
                        (LayoutInflater)getSystemService(LAYOUT_INFLATER_SERVICE);
                view=inflater.inflate(R.layout.list_sensor_item, null);
            }
            // 텍스트뷰 정의
            TextView pm1Text=view.findViewById(R.id.pm1);
            TextView pm2Text=view.findViewById(R.id.pm2);
            TextView pm10Text=view.findViewById(R.id.pm10);
            TextView createdAtText=view.findViewById(R.id.created_at);
            // 값 할당
            pm1Text.setText("pm1: "+items.get(position).pm1);
            pm2Text.setText("pm2: "+items.get(position).pm2);
            pm10Text.setText("pm10: "+items.get(position).pm10);
            createdAtText.setText("수집정보(날짜/시간)"+items.get(position).created_at);
            return view;
        }
    }
    // FAN ON 버튼 클릭시 동작되는 부분
    public void clickFanOnButton(View view) {
    // 서버 응답시 실행되는 콜백 리스너
        Response.Listener<String> listener=new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONObject obj=new JSONObject(response); Toast.makeText(getApplicationContext(),
                        "led가 켜짐:"+obj.get("led"), Toast.LENGTH_SHORT).show();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        };
        StringRequest led=new FANSensor("on", listener);
        led.setShouldCache(false);
        RequestQueue requestQueue_fan = Volley.newRequestQueue(MainActivity.this);
        requestQueue_fan.add(led);
    }
// FAN OFF 버튼 클릭시 동작되는 부분
    public void clickFanOffButton(View view) {
// 서버 응답시 실행되는 콜백 리스너
        Response.Listener<String> listener=new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONObject obj=new JSONObject(response);
                    Toast.makeText(getApplicationContext(),
                "led가 꺼짐:"+obj.get("led"), Toast.LENGTH_SHORT).show();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        };
        StringRequest led=new FANSensor("off", listener);
        led.setShouldCache(false);
        RequestQueue requestQueue_fan = Volley.newRequestQueue(MainActivity.this);
        requestQueue_fan.add(led);
    }
}