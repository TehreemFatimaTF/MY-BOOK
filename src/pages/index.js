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
import ModulesPage from "./modules";

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

  return (
    <Layout title={siteConfig.title} description="Homepage">
      <HomepageHeader />
      <main>
        <WhyChooseThisBook />
        <ModulesPage />
        <ReadyToBuildTheFuture />
      </main>
    </Layout>
  );
}
