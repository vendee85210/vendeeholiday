import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Star, Quote } from 'lucide-react';

const Testimonials = () => {
  return (
    <section className="py-16 bg-gradient-to-br from-yellow-50 to-orange-50">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
          The perfect company for booking in France
        </h2>
        <p className="text-lg text-gray-600 mb-8 max-w-3xl mx-auto">
          Every year we help over 9,000 happy holiday makers find their ideal holiday homes in France. 
          See what they have to say...
        </p>

        <Card className="max-w-4xl mx-auto mb-8 border-none shadow-lg">
          <CardContent className="p-8">
            <div className="flex justify-center mb-4">
              <Quote className="w-12 h-12 text-yellow-400" />
            </div>
            <div className="flex justify-center mb-4">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-6 h-6 text-yellow-400 fill-current" />
              ))}
            </div>
            <p className="text-lg text-gray-700 italic mb-4">
              "Pure France helped us find the most incredible villa in Provence. The service was exceptional 
              and the property exceeded all our expectations. We'll definitely be booking with them again!"
            </p>
            <p className="text-sm text-gray-500">- Sarah M., London</p>
          </CardContent>
        </Card>

        <Button 
          variant="outline"
          className="border-yellow-400 text-yellow-600 hover:bg-yellow-400 hover:text-white"
        >
          Customer reviews
        </Button>
      </div>
    </section>
  );
};

export default Testimonials;