import React, { Component, useState } from "react";
import { render } from "react-dom";
import FileList from "./FileList";
import CSVDataTable from "./CSVDataTable";
import MyTitle from "./MyTitle";
import ComparisonGraph from "./ComparisonGraph";
import { Grid } from "@mui/material";
import TimelineGraph from "./TimeLineGraph";
import IngestionMessageList from "./IngestionMessageList";

function App() {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <MyTitle />
      </Grid>
      <Grid item xs={12} md={12}>
        <FileList />
      </Grid>
      <Grid item xs={12} md={12}>
        <CSVDataTable />
      </Grid>
      <Grid item xs={6}>
        <ComparisonGraph />
      </Grid>
      <Grid item xs={6}>
        <TimelineGraph />
      </Grid>
      <Grid item xs={12} md={12}>
        <IngestionMessageList />
      </Grid>
    </Grid>
  );
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
