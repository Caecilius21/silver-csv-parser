import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import axios from "axios";

const TimelineGraph = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/timeline-data/"
        );
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const options = {
    chart: {
      type: "line",
      stacked: false,
      height: 350,
    },
    xaxis: {
      type: "datetime",
      labels: {
        format: "dd MMM yyyy",
      },
    },
    yaxis: [
      {
        title: {
          text: "Number of Files",
        },
        min: 0,
      },
      {
        opposite: true,
        title: {
          text: "Number of Rows",
        },
        min: 0,
      },
    ],
  };

  const series = [
    {
      name: "Files",
      type: "line",
      data: data ? data.files : [],
    },
    {
      name: "Rows",
      type: "bar",
      data: data ? data.rows : [],
      yaxis: 1,
    },
  ];

  return (
    <div>
      <h2>Timeline Graph</h2>
      {data && data.files.length > 0 ? (
        <Chart options={options} series={series} type="line" height={350} />
      ) : (
        <p>No data available</p>
      )}
    </div>
  );
};

export default TimelineGraph;
