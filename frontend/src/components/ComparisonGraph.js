import React, { useState, useEffect } from "react";
import { Typography, CircularProgress } from "@mui/material";
import Chart from "react-apexcharts";
import axios from "axios";

const ComparisonGraph = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/s3-vs-database-comparison/"
        );
        console.log(response.data);
        setData(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const options = {
    chart: {
      type: "bar",
      height: 350,
    },
    plotOptions: {
      bar: {
        horizontal: true,
      },
    },
    xaxis: {
      categories: ["Database", "S3 Bucket"],
    },
  };

  const series = [
    {
      name: "Files",
      data: [data?.db_total_files || 0, data?.s3_total_files || 0],
    },
  ];

  return (
    <div>
      <Typography variant="h5" gutterBottom>
        Comparison Graph
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <Chart options={options} series={series} type="bar" />
      )}
    </div>
  );
};

export default ComparisonGraph;
