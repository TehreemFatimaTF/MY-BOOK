import React from "react";
import Link from "@docusaurus/Link";

export default function WhyChooseThisBook() {
  const [hoveredCard, setHoveredCard] = React.useState(null);

  // Cards content
  const cards = [
    {
      title: "The Future of AI is Physical",
      content:
        "The next wave of AI moves beyond screens into the physical world. Learn how robots understand physics and interact naturally.",
    },
    {
      title: "Comprehensive Curriculum",
      content: [
        "Module 1: The Robotic Nervous System (ROS 2)",
        "Module 2: The Digital Twin (Gazebo & Unity)",
        "Module 3: The AI-Robot Brain (NVIDIA Isaac™)",
        "Module 4: Vision-Language-Action (VLA)",
      ],
    },
    {
      title: "Cutting-Edge Tech",
      content: [
        "ROS2 robotic middleware",
        "NVIDIA Isaac perception + navigation",
        "Simulation in Gazebo + Unity",
        "Vision-Language-Action systems",
      ],
    },
    {
      title: "Hands-On Learning",
      content: [
        "Jetson Orin hardware setup",
        "Sim-to-Real transfer",
        "Autonomous humanoid robots",
      ],
    },
  ];

  // Styles using CSS variables for theme compatibility
  const styles = {
    sectionWrapper: {
      backgroundColor: "var(--ifm-background-color)",
      color: "var(--ifm-color-primary)",
      padding: "4rem 2rem",
      borderRadius: "12px",
      margin: "2rem 0",
      fontFamily: "Arial, sans-serif",
      transition: "background 0.3s, color 0.3s",
    },
    header: {
      textAlign: "center",
      marginBottom: "3rem",
    },
    headerTitle: {
      fontSize: "2.5rem",
      fontWeight: "bold",
      marginBottom: "0.5rem",
      color: "var(--ifm-color-primary)", // accent color
    },
    headerSubtitle: {
      fontSize: "1.2rem",
      color: "var(--ifm-color-secondary)",
    },
    content: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
      gap: "1.5rem",
    },
    card: {
      backgroundColor: "var(--ifm-color-neutral-100)", // light card background
      border: "2px solid var(--ifm-color-primary)",
      borderRadius: "12px",
      padding: "1.5rem",
      transition: "transform 0.2s, box-shadow 0.2s, background 0.3s, border 0.3s",
      color: "var(--ifm-color-primary)",
    },
    cardHover: {
      transform: "translateY(-5px)",
      boxShadow: "0 8px 20px var(--ifm-color-primary)",
    },
    cardTitle: {
      fontSize: "1.5rem",
      fontWeight: "bold",
      marginBottom: "0.5rem",
    },
    cardList: {
      paddingLeft: "1rem",
      lineHeight: "1.6",
    },
    buttons: {
      marginTop: "3rem",
      display: "flex",
      justifyContent: "center",
      gap: "1rem",
      flexWrap: "wrap",
    },
    primaryBtn: {
       backgroundColor: "transparent",
      color: "var(--ifm-color-primary)",
      padding: "0.75rem 1.5rem",
      fontSize: "1.1rem",
      fontWeight: "bold",
      border: "2px solid var(--ifm-color-primary)",
      borderRadius: "6px",
      textDecoration: "none",
      textAlign: "center",
      display: "inline-block",
      transition: "background 0.2s, color 0.2s",
    },
    secondaryBtn: {
      backgroundColor: "transparent",
      color: "var(--ifm-color-primary)",
      padding: "0.75rem 1.5rem",
      fontSize: "1.1rem",
      fontWeight: "bold",
      border: "2px solid var(--ifm-color-primary)",
      borderRadius: "6px",
      textDecoration: "none",
      textAlign: "center",
      display: "inline-block",
      transition: "background 0.2s, color 0.2s",
    },
  };

  return (
    <section style={styles.sectionWrapper}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.headerTitle}>Why Choose This Book?</h1>
        <p style={styles.headerSubtitle}>
          The definitive guide to Physical AI & Humanoid Robotics
        </p>
      </div>

      {/* Content Cards */}
      <div style={styles.content}>
        {cards.map((card, index) => (
          <div
            key={index}
            style={{
              ...styles.card,
              ...(hoveredCard === index ? styles.cardHover : {}),
            }}
            onMouseEnter={() => setHoveredCard(index)}
            onMouseLeave={() => setHoveredCard(null)}
          >
            <h2 style={styles.cardTitle}>{card.title}</h2>
            {Array.isArray(card.content) ? (
              <ul style={styles.cardList}>
                {card.content.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>{card.content}</p>
            )}
          </div>
        ))}
      </div>

      {/* CTA Buttons */}
      <div style={styles.buttons}>
        <Link style={styles.primaryBtn} to="/docs/intro">
          Start Learning
        </Link>
        <Link style={styles.secondaryBtn} to="/">
          Browse Modules
        </Link>
      </div>
    </section>
  );
}
