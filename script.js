// Initialize map centered on DC
const map = L.map('map').setView([38.9072, -77.0369], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Sample bar data
const bars = [
  {
    name: "Sample Bar 1",
    lat: 38.915,
    lng: -77.038,
    happyHour: "Mon–Fri 4–7 PM: $5 beers, $3 tacos"
  },
  {
    name: "Sample Bar 2",
    lat: 38.900,
    lng: -77.030,
    happyHour: "Every day 5–8 PM: 2-for-1 cocktails"
  },
  {
    name: "The Whiskey Room",
    lat: 38.912,
    lng: -77.045,
    happyHour: "Tues–Sun 6–9 PM: Half-price whiskey flights"
  }
];

// Add markers
bars.forEach(bar => {
  L.marker([bar.lat, bar.lng])
    .addTo(map)
    .bindPopup(`<strong>${bar.name}</strong><br>${bar.happyHour}`);
});