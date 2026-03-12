// App.jsx
import React, { useState, useEffect } from 'react';
import { auth } from './firebase-config';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from 'firebase/auth';
import { apiCall } from './api'; // (From the previous response)
import MapComponent from './MapComponent';

// Form definition to keep JSX clean
const FORM_CONFIG = [
  { name: 'name', type: 'text', label: 'Full Name' },
  { name: 'smoker', type: 'select', options: ['true', 'false'], label: 'Smoker' },
  { name: 'drink_level', type: 'select', options: ['abstemious', 'social drinker', 'casual drinker'], label: 'Drink Level' },
  { name: 'budget', type: 'select', options: ['low', 'medium', 'high'], label: 'Budget' },
  { name: 'dress_preference', type: 'select', options: ['informal','formal', 'elegant', 'no preference'], label: 'Dress Preference' },
  { name: 'ambience', type: 'select', options: ['family', 'friends', 'solitary'], label: 'Ambience' },
  { name: 'transport', type: 'select', options: ['on foot', 'public', 'car owner'], label: 'Transport' },
  { name: 'marital_status', type: 'select', options: ['single', 'married', 'widow'], label: 'Marital Status' },
  { name: 'hijos', type: 'select', options: ['independent', 'kids', 'dependent'], label: 'Children (Hijos)' },
  { name: 'personality', type: 'select', options: ['thrifty-protector', 'hunter-ostentatious', 'hard-worker', 'conformist'], label: 'Personality' },
  { name: 'religion', type: 'select', options: ['none', 'Catholic', 'Mormon', 'Jewish', 'Christian'], label: 'Religion' },
  { name: 'interest', type: 'select', options: ['variety', 'technology','eco-friendly', 'retro','none'], label: 'Interests' },
  { name: 'activity', type: 'select', options: ['student', 'professional', 'unemployed', 'working-class'], label: 'Activity' },
  { name: 'color', type: 'select', options: ['black', 'red', 'blue', 'green', 'purple', 'orange', 'white'], label: 'Favorite Color' },
  { name: 'cuisine', type: 'multiselect', options: ['Afghan','African','American','Armenian','Asian','Australian','Austrian','Bagels','Bakery','Bar','Bar_Pub_Brewery','Barbecue','Basque','Brazilian','Breakfast-Brunch','British','Burgers','Burmese','Cafe-Coffee_Shop','Cafeteria','Cajun-Creole','California','Cambodian','Canadian','Caribbean','Chilean','Chinese','Contemporary','Continental-European','Cuban','Deli-Sandwiches','Dessert-Ice_Cream','Dim_Sum','Diner','Doughnuts','Dutch-Belgian','Eastern_European','Eclectic','Ethiopian','Family','Fast_Food','Filipino','Fine_Dining','French','Fusion','Game','German','Greek','Hawaiian','Hot_Dogs','Hungarian','Indian-Pakistani','Indigenous','Indonesian','International','Irish','Israeli','Italian','Jamaican','Japanese','Juice','Korean','Kosher','Latin_American','Lebanese','Malaysian','Mediterranean','Mexican','Middle_Eastern','Mongolian','Moroccan','North_African','Organic-Healthy','Pacific_Northwest','Pacific_Rim','Persian','Peruvian','Pizzeria','Polish','Polynesian','Portuguese','Regional','Romanian','Russian-Ukrainian','Scandinavian','Seafood','Soup','Southeast_Asian','Southern','Southwestern','Spanish','Steaks','Sushi','Swiss','Tapas','Tea_House','Tex-Mex','Thai','Tibetan','Tunisian','Turkish','Vegetarian','Vietnamese'], label: 'Cuisine Preferences' },
  { name: 'height', type: 'number', label: 'Height (m)', step: '0.01' },
  { name: 'weight', type: 'number', label: 'Weight (kg)' },
  { name: 'birth_year', type: 'number', label: 'Birth Year' },
  { name: 'age', type: 'number', label: 'Age' },
  
];

export default function App() {
  const [authUser, setAuthUser] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const [profile, setProfile] = useState(null);
  const [isProfileComplete, setIsProfileComplete] = useState(false);
  const [savingProfile, setSavingProfile] = useState(false);
  const [ratingForm, setRatingForm] = useState({ rating: 0, foodRating: 0, serviceRating: 0 });
const [isRatingSaving, setIsRatingSaving] = useState(false);

  const [recommendations, setRecommendations] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [loadingRecomms, setLoadingRecomms] = useState(false);
  const [userLocation, setUserLocation] = useState({ lat: 23.6345, lng: -102.5528 }); // Default: Center of Mexico
  const [userRatings, setUserRatings] = useState([]);
  const [loadingRatings, setLoadingRatings] = useState(false);
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      setAuthUser(user);
      if (user) await checkAndFetchProfile();
      else setProfile(null);
    });
    return unsubscribe;
  }, []);

  useEffect(() => {
    if (!profile) return setIsProfileComplete(false);
    // Ensure no null/empty strings. Arrays (cuisine) must have at least 1 item.
    const isValid = Object.entries(profile).every(([key, val]) => {
      if (Array.isArray(val)) return val.length > 0;
      return val !== "" && val !== null;
    });
    setIsProfileComplete(isValid);
  }, [profile]);

  const handleAuth = async (e, isSignUp) => {
    e.preventDefault();
    try {
      if (isSignUp) await createUserWithEmailAndPassword(auth, email, password);
      else await signInWithEmailAndPassword(auth, email, password);
    } catch (err) {
      alert("Auth Error: " + err.message);
    }
  };
  useEffect(() => {
  if (selectedRestaurant) {
    const existing = userRatings.find(r => r.placeID === selectedRestaurant.placeID);
    if (existing) {
      setRatingForm({ 
        rating: existing.rating, 
        foodRating: existing.foodrating, // match your GET response key
        serviceRating: existing.serviceRating 
      });
    } else {
      setRatingForm({ rating: 0, foodRating: 0, serviceRating: 0 });
    }
  }
}, [selectedRestaurant, userRatings]);

const handleSaveRating = async () => {
  if (!selectedRestaurant) return;
  setIsRatingSaving(true);
  try {
    
    const payload = {
      placeID: selectedRestaurant.placeID,
      rating: ratingForm.rating,
      foodRating: ratingForm.foodRating,
      serviceRating: ratingForm.serviceRating
    };
    console.log(payload);
    await apiCall('/users/rate', 'POST', payload);
    alert("Rating saved!");
    await fetchUserRatings(); // Refresh the history list
  } catch (err) {
    alert("Error saving rating: " + err.message);
  }
  setIsRatingSaving(false);
};
  const checkAndFetchProfile = async () => {
    try {
      const { userExists } = await apiCall('/users/exists');
      if (userExists) {
        const userData = await apiCall('/users');
        setProfile(userData);
        fetchUserRatings();
      } else {
        // Initialize an empty profile based on FORM_CONFIG
        const emptyProfile = FORM_CONFIG.reduce((acc, field) => {
          acc[field.name] = field.type === 'multiselect' ? [] : (field.type === 'number' ? 0 : "");
          return acc;
        }, {});
        setProfile(emptyProfile);
      }
    } catch (err) {
      console.error(err);
    }
  };
 const fetchUserRatings = async () => {
  setLoadingRatings(true);
  try {
    // 1. Fetch the user's rating history
    const ratingsData = await apiCall('/restaurant/rates', 'GET');
    
    if (ratingsData && ratingsData.length > 0) {
      // 2. Extract unique placeIDs from the ratings
      const placeIds = [...new Set(ratingsData.map(r => r.placeID))];

      // 3. Fetch full restaurant details for those IDs
      const restaurantDetails = await apiCall('/restaurant/list', 'POST', { 
        placeIDs: placeIds 
      });

      // 4. Merge the data: Add restaurant details to each rating object
      // This ensures your "Past Ratings" section has access to names and addresses
      const enrichedRatings = ratingsData.map(rating => {
        const details = restaurantDetails.find(rest => rest.placeID === rating.placeID);
        return {
          ...rating,
          // Fallback to existing name if details search fails
          name: details ? details.name : (rating.name || "Unknown Restaurant"),
          address: details ? details.address : ""
        };
      });

      setUserRatings(enrichedRatings);
    } else {
      setUserRatings([]);
    }
  } catch (err) {
    console.error("Error fetching ratings or restaurant details:", err);
  }
  setLoadingRatings(false);
};
  const handleProfileChange = (e) => {
    const { name, value, type } = e.target;
    // Keep this for standard inputs
    setProfile(prev => ({ 
      ...prev, 
      [name]: type === 'number' ? parseFloat(value) || 0 : value 
    }));
  };

  // ADD THIS specific function for cuisine
  const handleCuisineToggle = (option) => {
    setProfile(prev => {
      const currentCuisines = prev.cuisine || [];
      const updatedCuisines = currentCuisines.includes(option)
        ? currentCuisines.filter(c => c !== option) // Remove if already there
        : [...currentCuisines, option];            // Add if not there
      return { ...prev, cuisine: updatedCuisines };
    });
  };

  

  const saveProfile = async (e) => {
    e.preventDefault();

    //validating fields
    const requiredFields = [
    "name", "smoker", "drink_level", "budget", "dress_preference", 
    "ambience", "transport", "marital_status", "hijos", "personality", 
    "religion", "interest", "activity", "color", "cuisine", 
    "height", "weight", "birth_year", "age"
  ];

  const missingFields = requiredFields.filter(field => {
    const value = profile[field];
    
    // Check for empty arrays (Cuisine)
    if (Array.isArray(value)) return value.length === 0;
    
    // Check for numbers (must be greater than 0)
    if (typeof value === 'number') return value <= 0;
    
    // Check for empty strings or null/undefined
    return !value || value.toString().trim() === "";
  });

  if (missingFields.length > 0) {
    // Format field names for a nicer alert message
    const fieldList = missingFields.map(f => f.replace('_', ' ')).join(", ");
    alert(`Please fill out all fields. Missing: ${fieldList}`);
    return; // Stop execution
  }

    setSavingProfile(true);
    try {
      const { userExists } = await apiCall('/users/exists');
      await apiCall(userExists ? '/users/update' : '/users/create', userExists ? 'PATCH' : 'POST', profile);
      alert("Profile saved successfully!");
    } catch (err) {
      alert("Error saving profile: " + err.message);
    }
    setSavingProfile(false);
  };

  const getRecommendations = async (coords) => {
    setLoadingRecomms(true);
    // Hardcoding a center coordinate for Mexico City as fallback if geolocation fails
    // const defaultLat = 19.4326; 
    // const defaultLng = -99.1332;

    const fetchPlaces = async (lat, lng) => {
      try {
        print(lat, lng)
        const response = await apiCall('/recomm', 'POST', { latitude: lat, longitude: lng });

        const placeIds = response.recommendations;
        
        if (!placeIds || placeIds.length === 0) {
          setLoadingRecomms(false);
          return alert("No recommendations found.");
        }
        const restaurants = await apiCall('/restaurant/list', 'POST', { placeIDs: placeIds });
        console.log(restaurants);
        setRecommendations(restaurants);
      } catch (err) {
        alert("Error: " + err.message);
      }
      setLoadingRecomms(false);
    };

    
      fetchPlaces(coords.lat, coords.lng);
    
  };

  if (!authUser) {
    return (
      <div style={{ maxWidth: '400px', margin: '50px auto' }}>
        <h2>Login to Recommender</h2>
        <form style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
          <button onClick={(e) => handleAuth(e, false)}>Login</button>
          <button onClick={(e) => handleAuth(e, true)}>Create Account</button>
        </form>
      </div>
    );
  }

  return (
    <div style={{ padding: '40px 20px', maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <header style={{ display: 'flex', justifyContent: 'space-between' }}>
        <h1>Restaurant Recommender</h1>
        <button onClick={() => signOut(auth)}>Log Out</button>
      </header>

      {profile && (
        <section style={{ marginBottom: '40px' }}>
          <h2>Profile Setup</h2>
          <form onSubmit={saveProfile} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '25px' ,width: '100%'}}>
            {FORM_CONFIG.map(({ name, label, type, options, step }) => (
              <div key={name} style={{ display: 'flex', flexDirection: 'column' , gridColumn: type === 'multiselect' ? '1 / -1' : 'auto'}}>
                <label style={{ fontSize: '0.9rem', marginBottom: '5px' }}>{label}</label>
                
                {type === 'select' && (
                  <select name={name} value={profile[name]} onChange={handleProfileChange} required>
                    <option value="" disabled>Select...</option>
                    {options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                  </select>
                )}

                {type === 'multiselect' && (
                <div style={{ gridColumn: '1 / -1', marginTop: '10px' }}>
                  <label style={{ fontSize: '0.9rem', fontWeight: 'bold', display: 'block', marginBottom: '10px', textAlign: 'center' }}>
                    {label}
                  </label>
                  <div style={{ 
                    display: 'flex', 
                    flexWrap: 'wrap', 
                    gap: '10 px', 
                    justifyContent: 'center', // This centers the tags
                    padding: '10px',
                    border: '1px solid #eee',
                    borderRadius: '8px'
                  }}>
                    {options.map(opt => {
                      const isSelected = profile.cuisine?.includes(opt);
                      return (
                        <button
                          key={opt}
                          type="button" // Important: prevents form submission
                          onClick={() => handleCuisineToggle(opt)}
                          style={{
                            padding: '8px 16px',
                            borderRadius: '20px',
                            border: '1px solid',
                            borderColor: isSelected ? '#2563eb' : '#ccc',
                            backgroundColor: isSelected ? '#2563eb' : 'white',
                            color: isSelected ? 'white' : '#333',
                            cursor: 'pointer',
                            transition: 'all 0.2s'
                          }}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ) }

                {(type === 'text' || type === 'number') && (
                  <input type={type} name={name} step={step} value={profile[name]} onChange={handleProfileChange} required />
                )}
              </div>
            ))}
            <div style={{ gridColumn: '1 / -1', marginTop: '10px' }}>
              <button type="submit" disabled={savingProfile}>
                {savingProfile ? "Saving..." : "Save Profile"}
              </button>
            </div>
          </form>
        </section>
      )}

      <section style={{ marginBottom: '40px', width: '100%' }}>
  <h2>Your Past Ratings</h2>
  {loadingRatings ? (
    <p>Loading your history...</p>
  ) : userRatings.length > 0 ? (
    <div style={{ 
      display: 'grid', 
      gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
      gap: '15px' 
    }}>
      {userRatings.map((rate, idx) => (
        <div key={rate.placeID || idx} style={{ 
          padding: '15px', 
          border: '1px solid #eee', 
          borderRadius: '10px',
          backgroundColor: '#fafafa'
        }}>
          <h4 style={{ margin: '0 0 10px 0', color: '#2563eb'}}>{rate.name}</h4>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', color: 'black'}}>
            <span><strong>Overall:</strong> {rate.rating}</span>
            <span><strong>Food:</strong> {rate.foodrating}</span>
            <span><strong>Service:</strong> {rate.serviceRating}</span>
          </div>
        </div>
      ))}
    </div>
  ) : (
    <p style={{ fontStyle: 'italic', color: '#888' }}>You haven't rated any restaurants yet.</p>
  )}
</section>

<hr style={{ width: '100%', margin: '20px 0' }} />

      <hr />

      
      <section style={{ marginTop: '20px' }}>
  {isProfileComplete ? (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      {/* 1. Increased height to account for the <p> tag, or use min-height */}
      <div style={{ display: 'flex', gap: '20px', minHeight: '550px' }}> 
        
        {/* 2. Map Column: Use flexbox here too to stack P and Map correctly */}
        <div style={{ flex: 2, display: 'flex', flexDirection: 'column' }}>
          <p style={{ margin: '0 0 10px 0' }}>
             Click on the map to set your search location.
          </p>
          
          {/* 3. Wrap Map in a div that takes the REMAINING space */}
          <div style={{ flex: 1, position: 'relative', border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden' }}>
            <MapComponent 
              places={recommendations} 
              onMarkerClick={setSelectedRestaurant}
              onMapClick={(coords) => setUserLocation(coords)} 
              selectedLocation={userLocation}
              center={{ lat: 23.6345, lng: -102.5528 }} 
            />
          </div>
        </div>

        {/* Sidebar */}
        <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '8px', overflowY: 'auto', height: '100%' }}>
  {selectedRestaurant ? (
    <>
      <div style={{ borderBottom: '2px solid #eee', marginBottom: '15px', paddingBottom: '10px' }}>
        <h3>{selectedRestaurant.name}</h3>
        <p style={{fontSize: '0.85rem', color: '#666'}}>{selectedRestaurant.address}</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.9rem' }}>
        <p><strong>Place id:</strong> {selectedRestaurant.placeID}</p>
        <p><strong>Cuisine:</strong> {selectedRestaurant.rcuisine?.join(', ')}</p>
        <p><strong>Alcohol:</strong> {selectedRestaurant.alcohol?.replace(/_/g,' ')}</p>
        <p><strong>Dress code:</strong> {selectedRestaurant.dress_code}</p>
         <p><strong>Smoking Area:</strong> {selectedRestaurant.smoking_area}</p>

              <p><strong>Parking:</strong> {selectedRestaurant.parking_lot}</p>
      </div>

      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
        <h4 style={{ marginTop: 0 }}>{userRatings.some(r => r.placeID === selectedRestaurant.placeID) ? "Your Rating" : "Rate this Place"}</h4>
        
        {['rating', 'foodRating', 'serviceRating'].map((field) => (
          <div key={field} style={{ marginBottom: '10px' }}>
            <label style={{ display: 'block', fontSize: '0.8rem', textTransform: 'capitalize',  color:'black'}}>
              {field.replace('Rating', ' Rating')}: {ratingForm[field]}
            </label>
            <input 
              type="range" min="0" max="5" step="0.5" 
              value={ratingForm[field]} 
              onChange={(e) => setRatingForm({...ratingForm, [field]: parseFloat(e.target.value)})}
              style={{ width: '100%' }}
            />
          </div>
        ))}

        <button 
          onClick={handleSaveRating} 
          disabled={isRatingSaving}
          style={{ 
            width: '100%', 
            padding: '10px', 
            marginTop: '10px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: isRatingSaving ? 'not-allowed' : 'pointer'
          }}
        >
          {isRatingSaving ? "Saving..." : "Save Rating"}
        </button>
      </div>
    </>
  ) : (
    <p>{recommendations.length > 0 ? "Click a marker to see details." : "Select a location on the map to begin."}</p>
  )}
</div>
      </div>

      <button 
        onClick={() => getRecommendations(userLocation)} 
        disabled={loadingRecomms}
        style={{ 
          padding: '15px 20px', 
          fontSize: '1.1rem', 
          backgroundColor: '#4CAF50', 
          color: 'white',
          cursor: loadingRecomms ? 'not-allowed' : 'pointer',
          borderRadius: '5px',
          border: 'none',
          zIndex: 10 // Ensures button stays on top if anything drifts
        }}
      >
        {loadingRecomms ? "Analyzing..." : `Get Recommendations near this spot`}
      </button>
    </div>
  ) : (
    <p style={{ color: 'red', fontSize: '0.9rem' }}>Fill out and save all profile fields to unlock the map and recommendations.</p>
  )}
</section>
    </div>
  );
}