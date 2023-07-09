import React, { useEffect, useState } from "react";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import axios from "axios";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>;
    }
    return this.props.children;
  }
}

const CSVDataTable = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);
  const [totalFiles, setTotalFiles] = useState(0);
  const [totalUniqueData, setTotalUniqueData] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/csv-data/");
        const data = response.data;
        const csvColumns = Object.keys(data[0]);
        setColumns(csvColumns);
        setRows(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();

    const fetchMetadata = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/database-metadata/"
        );
        const { total_unique_files, total_data } = response.data;
        setTotalFiles(total_unique_files);
        setTotalUniqueData(total_data);
      } catch (error) {
        console.error("Error fetching metadata:", error);
      }
    };

    fetchMetadata();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <ErrorBoundary>
      <Paper sx={{ width: "100%", overflow: "hidden" }}>
        <div style={{ padding: "16px" }}>
          <h2>CSV Data Table</h2>
          <p>Total Files: {totalFiles}</p>
          <p>Total Unique Data: {totalUniqueData}</p>
        </div>
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell key={column}>{column}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, index) => {
                  return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                      {columns.map((column) => (
                        <TableCell key={column}>{row[column]}</TableCell>
                      ))}
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 25, 100]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </ErrorBoundary>
  );
};

export default CSVDataTable;
