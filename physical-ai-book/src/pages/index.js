import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HeroSection from '@site/src/components/HeroSection';
import FloatingAskAIButton from '@site/src/components/FloatingAskAIButton';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Comprehensive Guide to Physical AI and Humanoid Robotics">
      <HeroSection />
      <FloatingAskAIButton />
    </Layout>
  );
}
