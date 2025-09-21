import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { destinationsAPI } from '../services/api';

const Destinations = () => {
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await destinationsAPI.getAll();
        setDestinations(response.data);
      } catch (error) {
        console.error('Error fetching destinations:', error);
        // Fallback to mock data if API fails
        const { destinations: mockDestinations } = await import('../mock/data');
        setDestinations(mockDestinations);
      } finally {
        setLoading(false);
      }
    };

    fetchDestinations();
  }, []);

  if (loading) {
    return (
      <section id="destinations" className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-gray-800">
            View our holiday homes in...
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
            {[1, 2, 3, 4].map((i) => (
              <Card key={i} className="overflow-hidden animate-pulse">
                <div className="w-full h-64 md:h-80 bg-gray-300"></div>
                <CardContent className="p-6">
                  <div className="h-6 bg-gray-300 rounded mb-2"></div>
                  <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="destinations" className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-gray-800">
          View our holiday homes in...
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-12">
          {destinations.map((destination) => (
            <Card 
              key={destination.id} 
              className="group overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer border-none"
            >
              <div className="relative">
                <img 
                  src={destination.image_url}
                  alt={destination.name}
                  className="w-full h-64 md:h-80 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                  <h3 className="text-xl md:text-2xl font-bold mb-2">
                    {destination.name}
                  </h3>
                  <p className="text-sm md:text-base opacity-90">
                    {destination.description}
                  </p>
                  {destination.property_count > 0 && (
                    <p className="text-xs mt-2 text-yellow-400">
                      {destination.property_count} properties available
                    </p>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center mt-8">
          <a 
            href="#map" 
            className="text-yellow-600 hover:text-yellow-700 font-semibold underline decoration-2 underline-offset-4"
          >
            View properties on map
          </a>
        </div>
      </div>
    </section>
  );
};

export default Destinations;