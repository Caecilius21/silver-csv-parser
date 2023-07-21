import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import axios from "axios";
import { styled } from "@mui/material/styles";

const StyledTableRow = styled(TableRow)(({ theme, status }) => ({
  backgroundColor: status === "ok" ? "#c8e6c9" : "#ffcdd2",
}));

const IngestionMessageList = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIngestionMessages();
  }, []);

  const fetchIngestionMessages = () => {
    axios
      .get("http://127.0.0.1:8000/api/ingestion-message-list/")
      .then((response) => {
        setMessages(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching ingestion messages:", error);
        setLoading(false);
      });
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>File Name</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Message</TableCell>
            <TableCell>Ingestion Timestamp</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {loading ? (
            <StyledTableRow status="ok">
              <TableCell colSpan={5}>Loading...</TableCell>
            </StyledTableRow>
          ) : (
            messages.map((message) => (
              <StyledTableRow key={message.id} status={message.status}>
                <TableCell>{message.file}</TableCell>
                <TableCell>{message.status}</TableCell>
                <TableCell>{message.message}</TableCell>
                <TableCell>{message.ingestion_timestamp}</TableCell>
              </StyledTableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default IngestionMessageList;
