import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Link from '@docusaurus/Link';

function ReadyToBuildTheFuture() {
  const { siteConfig } = useDocusaurusContext();

  // Inline style objects
  const styles = {
    hero: {
      // backgroundColor: '#000',
      color: '#ffdd00',
      padding: '4rem 2rem',
      borderRadius: '12px',
      marginBottom: '2rem',
      textAlign: 'center',
    },
    heroTitle: {
      fontSize: '3rem',
      fontWeight: 'bold',
      marginBottom: '1rem',
    },
    heroSubtitle: {
      fontSize: '1.5rem',
      color: '#fff700cc',
    },
    sectionTitle: {
      color: '#ffdd00',
      fontWeight: '700',
      marginBottom: '1rem',
      textAlign: 'center',
    },
    listItem: {
      margin: '0.5rem 0',
      lineHeight: '1.6',
    },
    buttonYellow: {
      backgroundColor: '#ffdd00',
      color: '#000',
      border: 'none',
      margin: '0.5rem',
      padding: '0.75rem 1.5rem',
      fontSize: '1.1rem',
      borderRadius: '6px',
      cursor: 'pointer',
      textDecoration: 'none',
      display: 'inline-block',
    },
    buttonYellowHover: {
      backgroundColor: '#ffd633',
    },
    quoteBlock: {
      borderLeft: '4px solid #ffdd00',
      paddingLeft: '1.5rem',
      fontStyle: 'italic',
      color: '#fff',
      backgroundColor: '#111',
      borderRadius: '8px',
      marginTop: '2rem',
    },
    section: {
      marginBottom: '2rem',
    },
    containerCenter: {
      maxWidth: '800px',
      margin: '0 auto',
    },
  };

  return (
    <section
      title={`Ready to Build the Future? - ${siteConfig.title}`}
      description="The closing page for the Physical AI & Humanoid Robotics textbook, inspiring students to build the future of robotics">
      <main>
        <div className="container margin-vert--lg" style={styles.containerCenter}>
          {/* Hero */}
          <header style={styles.hero}>
            <h1 style={styles.heroTitle}>🚀 Ready to Build the Future?</h1>
            <p style={styles.heroSubtitle}>
              You've mastered Physical AI & Humanoid Robotics. Now it's time to create real-world impact!
            </p>
          </header>

          {/* Journey */}
          <section style={styles.section}>
            <h2 style={styles.sectionTitle}>Your Journey Doesn't End Here</h2>
            <p>
              Congratulations! You've completed the Physical AI & Humanoid Robotics curriculum.
              You now have the skills to design, simulate, and deploy humanoid robots capable of
              natural human interactions using ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems.
            </p>
          </section>

          {/* What You've Learned */}
          <section style={styles.section}>
            <h2 style={styles.sectionTitle}>What You've Learned</h2>
            <ul>
              <li style={styles.listItem}>ROS 2 fundamentals: Nodes, Topics, Services, and URDF for humanoid robots</li>
              <li style={styles.listItem}>Digital twin simulation: Physics, rendering, and sensor simulation in Gazebo and Unity</li>
              <li style={styles.listItem}>NVIDIA Isaac: Advanced perception, Isaac Sim, Isaac ROS, and hardware-accelerated navigation</li>
              <li style={styles.listItem}>Vision-Language-Action systems: Voice commands, cognitive planning, and computer vision</li>
              <li style={styles.listItem}>Capstone project: Implementing autonomous humanoid robots</li>
            </ul>
          </section>

          {/* Next Steps */}
          <section style={styles.section}>
            <h2 style={styles.sectionTitle}>Next Steps</h2>
            <p>Now that you have the theoretical knowledge, it's time to put it into practice:</p>
            <ol>
              <li style={styles.listItem}>Set up your hardware environment (Jetson Orin Nano, sensors, etc.)</li>
              <li style={styles.listItem}>Start with the capstone project to apply everything you've learned</li>
              <li style={styles.listItem}>Join our community of Physical AI practitioners</li>
              <li style={styles.listItem}>Continue learning with advanced topics and research papers</li>
            </ol>
          </section>

          {/* Future */}
          <section style={styles.section}>
            <h2 style={styles.sectionTitle}>The Future is Embodied</h2>
            <p>
              Physical AI represents the convergence of digital intelligence and the physical world.
              As you venture into building real robots, remember that you're not just writing code—
              you're creating systems that interact with and understand the physical world.
            </p>
            <p>
              The humanoid robots of tomorrow depend on your understanding of robust control systems,
              accurate perception, intelligent decision-making, and seamless human-robot interaction.
            </p>
          </section>

          {/* Buttons */}
          <div style={{ textAlign: 'center', margin: '2rem 0' }}>
            <Link style={styles.buttonYellow} to="/docs/capstone-project/project-overview">Start Capstone Project</Link>
            <Link className="button button--secondary button--lg" to="/modules" style={ styles.buttonYellow }>Review Modules</Link>
            <Link  className="button button--secondary button--lg" to="/docs/intro" style={ styles.buttonYellow }>Revisit Introduction</Link>
          </div>

          {/* Quote */}
        <div>
            <div>
              <p>
                "The future belongs to those who understand the harmony between artificial intelligence
                and physical systems. You are now equipped to build that future."
              </p>
              <p><em>— The Physical AI & Humanoid Robotics Team</em></p>
            </div>
          </div>
        </div>
      </main>
    </section>
  );
}

export default ReadyToBuildTheFuture;
