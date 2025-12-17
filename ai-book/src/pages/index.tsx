import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({ title, description, icon, link }: { title: string; description: string; icon?: string; link?: string }) {
  return (
    <div className="col col--4">
      <div className={clsx('card', styles.featureCard)}>
        <div className="card__body">
          <Heading as="h2" className={styles.featureCardTitle}>
            {title}
          </Heading>
          <p>{description}</p>
          {link && (
            <div className="card__footer">
              <Link className="button button--primary button--block" to={link}>
                Learn More
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics Book Documentation">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container padding-vert--lg">
            <div className="row">
              <FeatureCard
                title="Physical AI & Embodied Intelligence"
                description="Explore the intersection of artificial intelligence and physical systems, where AI learns through interaction with the real world."
              />
              <FeatureCard
                title="Humanoid Robotics & Simulation"
                description="Learn about humanoid robot design, control systems, and simulation environments for developing advanced robotic behaviors."
              />
              <FeatureCard
                title="AI-to-Physical World Integration"
                description="Understand how AI systems interact with and control physical environments, bridging the gap between digital and physical worlds."
              />
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
