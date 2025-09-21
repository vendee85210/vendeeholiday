import React from 'react';
import { Card, CardContent } from './ui/card';
import { inspirationCategories } from '../mock/data';

const Inspiration = () => {
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
                  src={category.image}
                  alt={category.title}
                  className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
                  <h3 className="text-lg font-bold text-center">
                    {category.title}
                  </h3>
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