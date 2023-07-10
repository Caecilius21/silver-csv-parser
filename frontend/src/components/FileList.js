import React, { useEffect, useState } from "react";
import {
  Typography,
  CircularProgress,
  Box,
  Button,
  Grid,
  FormControlLabel,
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { InsertDriveFile } from "@mui/icons-material";
import axios from "axios";

const FileList = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [selectAll, setSelectAll] = useState(false);
  const [uploadResult, setUploadResult] = useState([]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = () => {
    axios
      .get("http://127.0.0.1:8000/api/s3-bucket-files-list/")
      .then((response) => {
        setFiles(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching file data:", error);
        setLoading(false);
      });
  };

  const handleFileSelect = (file) => {
    if (selectedFiles.includes(file)) {
      setSelectedFiles(selectedFiles.filter((selected) => selected !== file));
    } else {
      setSelectedFiles([...selectedFiles, file]);
    }
  };

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedFiles([]);
    } else {
      setSelectedFiles(files);
    }
    setSelectAll(!selectAll);
  };

  const handleUploadData = () => {
    if (selectedFiles.length > 0) {
      axios
        .post("http://127.0.0.1:8000/api/upload-data-from-list/", {
          files: selectedFiles,
        })
        .then((response) => {
          setUploadResult(response.data);
          console.error(response.data);
          fetchFiles(); // Fetch the updated file list
        })
        .catch((error) => {
          console.error("Error uploading data:", error);
        });
    }
  };

  const handleDeleteFiles = () => {
    if (selectedFiles.length > 0) {
      axios
        .post("http://127.0.0.1:8000/api/delete-files-from-database/", {
          files: selectedFiles,
        })
        .then((response) => {
          console.log(response.data);
          setUploadResult(response.data); // Update the uploadResult state
          fetchFiles(); // Fetch the updated file list
        })
        .catch((error) => {
          console.error("Error deleting files:", error);
        });
    }
  };

  return (
    <div>
      <Grid container justifyContent="space-between" alignItems="center">
        <Grid item>
          <Typography variant="h5" gutterBottom>
            Files in AWS Bucket:
          </Typography>
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            color="primary"
            onClick={handleUploadData}
          >
            Upload Data to Database
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleDeleteFiles}
          >
            Delete Files Data from Database
          </Button>
        </Grid>
      </Grid>
      {loading ? (
        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
          minHeight="200px"
        >
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>
                  <Checkbox
                    checked={selectAll}
                    onChange={handleSelectAll}
                    color="primary"
                  />
                </TableCell>
                <TableCell>Filename</TableCell>
                <TableCell>Size</TableCell>
                <TableCell>Creation Date</TableCell>
                <TableCell>Is in database?</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {files.map((file, index) => {
                const matchingResult = uploadResult.find(
                  (result) => result.file_name === file.file_name
                );
                const resultMessage = matchingResult
                  ? matchingResult.message
                  : "";

                return (
                  <TableRow key={index}>
                    <TableCell>
                      <Checkbox
                        checked={selectedFiles.includes(file)}
                        onChange={() => handleFileSelect(file)}
                        color="primary"
                      />
                    </TableCell>
                    <TableCell>{file.file_name}</TableCell>
                    <TableCell>{file.size}B</TableCell>
                    <TableCell>{file.creation_date}</TableCell>
                    <TableCell
                      style={{ color: file.is_in_db ? "green" : "red" }}
                    >
                      {file.is_in_db.toString()}
                    </TableCell>
                    <TableCell>
                      <Typography
                        color={
                          matchingResult && matchingResult.status === "ko"
                            ? "error"
                            : matchingResult && matchingResult.status === "ok"
                            ? "success"
                            : "textSecondary"
                        }
                      >
                        {resultMessage}
                      </Typography>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
};

export default FileList;
