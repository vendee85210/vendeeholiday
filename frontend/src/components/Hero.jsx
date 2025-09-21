import React, { useState } from 'react';
import { Button } from './ui/button';
import { Calendar, Users, Search as SearchIcon } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { useToast } from '../hooks/use-toast';
import { propertiesAPI } from '../services/api';

const Hero = ({ onSearchResults }) => {
  const [searchFilters, setSearchFilters] = useState({
    region: 'All Regions',
    check_in: '',
    check_out: '',
    guests: 1
  });
  const [searching, setSearching] = useState(false);
  const { toast } = useToast();

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

  const handleSearch = async () => {
    setSearching(true);
    
    try {
      const searchParams = {
        ...(searchFilters.region !== 'All Regions' && { region: searchFilters.region }),
        ...(searchFilters.check_in && { check_in: searchFilters.check_in }),
        ...(searchFilters.check_out && { check_out: searchFilters.check_out }),
        ...(searchFilters.guests > 1 && { guests: searchFilters.guests }),
      };

      const response = await propertiesAPI.search(searchParams);
      const results = response.data;

      if (results.properties.length === 0) {
        toast({
          title: "No properties found",
          description: "Try adjusting your search criteria",
        });
      } else {
        toast({
          title: "Search completed!",
          description: `Found ${results.total_count} properties matching your criteria`,
        });
        
        // If parent component provided a callback to handle results
        if (onSearchResults) {
          onSearchResults(results);
        }
      }
    } catch (error) {
      console.error('Search error:', error);
      toast({
        title: "Search failed",
        description: "Please try again later",
        variant: "destructive"
      });
    } finally {
      setSearching(false);
    }
  };

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
                  value={searchFilters.region}
                  onChange={(e) => setSearchFilters({...searchFilters, region: e.target.value})}
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
                    value={searchFilters.check_in}
                    onChange={(e) => setSearchFilters({...searchFilters, check_in: e.target.value})}
                    min={new Date().toISOString().split('T')[0]}
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
                    value={searchFilters.check_out}
                    onChange={(e) => setSearchFilters({...searchFilters, check_out: e.target.value})}
                    min={searchFilters.check_in || new Date().toISOString().split('T')[0]}
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
                    value={searchFilters.guests}
                    onChange={(e) => setSearchFilters({...searchFilters, guests: parseInt(e.target.value)})}
                  >
                    {Array.from({ length: 20 }, (_, i) => (
                      <option key={i + 1} value={i + 1}>
                        {i === 19 ? '20+ guests' : `${i + 1} guest${i > 0 ? 's' : ''}`}
                      </option>
                    ))}
                  </select>
                  <Users className="absolute right-3 top-3 h-5 w-5 text-gray-400 pointer-events-none" />
                </div>
              </div>
            </div>

            <Button 
              className="w-full md:w-auto mt-6 bg-yellow-400 hover:bg-yellow-500 text-slate-800 font-semibold px-12 py-3"
              onClick={handleSearch}
              disabled={searching}
            >
              {searching ? (
                <>
                  <SearchIcon className="w-4 h-4 mr-2 animate-spin" />
                  Searching...
                </>
              ) : (
                'SEARCH'
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
};

export default Hero;