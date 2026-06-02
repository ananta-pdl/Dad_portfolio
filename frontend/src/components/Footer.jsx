import React from 'react';
import { NavLink } from 'react-router-dom';
import { Copyright, Heart } from 'lucide-react';
import { Facebook, Youtube, Instagram } from './SocialIcons';
import './Footer.css';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const socialLinks = {
    facebook: "https://facebook.com/dummy",
    youtube:  "https://youtube.com/dummy",
    instagram: "https://instagram.com/dummy"
  };

  return (
    <footer className="footer-container glass-panel">
      <div className="footer-content">
        {/* Brand */}
        <div className="footer-brand">
          <h3>Gandharba Raj Paudel</h3>

          <p className="brand-description">
            A Loan Officer who spent his youth writing melodies, recording vocals,
            and performing on stage. Today he bridges structured leadership with creative spirit.
          </p>
        </div>

        {/* Quick Links */}
        <div className="footer-nav">
          <h4>Navigate</h4>
          <div className="footer-links">
            <NavLink to="/">Home &amp; About</NavLink>
            <NavLink to="/gallery">Achievements</NavLink>
            <NavLink to="/music">Music Lounge</NavLink>
            <NavLink to="/contact">Contact</NavLink>
          </div>
        </div>

        {/* Social tiles */}
        <div className="footer-socials">
          <h4>Connect</h4>
          <div className="social-grid">
            <a href={socialLinks.facebook} target="_blank" rel="noopener noreferrer"
               className="social-card fb" aria-label="Connect on Facebook">
              <Facebook className="social-card-icon" />
              <span>Facebook</span>
            </a>
            <a href={socialLinks.youtube} target="_blank" rel="noopener noreferrer"
               className="social-card yt" aria-label="Subscribe on YouTube">
              <Youtube className="social-card-icon" />
              <span>YouTube</span>
            </a>
            <a href={socialLinks.instagram} target="_blank" rel="noopener noreferrer"
               className="social-card ig" aria-label="Follow on Instagram">
              <Instagram className="social-card-icon" />
              <span>Instagram</span>
            </a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="bottom-content">
          <div className="copyright">
            <Copyright size={13} />&nbsp;{currentYear} Gandharba Raj Paudel. All rights reserved.
          </div>
          <div className="made-with">
            Crafted with <Heart size={11} className="heart-icon" /> for a life of leadership &amp; melody.
          </div>
        </div>
      </div>
    </footer>
  );
}
