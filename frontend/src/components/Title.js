import * as React from "react";
import PropTypes from "prop-types";
import Typography from "@mui/material/Typography";

function Title(props) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <img
        src={props.imageSrc}
        alt="Title Image"
        style={{ marginRight: "10px", height: "48px" }}
      />
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        {props.children}
      </Typography>
    </div>
  );
}

Title.propTypes = {
  children: PropTypes.node,
  imageSrc: PropTypes.string.isRequired,
};

export default Title;
