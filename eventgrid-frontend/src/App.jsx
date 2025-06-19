import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Calendar, Users, MapPin, Zap, Star, ArrowRight, Home, Search, Settings, User } from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import AuthPage from './components/AuthPage.jsx';
import Dashboard from './components/Dashboard.jsx';
import './App.css';

// Landing Page Component
const LandingPage = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 eventgrid-gradient rounded-lg flex items-center justify-center">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-2xl font-bold eventgrid-text-gradient">EventGrid</h1>
          </Link>
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">Features</a>
            <a href="#marketplace" className="text-muted-foreground hover:text-foreground transition-colors">Marketplace</a>
            <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">Pricing</a>
            <Link to="/auth">
              <Button variant="outline" className="mr-2">Sign In</Button>
            </Link>
            <Link to="/auth">
              <Button className="eventgrid-gradient">Get Started</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="mb-4 inline-flex items-center px-4 py-2 rounded-full bg-purple-100 text-purple-700">
            <Zap className="w-4 h-4 mr-1" />
            AI-Powered Event Management
          </div>
          <h2 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Plan Events Like a
            <span className="eventgrid-text-gradient"> Pro</span>
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            EventGrid is the intelligent global event management ecosystem that connects event planners, 
            vendors, and venues worldwide. From intimate weddings to massive conferences, we make every event extraordinary.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/auth">
              <Button size="lg" className="eventgrid-gradient text-lg px-8 py-3">
                Start Planning Free
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
            <Link to="/dashboard">
              <Button size="lg" variant="outline" className="text-lg px-8 py-3">
                View Demo Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-3xl md:text-4xl font-bold mb-4">Everything You Need to Succeed</h3>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Powerful tools and intelligent features designed for modern event professionals
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature cards remain the same */}
            <div className="eventgrid-card p-6">
              <div className="w-12 h-12 eventgrid-gradient rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-xl font-semibold mb-2">AI Event Designer</h4>
              <p className="text-muted-foreground mb-4">
                Get instant theme suggestions, color palettes, and layout designs powered by AI
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Intelligent theme recommendations</li>
                <li>• Custom color palette generation</li>
                <li>• Layout optimization suggestions</li>
                <li>• Integration with design tools</li>
              </ul>
            </div>

            <div className="eventgrid-card p-6">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <Users className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-xl font-semibold mb-2">Global Marketplace</h4>
              <p className="text-muted-foreground mb-4">
                Connect with verified vendors and talent from around the world
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Verified vendor profiles</li>
                <li>• Real-time availability</li>
                <li>• Instant quote requests</li>
                <li>• Secure contract management</li>
              </ul>
            </div>

            <div className="eventgrid-card p-6">
              <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center mb-4">
                <MapPin className="w-6 h-6 text-white" />
              </div>
              <h4 className="text-xl font-semibold mb-2">AR Venue Discovery</h4>
              <p className="text-muted-foreground mb-4">
                Explore venues with immersive AR previews and virtual tours
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• 3D venue visualization</li>
                <li>• AR layout planning</li>
                <li>• Virtual walkthroughs</li>
                <li>• Capacity optimization</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-muted/30 py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 eventgrid-gradient rounded-lg flex items-center justify-center">
                  <Calendar className="w-5 h-5 text-white" />
                </div>
                <h4 className="text-lg font-bold">EventGrid</h4>
              </div>
              <p className="text-muted-foreground text-sm">
                The intelligent global event management ecosystem for modern professionals.
              </p>
            </div>
            <div>
              <h5 className="font-semibold mb-3">Product</h5>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">API</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Integrations</a></li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-3">Company</h5>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">About</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Contact</a></li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-3">Support</h5>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Community</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Status</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2025 EventGrid. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

// Navigation Component for authenticated pages
const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/events', icon: Calendar, label: 'Events' },
    { path: '/marketplace', icon: Search, label: 'Marketplace' },
    { path: '/venues', icon: MapPin, label: 'Venues' },
    { path: '/profile', icon: User, label: 'Profile' },
    { path: '/settings', icon: Settings, label: 'Settings' }
  ];

  return (
    <nav className="bg-card border-r border-border w-64 min-h-screen p-4">
      <div className="flex items-center space-x-2 mb-8">
        <div className="w-8 h-8 eventgrid-gradient rounded-lg flex items-center justify-center">
          <Calendar className="w-5 h-5 text-white" />
        </div>
        <h1 className="text-xl font-bold eventgrid-text-gradient">EventGrid</h1>
      </div>
      
      <div className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                isActive 
                  ? 'bg-primary text-primary-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

// Layout wrapper for authenticated pages
const AuthenticatedLayout = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-background">
      <Navigation />
      <main className="flex-1">
        {children}
      </main>
    </div>
  );
};

// Placeholder components for other routes
const EventsPage = () => (
  <AuthenticatedLayout>
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Events</h1>
      <p className="text-muted-foreground">Manage all your events here.</p>
    </div>
  </AuthenticatedLayout>
);

const MarketplacePage = () => (
  <AuthenticatedLayout>
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Marketplace</h1>
      <p className="text-muted-foreground">Find vendors and services for your events.</p>
    </div>
  </AuthenticatedLayout>
);

const VenuesPage = () => (
  <AuthenticatedLayout>
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Venues</h1>
      <p className="text-muted-foreground">Discover and book amazing venues.</p>
    </div>
  </AuthenticatedLayout>
);

const ProfilePage = () => (
  <AuthenticatedLayout>
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Profile</h1>
      <p className="text-muted-foreground">Manage your profile and preferences.</p>
    </div>
  </AuthenticatedLayout>
);

const SettingsPage = () => (
  <AuthenticatedLayout>
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Settings</h1>
      <p className="text-muted-foreground">Configure your account settings.</p>
    </div>
  </AuthenticatedLayout>
);

// Main App Component
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/dashboard" element={
          <AuthenticatedLayout>
            <Dashboard />
          </AuthenticatedLayout>
        } />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/venues" element={<VenuesPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Router>
  );
}

export default App;

