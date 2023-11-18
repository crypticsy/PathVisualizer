import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Box } from "@mui/material";
import SideMenu from "./sidebar/SideMenu";
import TopBar from "./topbar/TopBar";
import { uiChanged } from "../../store/ui";

const Layout = ({ children }) => {
  const dispatch = useDispatch();
  const { isMobile } = useSelector(({ ui }) => ui);

  window.addEventListener("orientationchange", () => {
    const { angle } = window.screen.orientation;
    dispatch(
      uiChanged({
        prop: "screen",
        att: "orientation",
        val: angle === 90 ? "landscape" : "portrait",
      })
    );
  });

  useEffect(() => {
    const { angle } = window.screen.orientation;

    dispatch(
      uiChanged({
        prop: "screen",
        att: "orientation",
        val: angle === 90 ? "landscape" : "portrait",
      })
    );
  }, []);

  return (
    <Box
      display="flex"
      justifyContent="flex-end"
      alignItems="flex-end"
      flexDirection="column"
      width="100%"
      height="100%"
      overflow="hidden"
      minWidth={isMobile ? "auto" : 900}
      bgcolor="red">
      <TopBar />
      {children}
      <SideMenu />
    </Box>
  );
};

export default Layout;
