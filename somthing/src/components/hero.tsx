import React, { Suspense, useState, useEffect } from 'react';
import Spline from '@splinetool/react-spline';

const Hero: React.FC = () => {
  const [splineLoaded, setSplineLoaded] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkDevice = () => {
      const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
      const isSmallScreen = window.innerWidth <= 1024;
      setIsMobile(isTouchDevice || isSmallScreen);
    };

    checkDevice();
    window.addEventListener('resize', checkDevice);
    window.addEventListener('orientationchange', checkDevice);
    
    return () => {
      window.removeEventListener('resize', checkDevice);
      window.removeEventListener('orientationchange', checkDevice);
    };
  }, []);

  const handleSplineLoad = () => {
    setSplineLoaded(true);
  };

  return (
    <section className="w-full min-h-screen relative bg-slate-900 overflow-hidden">
      <div className="container mx-auto px-4 h-screen">
        <div className="grid lg:grid-cols-2 h-full items-center gap-8">
          
          {/* Left Side - Text Content */}
          <div className="flex flex-col justify-center z-30 relative order-2 lg:order-1">
            <div className="max-w-lg">
              {/* Badge */}
              <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-500/20 border border-purple-500/30 text-purple-300 text-sm font-medium mb-4 backdrop-blur-sm">
                <span className="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                Welcome to the Future
              </div>

              {/* Main Heading */}
              <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold text-white leading-tight mb-4">
                Experience
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                  3D Innovation
                </span>
              </h1>

              {/* Subtitle */}
              <p className="text-base sm:text-lg lg:text-xl text-gray-300 mb-6 leading-relaxed">
                Immerse yourself in cutting-edge 3D experiences that blend creativity with technology.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-3">
                <button className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold rounded-full transition-all duration-300 shadow-lg text-sm sm:text-base">
                  Get Started
                </button>
                <button className="px-6 py-3 border-2 border-white/20 text-white hover:border-purple-400 font-semibold rounded-full transition-all duration-300 backdrop-blur-sm text-sm sm:text-base">
                  Learn More
                </button>
              </div>

              {/* Stats */}
              <div className="flex gap-6 mt-8">
                <div className="text-center">
                  <div className="text-xl sm:text-2xl font-bold text-white">50K+</div>
                  <div className="text-xs sm:text-sm text-gray-400">Users</div>
                </div>
                <div className="text-center">
                  <div className="text-xl sm:text-2xl font-bold text-white">99%</div>
                  <div className="text-xs sm:text-sm text-gray-400">Satisfaction</div>
                </div>
                <div className="text-center">
                  <div className="text-xl sm:text-2xl font-bold text-white">24/7</div>
                  <div className="text-xs sm:text-sm text-gray-400">Support</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - 3D Spline Element */}
          <div className="relative z-10 order-1 lg:order-2 h-[300px] sm:h-[400px] lg:h-[500px] xl:h-[600px]">
            <div className="w-full h-full relative rounded-xl overflow-hidden">
              
              {/* Loading State */}
              {!splineLoaded && (
                <div className="absolute inset-0 z-20 flex items-center justify-center bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-xl">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-3"></div>
                    <p className="text-purple-300 text-sm">Loading 3D...</p>
                  </div>
                </div>
              )}

              {/* Spline Container with Size Control */}
              <div 
                className="absolute inset-0 rounded-xl overflow-hidden"
                style={{
                  transform: isMobile ? 'scale(0.8)' : 'scale(1)',
                  transformOrigin: 'center center',
                }}
              >
                <Suspense fallback={null}>
                  <div className={`transition-opacity duration-1000 ${splineLoaded ? 'opacity-100' : 'opacity-0'}`}>
                    <Spline 
                      scene="https://prod.spline.design/mdVCbid2SvijRPtx/scene.splinecode"
                      onLoad={handleSplineLoad}
                      style={{
                        width: '100%',
                        height: '100%',
                        borderRadius: '12px',
                        background: 'transparent',
                      }}
                    />
                  </div>
                </Suspense>
              </div>

              {/* Subtle border effect */}
              <div className="absolute inset-0 rounded-xl ring-1 ring-white/10 pointer-events-none"></div>
            </div>
          </div>

        </div>
      </div>

      {/* Background gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900 pointer-events-none"></div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 z-30">
        <div className="w-5 h-8 border-2 border-white/30 rounded-full flex justify-center">
          <div className="w-1 h-2 bg-white/50 rounded-full mt-1"></div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
