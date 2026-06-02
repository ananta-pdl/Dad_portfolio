import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight, Music } from 'lucide-react';
import './Home.css';

const stats = [
  { value: '10+', label: 'Cooperative Experience' },
  { value: '4+', label: 'Albums & Recordings' },
];

export default function Home() {
  return (
    <div className="home-wrapper">

      {/* ─── Hero Section ─────────────────────────────────────────── */}
      <section className="hero-section">
        <div className="container hero-inner">
          {/* Text */}
          <div className="hero-text">
            <div className="hero-eyebrow">Loan Officer &amp; Musician</div>
            <h1 className="hero-name">Gandharba<br />Raj Paudel</h1>
            <p className="hero-tagline">
              "बिगुटारले यत्तिको मान्छे अहिलेसम्म भेट्या छैन।"
            </p>
            <div className="hero-ctas">
              <Link to="/music" className="btn btn-primary">
                <Music size={17} /> Music Lounge
              </Link>
              <Link to="/gallery" className="btn btn-outline">
                View Achievements <ChevronRight size={16} />
              </Link>
            </div>

          {/* Stats Row */}
            <div className="stats-row">
              {stats.map(s => (
                <div key={s.label} className="stat-item">
                  <span className="stat-value">{s.value}</span>
                  <span className="stat-label">{s.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Portrait */}
          <div className="hero-portrait-wrap">
            <div className="portrait-glow" />
            <img
              src="https://res.cloudinary.com/ducdlgkcq/image/upload/v1780375240/baba_pic_lmk02i.jpg"
              alt="Gandharba Raj Paudel"
              className="hero-portrait"
            />
          </div>
        </div>
      </section>

      {/* ─── About Section ───────────────────────────────────────── */}
      <section className="about-section">
        <div className="container">
          <div className="about-content">
            <h2 className="about-heading font-serif">About Gandharba Raj Paudel</h2>
            <div className="about-text">
              <p className="about-para">
                गन्धर्वराज पौडेल एक समर्पित, मेहनती तथा बहुप्रतिभाशाली व्यक्तित्व हुनुहुन्छ। उहाँ हाल NPTC मा ऋण अधिकृत (Loan Officer) को रूपमा कार्यरत हुनुहुन्छ। यस संस्थामा एक दशकभन्दा बढी समयदेखि सेवा गर्दै आउनुभएका उहाँले आफ्नो इमानदारी, जिम्मेवारीबोध तथा व्यावसायिक दक्षतामार्फत संस्थाको विकासमा महत्वपूर्ण योगदान पुर्‍याउनुभएको छ।              </p>
              <p className="about-para">
                व्यावसायिक जीवनसँगै उहाँ धार्मिक तथा सांस्कृतिक क्षेत्रमा पनि उत्तिकै सक्रिय हुनुहुन्छ। एक अनुभवी तथा श्रद्धेय पण्डितको रूपमा उहाँले विभिन्न शुभ तथा धार्मिक अवसरहरूमा पूजा, पाठ तथा धार्मिक अनुष्ठानहरू सम्पन्न गर्दै समाजमा आध्यात्मिक सेवा प्रदान गर्दै आउनुभएको छ।              </p>
              <p className="about-para">
                संगीतप्रति विशेष रुचि राख्ने उहाँ युवावस्थादेखि नै गायन क्षेत्रमा सक्रिय रहनुभएको थियो। उहाँले विभिन्न गीतहरू गाउनुभएको छ भने आफ्नै सांगीतिक एल्बमहरू समेत सार्वजनिक गर्नुभएको छ। संगीतप्रतिको उहाँको समर्पण र योगदानले उहाँलाई एक कुशल गायक तथा कलाकारको रूपमा समेत परिचित गराएको छ।              </p>
              <p className='about-para'> व्यावसायिक दक्षता, धार्मिक आस्था तथा सांगीतिक प्रतिभाको सुन्दर समन्वय बोकेका गन्धर्वराज पौडेल समाजका लागि प्रेरणादायी व्यक्तित्वका रूपमा परिचित हुनुहुन्छ।</p>
            </div>
            <div className="about-cta-row">
              <Link to="/gallery" className="btn btn-primary">
                View Achievements <ChevronRight size={16} />
              </Link>
              <Link to="/contact" className="btn btn-outline">
                Get in Touch
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Quote Section ────────────────────────────────────────── */}
      <section className="quote-section">
        <div className="container">
          <blockquote className="pull-quote">
            <span className="quote-mark">"</span>
            "पढ्नुपर्छ है नाति, नपढी त हुँदैन।"<br />
          </blockquote>
          <cite className="quote-cite">— Gandharba Raj Paudel</cite>
        </div>
      </section>

    </div>
  );
}
