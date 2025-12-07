import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import { useLocation } from '@docusaurus/router';
import BrowserOnly from '@docusaurus/BrowserOnly';

const CustomNavbar = (props) => {
  const location = useLocation();

  // Don't show custom navbar on 404 page
  if (location.pathname === '/404') {
    return <OriginalNavbar {...props} />;
  }

  // For now, we'll extend the original navbar with additional functionality
  // In a more complex implementation, we could replace it entirely
  return (
    <>
      <OriginalNavbar {...props} />
      <BrowserOnly>
        {() => {
          // Add any additional navbar functionality here if needed
          // For now, we'll just return null to not add extra elements
          return null;
        }}
      </BrowserOnly>
    </>
  );
};

export default CustomNavbar;