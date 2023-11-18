import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Box, Grid } from "@mui/material";
import BoardModel from "../Board/BoardModel";
import Header from "./Header";

const Home = () => {
  const { isMobile, screen } = useSelector(({ ui }) => ui);
  const [showBoard, setShowBoard] = useState(false);
  const [showHeader, setShowHeader] = useState(false);

  useEffect(() => {
    const timeout1 = setTimeout(() => setShowBoard(true), 400);
    const timeout2 = setTimeout(() => setShowHeader(true), 1500);
    return () => {
      clearTimeout(timeout1);
      clearTimeout(timeout2);
    };
  }, []);
  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        position: "relative",
        px: "5%",
        pb: "10%",
      }}>
      <Grid
        container
        direction={!isMobile || screen.orientation === "landscape" ? "row" : "column"}
        maxHeight={!isMobile || screen.orientation === "landscape" ? "600px" : "100%"}
        sx={{
          zIndex: 99,
          height: "100%",
          alignItems: "center",
          justifyContent: "center",
        }}>
        <Grid
          item
          xs={6}
          sx={{
            height: { sm: "100%", xs: "50%" },
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}>
          <Header show={showHeader} />
        </Grid>
        <Grid
          item
          xs={6}
          sx={{
            position: "relative",
            height: { sm: "100%", xs: "50%" },
            width: "100%",
            pt: isMobile ? 0 : "5%",
            opacity: showBoard ? 1 : 0,
            transition: "2s",
          }}>
          <BoardModel />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Home;
