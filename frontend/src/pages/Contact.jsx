import React, { useState } from 'react';
import { submitContactForm } from '../services/api';
import { Mail, User, BookOpen, MessageSquare, Send, CheckCircle, AlertTriangle } from 'lucide-react';
import { Facebook, Youtube, Instagram } from '../components/SocialIcons';
import './Contact.css';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const socialLinks = {
    facebook: "https://facebook.com/dummy",
    youtube: "https://youtube.com/dummy",
    instagram: "https://instagram.com/dummy"
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await submitContactForm(formData);
      setSuccess(true);
      setFormData({ name: '', email: '', subject: '', message: '' }); // reset form
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to deliver message. Please verify backend state.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="contact-page container section">
      <h1 className="section-title font-serif">Get in Touch</h1>
      <p className="section-subtitle">
        Whether you are looking to book a corporate consultation, discuss public speaking, or ask about old cassette recording archives, drop a message below.
      </p>

      <div className="contact-grid">
        {/* Contact info card (Left side) */}
        <div className="contact-info-card glass-panel">
          <h2 className="info-title font-serif">Channel Directory</h2>
          <p className="info-intro">
            Feel free to reach out through official channels or stay updated by following these social media accounts.
          </p>

          <div className="info-channels">
            <div className="channel-item">
              <div className="channel-icon">
                <Mail size={18} />
              </div>
              <div>
                <h5>Official Email</h5>
                <p>gbigutar@gmail.com</p>
              </div>
            </div>

          
          </div>

          <div className="info-social-shelf">
            <h5>Social Handles</h5>
            <div className="social-shelf-icons">
              <a href={socialLinks.facebook} target="_blank" rel="noopener noreferrer" className="shelf-icon fb" aria-label="Facebook">
                <Facebook size={20} />
              </a>
              <a href={socialLinks.youtube} target="_blank" rel="noopener noreferrer" className="shelf-icon yt" aria-label="YouTube">
                <Youtube size={20} />
              </a>
              <a href={socialLinks.instagram} target="_blank" rel="noopener noreferrer" className="shelf-icon ig" aria-label="Instagram">
                <Instagram size={20} />
              </a>
            </div>
          </div>
        </div>

        {/* Contact form (Right side) */}
        <div className="contact-form-card glass-panel">
          {success ? (
            <div className="submit-success-view">
              <CheckCircle size={56} className="success-icon" />
              <h2 className="font-serif">Message Dispatched!</h2>
              <p>Your correspondence was uploaded successfully to the backend log. Thank you for connecting!</p>
              <button className="btn btn-corporate" onClick={() => setSuccess(false)}>
                Send Another Message
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="contact-form">
              {error && (
                <div className="form-error-alert">
                  <AlertTriangle size={18} />
                  <span>{error}</span>
                </div>
              )}

              <div className="form-group">
                <label htmlFor="name"><User size={14} /> Full Name</label>
                <input 
                  type="text" 
                  id="name" 
                  name="name" 
                  required 
                  minLength="2"
                  maxLength="100"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="e.g. John Doe"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="email"><Mail size={14} /> Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email" 
                  required 
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="e.g. john@company.com"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="subject"><BookOpen size={14} /> Subject</label>
                <input 
                  type="text" 
                  id="subject" 
                  name="subject" 
                  required 
                  minLength="2"
                  maxLength="200"
                  value={formData.subject}
                  onChange={handleChange}
                  placeholder="e.g. Corporate Inquiry / Music Collaboration"
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="message"><MessageSquare size={14} /> Message Content</label>
                <textarea 
                  id="message" 
                  name="message" 
                  required 
                  minLength="5"
                  maxLength="2000"
                  rows="5"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Write your message here..."
                  className="form-textarea"
                ></textarea>
              </div>

              <button type="submit" className="btn btn-corporate submit-btn" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner-small"></span> Sending...
                  </>
                ) : (
                  <>
                    <Send size={16} /> Send Message
                  </>
                )}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
