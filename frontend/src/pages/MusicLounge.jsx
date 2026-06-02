import React, { useState, useEffect, useRef } from 'react';
import { fetchMusicTracks } from '../services/api';
import { Play, Pause, SkipForward, SkipBack, Volume2, Music, Disc, Calendar, Clock } from 'lucide-react';
import './MusicLounge.css';

export default function MusicLounge() {
  const [tracks, setTracks] = useState([]);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const audioRef = useRef(null);
  const progressRef = useRef(null);

  // Load Tracks on Mount
  useEffect(() => {
    async function loadTracks() {
      try {
        setLoading(true);
        const data = await fetchMusicTracks();
        setTracks(data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Unable to load recordings. Make sure backend is running.");
      } finally {
        setLoading(false);
      }
    }
    loadTracks();
  }, []);

  // Update volume when state changes
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  // Handle Play/Pause Toggle
  const togglePlay = () => {
    if (!audioRef.current || tracks.length === 0) return;
    
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play().catch(err => console.log("Play interrupted:", err));
      setIsPlaying(true);
    }
  };

  // Play a specific track by index
  const playTrack = (index) => {
    if (index < 0 || index >= tracks.length) return;
    setCurrentTrackIndex(index);
    setIsPlaying(false); // Reset before load
    
    // Use timeout to let state update src, then load and play
    setTimeout(() => {
      if (audioRef.current) {
        audioRef.current.load();
        audioRef.current.play()
          .then(() => {
            setIsPlaying(true);
          })
          .catch(err => console.log("Play failed:", err));
      }
    }, 50);
  };

  const handleNext = () => {
    const nextIndex = (currentTrackIndex + 1) % tracks.length;
    playTrack(nextIndex);
  };

  const handlePrev = () => {
    const prevIndex = currentTrackIndex === 0 ? tracks.length - 1 : currentTrackIndex - 1;
    playTrack(prevIndex);
  };

  // Time Updates
  const onTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const onLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const onAudioEnded = () => {
    handleNext();
  };

  // Draggable Timeline Handler
  const handleProgressChange = (e) => {
    const newTime = parseFloat(e.target.value);
    setCurrentTime(newTime);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
    }
  };

  // Formatter for seconds to MM:SS
  const formatTime = (timeInSecs) => {
    if (isNaN(timeInSecs)) return "00:00";
    const minutes = Math.floor(timeInSecs / 60);
    const seconds = Math.floor(timeInSecs % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const currentTrack = tracks[currentTrackIndex];

  return (
    <div className="music-page container section">
      <h1 className="section-title font-serif">The Music Lounge</h1>
      <p className="section-subtitle">
        Step into the archives. Revisit raw recordings, studio demos, and live acoustic tracklists sung and recorded by BABA.
      </p>

      {loading && (
        <div className="music-loading">
          <div className="spinner"></div>
          <p>Tuning the instruments...</p>
        </div>
      )}

      {error && (
        <div className="music-error glass-panel">
          <Music size={36} className="error-icon" />
          <p>{error}</p>
          <button className="btn btn-outline" onClick={() => window.location.reload()}>
            Reload Tracks
          </button>
        </div>
      )}

      {!loading && !error && tracks.length > 0 && (
        <div className="music-grid">
          {/* Custom Audio Player Deck */}
          <div className="player-deck glass-panel pulse-glow-music">
            <div className="player-meta">
              <div className={`disc-container ${isPlaying ? 'spinning' : ''}`}>
                {currentTrack.cover_image_url ? (
                  <img src={currentTrack.cover_image_url} alt={currentTrack.title} className="disc-image" />
                ) : (
                  <Disc size={48} className="disc-fallback" />
                )}
                <div className="disc-center"></div>
              </div>
              <div className="track-details">
                <span className="now-playing-tag">Now Playing</span>
                <h2 className="player-title font-serif">{currentTrack.title}</h2>
                <div className="player-year">
                  <Calendar size={14} />
                  <span>{currentTrack.year}</span>
                </div>
                <p className="player-desc">{currentTrack.description}</p>
              </div>
            </div>

            {/* Draggable Progress Slider */}
            <div className="player-timeline">
              <span className="time-display">{formatTime(currentTime)}</span>
              <input 
                type="range" 
                min="0" 
                max={duration || 100} 
                value={currentTime} 
                onChange={handleProgressChange} 
                className="progress-slider"
                ref={progressRef}
              />
              <span className="time-display">{formatTime(duration)}</span>
            </div>

            {/* Controls Row */}
            <div className="player-controls">
              <button className="control-btn" onClick={handlePrev} aria-label="Previous Track">
                <SkipBack size={20} />
              </button>
              <button className="play-trigger-btn" onClick={togglePlay} aria-label={isPlaying ? "Pause" : "Play"}>
                {isPlaying ? <Pause size={24} /> : <Play size={24} style={{ marginLeft: '2px' }} />}
              </button>
              <button className="control-btn" onClick={handleNext} aria-label="Next Track">
                <SkipForward size={20} />
              </button>

              {/* Volume */}
              <div className="volume-control">
                <Volume2 size={16} />
                <input 
                  type="range" 
                  min="0" 
                  max="1" 
                  step="0.05" 
                  value={volume} 
                  onChange={(e) => setVolume(parseFloat(e.target.value))} 
                  className="volume-slider" 
                />
              </div>
            </div>

            {/* Invisible Audio Element */}
            <audio 
              ref={audioRef}
              src={currentTrack.audio_url}
              onTimeUpdate={onTimeUpdate}
              onLoadedMetadata={onLoadedMetadata}
              onEnded={onAudioEnded}
            />
          </div>

          {/* Ordered Tracklist Shelf */}
          <div className="track-shelf">
            <h3 className="shelf-title">Recordings Catalog ({tracks.length} tracks)</h3>
            <div className="track-list">
              {tracks.map((track, index) => (
                <div 
                  key={track.id} 
                  className={`track-item glass-panel ${index === currentTrackIndex ? 'active' : ''}`}
                  onClick={() => playTrack(index)}
                >
                  <div className="track-item-left">
                    <span className="track-number">{(index + 1).toString().padStart(2, '0')}</span>
                    <button className="track-item-play-btn">
                      {index === currentTrackIndex && isPlaying ? <Pause size={12} /> : <Play size={12} />}
                    </button>
                    <div>
                      <h4 className="track-item-title">{track.title}</h4>
                      <span className="track-item-year">{track.year}</span>
                    </div>
                  </div>

                  <div className="track-item-right">
                    {index === currentTrackIndex && isPlaying && (
                      <div className="equalizer-bar-group">
                        <div className="eq-bar"></div>
                        <div className="eq-bar"></div>
                        <div className="eq-bar"></div>
                        <div className="eq-bar"></div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
