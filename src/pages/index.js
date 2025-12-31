import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";

import Heading from "@theme/Heading";
import styles from "./index.module.css";

// homepage features & sections
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import WhyChooseThisBook from "../components/why-choose-book";
import ReadyToBuildTheFuture from "../components/ready-to-build-future";
import ModuleCard from "../components/ModuleCards/ModuleCard";
import HardwarePrerequisites from "../components/Chapter/HardwarePrerequisites";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className={styles.sectionWrapper}>
        <div className={styles.header}>
          <Heading as="h1">{siteConfig.title}</Heading>
          <p>{siteConfig.tagline}</p>
        </div>

        <div className={styles.buttons}>
          <Link className={styles.primaryBtn} to="/docs/intro">
            Go to Docs
          </Link>
          <Link className={styles.secondaryBtn} to="/modules">
            Browse Modules
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  // Define modules data
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
    <Layout title={siteConfig.title} description="Homepage">
      <HomepageHeader />
      
      <main>
        <WhyChooseThisBook />
        <section>
          <div className="container margin-vert--lg">
            <HardwarePrerequisites
              chapterTitle="ROS 2 on Real Robot"
              difficultyLevel="advanced"
              requiredHardware={["Humanoid Robot Platform", "Lidar Sensor", "Depth Camera"]}
            />
            <div className="row margin-vert--lg">
              {modules.map((module) => (
                <ModuleCard
                  key={module.id}
                  title={module.title}
                  description={module.description}
                  moduleNumber={module.id}
                  to={module.link}
                />
              ))}
            </div>
          </div>
        </section>
        <ReadyToBuildTheFuture />
      </main>
    </Layout>
  );
}
