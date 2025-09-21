import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import SpecialOffers from "./components/SpecialOffers";
import Destinations from "./components/Destinations";
import About from "./components/About";
import LatestProperties from "./components/LatestProperties";
import Inspiration from "./components/Inspiration";
import Blog from "./components/Blog";
import Testimonials from "./components/Testimonials";
import WhyBookWithUs from "./components/WhyBookWithUs";
import Footer from "./components/Footer";

const Home = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <Hero />
      <SpecialOffers />
      <Destinations />
      <About />
      <LatestProperties />
      <Inspiration />
      <Blog />
      <Testimonials />
      <WhyBookWithUs />
      <Footer />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;