import React from "react";
import { useSelector } from "react-redux";
import { Box, Drawer } from "@mui/material";
import AlgosList from "./AlgosList";

const SideMenu = () => {
  const { sideMenu, topBar } = useSelector(({ ui }) => ui);

  return (
    <Drawer
      id="sideMenu"
      anchor="left"
      variant="permanent"
      ModalProps={{ keepMounted: true }}
      sx={{
        color: "red",
        "& .MuiDrawer-paper": {
          border: 0,
          width: sideMenu.width,
          height: '100%',
          transition: "width 0.3s",
          msOverflowStyle: "none",
          scrollbarWidth: "none",
        },
      }}>
      <AlgosList />

    </Drawer>
  );
};

export default SideMenu;
