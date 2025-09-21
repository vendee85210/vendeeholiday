import React, { useState } from 'react';
import { Button } from './ui/button';
import { Search, Menu, X } from 'lucide-react';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-slate-800 text-white sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-yellow-400 rounded-md flex items-center justify-center">
                <div className="w-4 h-4 bg-slate-800 rounded-sm"></div>
              </div>
              <span className="text-xl font-bold tracking-wider">PURE FRANCE</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#destinations" className="hover:text-yellow-400 transition-colors">
              Destinations
            </a>
            <a href="#inspiration" className="hover:text-yellow-400 transition-colors">
              Inspiration
            </a>
            <a href="#blog" className="hover:text-yellow-400 transition-colors">
              Blog
            </a>
          </nav>

          {/* Right side actions */}
          <div className="hidden md:flex items-center space-x-4">
            <select className="bg-transparent border-none text-white">
              <option>English</option>
              <option>Français</option>
            </select>
            <a href="#login" className="hover:text-yellow-400 transition-colors">
              Owner Login
            </a>
            <Search className="w-5 h-5 cursor-pointer hover:text-yellow-400 transition-colors" />
            <Button variant="outline" className="bg-yellow-400 text-slate-800 border-yellow-400 hover:bg-yellow-500">
              Shortlist
            </Button>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-slate-700">
            <nav className="flex flex-col space-y-4">
              <a href="#destinations" className="hover:text-yellow-400 transition-colors">
                Destinations
              </a>
              <a href="#inspiration" className="hover:text-yellow-400 transition-colors">
                Inspiration
              </a>
              <a href="#blog" className="hover:text-yellow-400 transition-colors">
                Blog
              </a>
              <a href="#login" className="hover:text-yellow-400 transition-colors">
                Owner Login
              </a>
              <Button variant="outline" className="bg-yellow-400 text-slate-800 border-yellow-400 hover:bg-yellow-500 w-fit">
                Shortlist
              </Button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;