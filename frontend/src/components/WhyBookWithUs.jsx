import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Shield, CreditCard, Clock, Users, Heart, Search } from 'lucide-react';

const WhyBookWithUs = () => {
  const features = [
    {
      icon: <Shield className="w-8 h-8 text-yellow-600" />,
      title: "Quality Assured",
      description: "All properties personally visited by our team for your peace of mind"
    },
    {
      icon: <CreditCard className="w-8 h-8 text-yellow-600" />,
      title: "No Hidden Charges",
      description: "The advertised price is the price you pay - no booking fees, cleaning charges or card fees"
    },
    {
      icon: <Clock className="w-8 h-8 text-yellow-600" />,
      title: "7 Days a Week",
      description: "Our office is open from early to late, 7 days a week to help you"
    },
    {
      icon: <Users className="w-8 h-8 text-yellow-600" />,
      title: "Expert Service",
      description: "We help you find the perfect holiday home for you and your family"
    },
    {
      icon: <Heart className="w-8 h-8 text-yellow-600" />,
      title: "Customer Loyalty",
      description: "Many customers return to us year after year and recommend us to friends and family"
    },
    {
      icon: <Search className="w-8 h-8 text-yellow-600" />,
      title: "Huge Range",
      description: "First and foremost is our huge range of quality holiday homes throughout France"
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-6">
            Why book with Pure France?
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {features.map((feature, index) => (
            <Card key={index} className="text-center p-6 hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-0">
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center bg-gray-50 p-8 rounded-lg">
          <p className="text-lg text-gray-700 mb-6 font-medium">
            So why book your French villa holiday with anyone else?
          </p>
          <div className="space-y-4 md:space-y-0 md:space-x-4 md:flex md:justify-center">
            <Button 
              className="bg-yellow-400 hover:bg-yellow-500 text-slate-800 font-semibold px-8 py-3"
            >
              Search holiday homes
            </Button>
            <div className="text-gray-600">
              <p className="text-sm">Call our reservations team on</p>
              <a href="tel:+33674048322" className="text-lg font-semibold text-yellow-600 hover:text-yellow-700">
                0033 674 048 322
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default WhyBookWithUs;