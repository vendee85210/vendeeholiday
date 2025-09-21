import React from 'react';
import { Card, CardContent } from './ui/card';
import { properties } from '../mock/data';

const LatestProperties = () => {
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
                  src={property.image}
                  alt={property.name}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </div>
              <CardContent className="p-4">
                <h3 className="font-bold text-lg mb-2 text-gray-800 group-hover:text-yellow-600 transition-colors">
                  {property.name}
                </h3>
                <p className="text-sm text-gray-600">
                  {property.bedrooms} bed {property.type}, {property.region}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default LatestProperties;