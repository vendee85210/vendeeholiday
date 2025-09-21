import React from 'react';
import { Facebook, Instagram, Youtube, Linkedin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-slate-800 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Pure France */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Pure France</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Home</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">About</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Contact</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Press and Media</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">List your property</a></li>
            </ul>
          </div>

          {/* Useful Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Useful Info</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">FAQ</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Travel</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Blog</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Customer reviews</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Sitemap</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Legal</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Terms of use</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Rental agreement</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Privacy policy</a></li>
              <li><a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">Cookies</a></li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Connect</h3>
            <div className="flex space-x-4 mb-4">
              <a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">
                <Youtube className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-300 hover:text-yellow-400 transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
            <div className="text-sm space-y-1">
              <p className="text-gray-300">Holiday Destinations</p>
              <p className="text-xs text-gray-400">Explore our holiday homes in France most popular destinations...</p>
            </div>
          </div>
        </div>

        {/* Bottom section */}
        <div className="border-t border-slate-700 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-sm text-gray-300">
                © Atkins & Jones Limited.
              </p>
              <p className="text-xs text-gray-400">
                Pure France™ is a registered trading name of Atkins & Jones Ltd and a registered trademark. DS1
              </p>
            </div>
            <div className="text-xs text-gray-400">
              <a href="#" className="hover:text-yellow-400 transition-colors">
                Self-catering holiday rentals with private pools in France | Pure France
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;