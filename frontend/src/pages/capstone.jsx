import React from 'react';
import Layout from '@theme/Layout';
import ProjectTracker from '../components/Capstone/ProjectTracker';

export default function CapstonePage() {
  return (
    <Layout title="Capstone Project">
      <main>
        <div className="container margin-vert--lg">
          <h1>Capstone Project Tracker</h1>
          <ProjectTracker />
        </div>
      </main>
    </Layout>
  );
}
