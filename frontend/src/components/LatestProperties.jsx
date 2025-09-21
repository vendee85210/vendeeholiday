import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { propertiesAPI } from '../services/api';

const LatestProperties = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const response = await propertiesAPI.getAll({ limit: 12 });
        setProperties(response.data);
      } catch (error) {
        console.error('Error fetching properties:', error);
        // Fallback to mock data if API fails
        const { properties: mockProperties } = await import('../mock/data');
        setProperties(mockProperties);
      } finally {
        setLoading(false);
      }
    };

    fetchProperties();
  }, []);

  if (loading) {
    return (
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
              What's new?
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <Card key={i} className="overflow-hidden animate-pulse">
                <div className="w-full h-48 bg-gray-300"></div>
                <CardContent className="p-4">
                  <div className="h-5 bg-gray-300 rounded mb-2"></div>
                  <div className="h-4 bg-gray-300 rounded w-2/3"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            <a href="#latest" className="text-yellow-600 hover:text-yellow-700 underline decoration-2 underline-offset-4">
              What's new?
            </a>
          </h2>
          <p className="text-lg text-gray-600 max-w-4xl mx-auto">
            We add beautiful and unique holiday accommodation with private swimming pools to our portfolio on a regular basis. 
            Here are some of our most <a href="#latest" className="text-yellow-600 hover:text-yellow-700 underline">recently added holiday rental homes</a>...
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {properties.map((property) => (
            <Card 
              key={property.id} 
              className="group overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer"
            >
              <div className="relative">
                <img 
                  src={property.images?.[0]?.url || property.image || 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&h=600&fit=crop'}
                  alt={property.name}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                {property.average_rating && (
                  <div className="absolute top-2 right-2 bg-white/90 rounded-full px-2 py-1 text-xs font-semibold">
                    ★ {property.average_rating}
                  </div>
                )}
              </div>
              <CardContent className="p-4">
                <h3 className="font-bold text-lg mb-2 text-gray-800 group-hover:text-yellow-600 transition-colors">
                  {property.name}
                </h3>
                <p className="text-sm text-gray-600 mb-1">
                  {property.bedrooms} bed {property.property_type || property.type}, {property.location?.region || property.region}
                </p>
                {property.max_guests && (
                  <p className="text-sm text-gray-500">
                    Up to {property.max_guests} guests
                  </p>
                )}
                {property.price_per_night && (
                  <p className="text-sm font-semibold text-gray-800 mt-2">
                    €{property.price_per_night}/night
                  </p>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default LatestProperties;