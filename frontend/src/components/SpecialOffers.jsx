import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Quote } from 'lucide-react';

const SpecialOffers = () => {
  return (
    <section className="py-16 bg-gradient-to-br from-yellow-50 to-orange-50">
      <div className="container mx-auto px-4 text-center">
        <Card className="max-w-4xl mx-auto border-none shadow-lg">
          <CardContent className="p-12">
            <div className="flex justify-center mb-6">
              <Quote className="w-16 h-16 text-yellow-400" />
            </div>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
              Dream Holidays, Dream Prices
            </h2>
            <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
              Discover amazing discounts and special offers on many of our fabulous properties all over France.
            </p>
            <Button 
              className="bg-yellow-400 hover:bg-yellow-500 text-slate-800 font-semibold px-8 py-3 text-lg"
            >
              Special offers
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default SpecialOffers;