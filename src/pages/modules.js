import React from "react";
import Layout from "@theme/Layout"; // Isko use karna zaroori hai
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import ModuleCard from "../components/ModuleCards/ModuleCard";
import HardwarePrerequisites from "../components/Chapter/HardwarePrerequisites";

function ModulesPage() {
  const { siteConfig } = useDocusaurusContext();

  const modules = [
    {
      id: 1,
      title: "The Robotic Nervous System (ROS 2)",
      description: "Learn about middleware for robot control, including ROS 2 Nodes, Topics, and Services.",
      link: "/docs/module-1-ros2/chapter-1-intro-ros2",
    },
    {
      id: 2,
      title: "The Digital Twin (Gazebo & Unity)",
      description: "Master physics simulation and environment building.",
      link: "/docs/module-2-digital-twin/chapter-1-physics-simulation",
    },
    {
      id: 3,
      title: "The AI-Robot Brain (NVIDIA Isaac™)",
      description: "Explore advanced perception and training with NVIDIA Isaac Sim.",
      link: "/docs/module-3-nvidia-isaac/chapter-1-isaac-sim",
    },
    {
      id: 4,
      title: "Vision-Language-Action (VLA)",
      description: "Understand the convergence of LLMs and Robotics.",
      link: "/docs/module-4-vla-humanoids/chapter-1-voice-to-action",
    },
  ];

  return (
    // <section> ki jagah <Layout> use karein taake header/footer nazar aayein
    <section
      title={`Modules - ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics curriculum modules"
    >
      <main>
        <div className="container margin-vert--lg">
          <header className="hero hero--primary" style={{ borderRadius: '10px', marginBottom: '2rem' }}>
            <div className="container">
              <h1 className="hero__title">Physical AI Curriculum Modules</h1>
              <p className="hero__subtitle">Explore the comprehensive curriculum</p>
            </div>
          </header>

          <HardwarePrerequisites
            chapterTitle="ROS 2 on Real Robot"
            difficultyLevel="advanced"
            requiredHardware={["Humanoid Robot Platform", "Lidar Sensor", "Depth Camera"]}
          />

          {/* MODULES PAGE (Sahi Version) */}
<div className="row margin-vert--lg">
  {modules.map((module) => (
    <ModuleCard
      key={module.id}
      title={module.title}
      description={module.description}
      moduleNumber={module.id}
      // YAHAN FIX HAI: 'link' ki jagah 'to' likhein
      to={module.link} 
    />
  ))}
</div>
        </div>
      </main>
    </section>
  ); // Yahan extra bracket khatam kar diya gaya hai
}

export default ModulesPage;