package com.example.michal.client;

import android.support.v7.widget.RecyclerView;
import android.util.JsonReader;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.TextView;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;

public class RecordAdapter extends RecyclerView.Adapter<RecordAdapter.MyViewHolder> {
    private ArrayList<JSONObject> mDataset;

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
    }

    public RecordAdapter() {
        mDataset = new ArrayList<JSONObject>();
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
    public void onBindViewHolder(MyViewHolder holder, int position) {
        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        Iterator<String> keys = mDataset.get(position).keys();
        String str_Name=keys.next();
        String title;
        try {
            title = mDataset.get(position).getString(str_Name);
        } catch (org.json.JSONException e) {
            title = "error";
            System.out.println(e);
        }
        holder.textView.setText(title);

    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.size();
    }

    public void setData(ArrayList<JSONObject> DataSet)
    {
        mDataset = DataSet;
    }
}
