const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Fetch ordered list of music tracks from backend.
 * Falls back to default tracks on backend side if DB is uninitialized.
 */
export async function fetchMusicTracks() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/music/`);
    if (!response.ok) {
      throw new Error(`Server returned status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("fetchMusicTracks error:", error);
    throw error;
  }
}

/**
 * Fetch achievements/milestones for gallery page.
 */
export async function fetchGalleryItems() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/gallery/`);
    if (!response.ok) {
      throw new Error(`Server returned status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("fetchGalleryItems error:", error);
    throw error;
  }
}

/**
 * Submit contact request form data.
 * @param {Object} data - Schema: { name, email, subject, message }
 */
export async function submitContactForm(data) {
  const response = await fetch(`${API_BASE_URL}/api/contact/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `Server returned status: ${response.status}`);
  }
  
  return await response.json();
}
