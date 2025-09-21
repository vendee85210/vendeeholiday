import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { blogPosts } from '../mock/data';

const Blog = () => {
  return (
    <section id="blog" className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            <a href="#blog-full" className="text-yellow-600 hover:text-yellow-700 underline decoration-2 underline-offset-4">
              The French Lifestyle And Luxury Living Blog
            </a>
          </h2>
          <p className="text-lg text-gray-600 max-w-4xl mx-auto leading-relaxed">
            Just before Covid arrived, France retained its crown as the world's most visited country. 
            And French people's favourite country to holiday in is their own. Each region has its own individual identity; 
            its culture, geography and gastronomy. And above it all, it's the French lifestyle that we all wish to embrace. 
            In the pages within this Blog, you'll find everything that is indeed "Pure France".
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {blogPosts.map((post) => (
            <Card 
              key={post.id} 
              className="group overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer"
            >
              <div className="relative">
                <img 
                  src={post.image}
                  alt={post.title}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </div>
              <CardContent className="p-4">
                <h3 className="font-semibold text-sm leading-tight text-gray-800 group-hover:text-yellow-600 transition-colors line-clamp-3">
                  {post.title}
                </h3>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center">
          <Button 
            variant="outline"
            className="border-yellow-400 text-yellow-600 hover:bg-yellow-400 hover:text-white"
          >
            The Blog
          </Button>
        </div>
      </div>
    </section>
  );
};

export default Blog;