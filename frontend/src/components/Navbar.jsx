import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { Facebook, Youtube, Instagram } from './SocialIcons';
import './Navbar.css';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  // Social Links
  const socialLinks = {
    facebook: "https://facebook.com/dummy",
    youtube: "https://youtube.com/dummy",
    instagram: "https://instagram.com/dummy"
  };

  return (
    <nav className="navbar-container glass-panel">
      <div className="navbar-content">
        {/* Brand / Logo */}
        <NavLink to="/" className="navbar-brand">
          <span className="brand-primary">Gandharba Raj Paudel</span>
          <span className="brand-divider">|</span>
          <span className="brand-secondary">Executive & Musician</span>
        </NavLink>

        {/* Desktop Links */}
        <div className="navbar-links">
          <NavLink to="/" end className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Home
          </NavLink>
          <NavLink to="/gallery" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Gallery
          </NavLink>
          <NavLink to="/music" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Music Lounge
          </NavLink>
          <NavLink to="/contact" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Contact
          </NavLink>
        </div>

        {/* Desktop Socials */}
        <div className="navbar-socials">
          <a href={socialLinks.facebook} target="_blank" rel="noopener noreferrer" className="social-icon fb" aria-label="Facebook">
            <Facebook size={18} />
          </a>
          <a href={socialLinks.youtube} target="_blank" rel="noopener noreferrer" className="social-icon yt" aria-label="YouTube">
            <Youtube size={18} />
          </a>
          <a href={socialLinks.instagram} target="_blank" rel="noopener noreferrer" className="social-icon ig" aria-label="Instagram">
            <Instagram size={18} />
          </a>
        </div>

        {/* Hamburger Toggle */}
        <button className="mobile-toggle" onClick={toggleMenu} aria-label="Toggle Navigation Menu">
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="mobile-menu glass-panel">
          <NavLink to="/" end className="mobile-nav-link" onClick={toggleMenu}>
            Home
          </NavLink>
          <NavLink to="/gallery" className="mobile-nav-link" onClick={toggleMenu}>
            Achievements
          </NavLink>
          <NavLink to="/music" className="mobile-nav-link" onClick={toggleMenu}>
            Music Lounge
          </NavLink>
          <NavLink to="/contact" className="mobile-nav-link" onClick={toggleMenu}>
            Contact
          </NavLink>

          <div className="mobile-socials">
            <a href={socialLinks.facebook} target="_blank" rel="noopener noreferrer" className="social-icon fb">
              <Facebook size={20} />
            </a>
            <a href={socialLinks.youtube} target="_blank" rel="noopener noreferrer" className="social-icon yt">
              <Youtube size={20} />
            </a>
            <a href={socialLinks.instagram} target="_blank" rel="noopener noreferrer" className="social-icon ig">
              <Instagram size={20} />
            </a>
          </div>
        </div>
      )}
    </nav>
  );
}
