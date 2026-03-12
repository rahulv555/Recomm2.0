import React from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// 1. Define a custom icon for the user's location
const userIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

// 2. Helper component to handle clicks
function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click: (e) => {
      onMapClick({ lat: e.latlng.lat, lng: e.latlng.lng });
    },
  });
  return null;
}

export default function MapComponent({ onMapClick, selectedLocation, places, onMarkerClick }) {
  return (
    <div style={{ height: '100%', width: '100%', minHeight: '400px' }}> {/* CRITICAL: Explicit Height */}
      <MapContainer
        center={[23.6345, -102.5528]} // Leaflet uses [lat, lng] arrays or {lat, lng} objects
        zoom={5}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />

        {/* This component handles the click logic */}
        <MapClickHandler onMapClick={onMapClick} />

        {/* User Search Point */}
        {selectedLocation && (
          <Marker position={[selectedLocation.lat, selectedLocation.lng]} icon={userIcon} />
        )}

        {/* Restaurant Recommendations */}
        {places.map((place) => (
          <Marker
            key={place.placeID}
            position={[place.latitude, place.longitude]}
            eventHandlers={{
              click: () => onMarkerClick(place),
            }}
          />
        ))}
      </MapContainer>
    </div>
  );
}