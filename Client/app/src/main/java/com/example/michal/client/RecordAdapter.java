package com.example.michal.client;

import android.content.Intent;
import android.support.v7.widget.RecyclerView;
import android.util.JsonReader;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;

import static com.example.michal.client.MainActivity.USERNAME;

public class RecordAdapter extends RecyclerView.Adapter<RecordAdapter.MyViewHolder> {
    private ArrayList<JSONObject> mDataset;
    private ArrayList<JSONObject> mDatasetCopy;

    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder
    public static class MyViewHolder extends RecyclerView.ViewHolder {
        // each data item is just a string in this case
        public TextView textView;
        public MyViewHolder(TextView v) {
            super(v);
            textView = v;
        }
    }

    // Provide a suitable constructor (depends on the kind of dataset)
    public RecordAdapter(ArrayList<JSONObject> myDataset) {
        mDataset = myDataset;
        mDatasetCopy.addAll(myDataset);
    }

    public RecordAdapter() {
        mDataset = new ArrayList<JSONObject>();
        mDatasetCopy = new ArrayList<JSONObject>();
    }

    // Create new views (invoked by the layout manager)
    @Override
    public RecordAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent,
                                                         int viewType) {
        // create a new view
        TextView v = (TextView) LayoutInflater.from(parent.getContext())
                .inflate(R.layout.view_line, parent, false);

        MyViewHolder vh = new MyViewHolder(v);
        return vh;
    }

    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(final MyViewHolder holder, final int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        Iterator<String> keys = mDataset.get(position).keys();
        final String name = keys.next();
        holder.textView.setText(name);

        holder.textView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(v.getContext(), RecordActivity.class);

                try {
                    JSONObject obj = (JSONObject)mDataset.get(position).get(name);
                    String email = obj.get("email").toString();
                    String website  = obj.get("website").toString();
                    String phone  = obj.get("phone").toString();
                    intent.putExtra("EMAIL", email);
                    intent.putExtra("WEBSITE", website);
                    intent.putExtra("PHONE", phone);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                intent.putExtra("NAME", name);

                v.getContext().startActivity(intent);
            }
        });

    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.size();
    }

    public void setData(ArrayList<JSONObject> DataSet)
    {
        if (DataSet != null) {
            mDataset = DataSet;
            mDatasetCopy.addAll(DataSet);
        }
    }

    public void filter(String text) {
        mDataset.clear();
        if(text.isEmpty()){
            mDataset.addAll(mDatasetCopy);
        } else {
            text = text.toLowerCase();
            for(JSONObject record: mDatasetCopy){
                String name = record.keys().next();
                if(name.toLowerCase().contains(text)){
                    mDataset.add(record);
                }
            }
        }
        notifyDataSetChanged();
    }

    public void onClick() {

    }
}
