import React from 'react';
import { Card, CardContent } from './ui/card';

const About = () => {
  const pressLogos = [
    { name: "The Sunday Times", logo: "ST" },
    { name: "The Telegraph", logo: "T" },
    { name: "The Guardian", logo: "G" },
    { name: "Conde Nast Traveller", logo: "CN" }
  ];

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Pure France</h2>
            <h3 className="text-xl text-gray-600 mb-6">
              The specialists for quality holiday villas and châteaux with pools in France.
            </h3>
          </div>

          <div className="prose prose-lg mx-auto text-gray-700 leading-relaxed">
            <p className="mb-6">
              We have been offering a superb range of self-catering holiday accommodation in France for over 23 years. 
              We are passionate about France and the diversity of its culture, geography and beautiful holiday homes that we are proud to offer you.
            </p>
            
            <p className="mb-6">
              Whatever you are searching for, you will find it in our listings; family villas with pools, châteaux holidays, 
              luxurious beachfront villas, country homes and traditional farmhouses.
            </p>

            <div className="bg-white p-6 rounded-lg mb-8">
              <h4 className="font-bold text-lg mb-4">Where to stay?</h4>
              <p className="mb-4">
                France is a wonderfully diverse country, as well as being the most-visited country by holiday-makers every year.
              </p>
              <p>
                A holiday in France can take you to rolling countryside of Burgundy and the Dordogne, the historical châteaux of the Loire Valley, 
                the vineyards and expansive coastline of Occitanie. And Provence... well, everyone knows Provence for its lavender fields, 
                pretty villages and the Côte d'Azur.
              </p>
            </div>

            <p className="text-center mb-8">
              Arranging your villa holiday in France has never been easier or more accessible with our huge choice of villas with private pools, 
              self-catering accommodation and very special family holiday homes.
            </p>
          </div>

          {/* Press Logos */}
          <div className="text-center">
            <p className="text-sm text-gray-500 mb-4">As featured in...</p>
            <div className="flex justify-center items-center space-x-6 md:space-x-12">
              {pressLogos.map((press) => (
                <div key={press.name} className="text-center">
                  <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center text-xs font-bold text-gray-600 mb-1">
                    {press.logo}
                  </div>
                  <span className="text-xs text-gray-500 hidden md:block">{press.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;