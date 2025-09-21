import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { contentAPI } from '../services/api';

const Inspiration = () => {
  const [inspirationCategories, setInspirationCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInspirationCategories = async () => {
      try {
        const response = await contentAPI.getInspiration();
        setInspirationCategories(response.data);
      } catch (error) {
        console.error('Error fetching inspiration categories:', error);
        // Fallback to mock data if API fails
        const { inspirationCategories: mockCategories } = await import('../mock/data');
        setInspirationCategories(mockCategories);
      } finally {
        setLoading(false);
      }
    };

    fetchInspirationCategories();
  }, []);

  if (loading) {
    return (
      <section id="inspiration" className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
              Yours to discover...
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <Card key={i} className="overflow-hidden animate-pulse">
                <div className="w-full h-64 bg-gray-300"></div>
                <CardContent className="p-4">
                  <div className="h-5 bg-gray-300 rounded"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="inspiration" className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            Yours to discover...
          </h2>
          <p className="text-lg text-gray-600 max-w-4xl mx-auto">
            Be inspired by our selections of quality villas and self-catering holiday homes with private pools in all locations and to suit all tastes...
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {inspirationCategories.map((category) => (
            <Card 
              key={category.id} 
              className="group overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer border-none"
            >
              <div className="relative">
                <img 
                  src={category.image_url || category.image}
                  alt={category.title}
                  className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
                  <h3 className="text-lg font-bold text-center">
                    {category.title}
                  </h3>
                  {category.property_count > 0 && (
                    <p className="text-xs text-center mt-2 text-yellow-400">
                      {category.property_count} properties
                    </p>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Inspiration;