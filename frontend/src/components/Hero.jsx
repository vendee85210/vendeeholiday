import React, { useState } from 'react';
import { Button } from './ui/button';
import { Calendar, Users } from 'lucide-react';
import { Card, CardContent } from './ui/card';

const Hero = () => {
  const [selectedRegion, setSelectedRegion] = useState('All Regions');
  const [selectedGuests, setSelectedGuests] = useState('1 guest');
  const [checkIn, setCheckIn] = useState('');
  const [checkOut, setCheckOut] = useState('');

  const regions = [
    'All Regions',
    'Loire, Vendée and Brittany',
    'Burgundy',
    'Dordogne and South-West',
    'Occitanie (inc. Languedoc)',
    'Provence',
    'Côte d\'Azur and Riviera',
    'Island of Corsica'
  ];

  const guestOptions = Array.from({ length: 20 }, (_, i) => 
    i === 19 ? '20+ guests' : `${i + 1} guest${i > 0 ? 's' : ''}`
  );

  return (
    <section className="relative h-screen flex items-center justify-center">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1920&h=1080&fit=crop')"
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 text-center text-white">
        <h1 className="text-4xl md:text-6xl font-bold mb-4">
          Find your perfect French holiday home
        </h1>
        <p className="text-xl md:text-2xl mb-8 font-light">
          Holiday villas and rental châteaux throughout France
        </p>

        {/* Search Form */}
        <Card className="max-w-4xl mx-auto bg-white/95 backdrop-blur-sm">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
              {/* Region Selector */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Region</label>
                <select 
                  className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-gray-900"
                  value={selectedRegion}
                  onChange={(e) => setSelectedRegion(e.target.value)}
                >
                  {regions.map((region) => (
                    <option key={region} value={region}>{region}</option>
                  ))}
                </select>
              </div>

              {/* Check-in Date */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Check in</label>
                <div className="relative">
                  <input
                    type="date"
                    className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-gray-900"
                    value={checkIn}
                    onChange={(e) => setCheckIn(e.target.value)}
                  />
                  <Calendar className="absolute right-3 top-3 h-5 w-5 text-gray-400 pointer-events-none" />
                </div>
              </div>

              {/* Check-out Date */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Check out</label>
                <div className="relative">
                  <input
                    type="date"
                    className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-gray-900"
                    value={checkOut}
                    onChange={(e) => setCheckOut(e.target.value)}
                  />
                  <Calendar className="absolute right-3 top-3 h-5 w-5 text-gray-400 pointer-events-none" />
                </div>
              </div>

              {/* Guests */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Guests</label>
                <div className="relative">
                  <select 
                    className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-gray-900"
                    value={selectedGuests}
                    onChange={(e) => setSelectedGuests(e.target.value)}
                  >
                    {guestOptions.map((option) => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                  <Users className="absolute right-3 top-3 h-5 w-5 text-gray-400 pointer-events-none" />
                </div>
              </div>
            </div>

            <Button className="w-full md:w-auto mt-6 bg-yellow-400 hover:bg-yellow-500 text-slate-800 font-semibold px-12 py-3">
              SEARCH
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default Hero;