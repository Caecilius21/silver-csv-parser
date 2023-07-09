import React from "react";
import { Typography, Box } from "@mui/material";

const MyTitle = () => {
  return (
    <Box display="flex" justifyContent="center" alignItems="center">
      <div>
        <img
          src="/static/images/logo.png"
          alt="Logo"
          style={{ width: "150px", height: "150px" }}
        />
      </div>
      <div>
        <Typography variant="h4" gutterBottom>
          CSV Parser App
        </Typography>
        <Typography variant="body1">
          A tool to upload, parse, and manage CSV files
        </Typography>
        <Typography variant="body2">Created by Ayoub Bouhachmoud</Typography>
      </div>
    </Box>
  );
};

export default MyTitle;
