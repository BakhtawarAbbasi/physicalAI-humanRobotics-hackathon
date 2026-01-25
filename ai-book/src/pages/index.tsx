import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HeroSection() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <section className="hero-section fade-in">
      <div className="hero-section__content">
        <Heading as="h1" className="hero-section__title slide-up">
          {siteConfig.title}
        </Heading>
        <p className="hero-section__subtitle slide-up-delay-1">{siteConfig.tagline}</p>
        <div className={`${styles.buttons} slide-up-delay-2`}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Reading
          </Link>
        </div>
      </div>
    </section>
  );
}

function ModuleCard({ title, description, icon, link, animationDelay }: { title: string; description: string; icon?: string; link?: string; animationDelay?: string }) {
  const cardClass = animationDelay ? `module-card slide-up ${animationDelay}` : 'module-card slide-up';
  return (
    <div className="col col--4">
      <div className={cardClass}>
        <div className="module-card__icon">
          {icon || '🤖'}
        </div>
        <Heading as="h2" className="module-card__title">
          {title}
        </Heading>
        <p className="module-card__description">
          {description}
        </p>
        {link && (
          <div className="module-card__footer">
            <Link className="button button--primary" to={link}>
              Explore Module
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} - Advanced Physical AI & Humanoid Robotics`}
      description="Professional book on Physical AI and Humanoid Robotics - Modern approach to embodied intelligence and robotics">
      <HeroSection />
      <main>
        <section className={styles.modules}>
          <div className="container padding-vert--lg">
            <div className="row">
              <ModuleCard
                title="Physical AI & Embodied Intelligence"
                description="Explore the intersection of artificial intelligence and physical systems, where AI learns through interaction with the real world. Understand how embodied cognition shapes intelligent behavior."
                link="/docs/module-01/chapter-1-ros2-fundamentals"
                animationDelay="slide-up-delay-1"
              />
              <ModuleCard
                title="Humanoid Robotics & Simulation"
                description="Learn about humanoid robot design, control systems, and simulation environments for developing advanced robotic behaviors and human-like movements."
                link="/docs/module-02/chapter-1-gazebo-physics"
                animationDelay="slide-up-delay-2"
              />
              <ModuleCard
                title="AI-to-Physical World Integration"
                description="Understand how AI systems interact with and control physical environments, bridging the gap between digital intelligence and physical reality."
                link="/docs/module-03/isaac-sim"
                animationDelay="slide-up-delay-3"
              />
              <ModuleCard
                title="Voice to Action & Cognitive Planning"
                description="Discover how voice commands are processed and transformed into robotic actions, with advanced cognitive planning for complex task execution."
                link="/docs/module-04/voice-to-action"
                animationDelay="slide-up-delay-1"
              />
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
