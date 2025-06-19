import React, { useState } from 'react';
import { 
  Calendar, 
  Plus, 
  Filter, 
  Search, 
  MoreHorizontal, 
  Clock, 
  Users, 
  DollarSign, 
  MapPin,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Bell
} from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Progress } from '@/components/ui/progress.jsx';

const Dashboard = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  const events = [
    {
      id: 1,
      title: "Tech Summit 2025",
      date: "2025-09-15",
      status: "planning",
      attendees: 500,
      budget: 150000,
      progress: 65,
      venue: "San Francisco Convention Center"
    },
    {
      id: 2,
      title: "Wedding - Sarah & Mike",
      date: "2025-07-20",
      status: "confirmed",
      attendees: 120,
      budget: 45000,
      progress: 90,
      venue: "Napa Valley Vineyard"
    },
    {
      id: 3,
      title: "Corporate Retreat",
      date: "2025-08-10",
      status: "draft",
      attendees: 80,
      budget: 25000,
      progress: 25,
      venue: "Lake Tahoe Resort"
    }
  ];

  const upcomingTasks = [
    { id: 1, title: "Finalize catering menu", dueDate: "2025-06-22", priority: "high", event: "Tech Summit 2025" },
    { id: 2, title: "Send invitations", dueDate: "2025-06-25", priority: "medium", event: "Wedding - Sarah & Mike" },
    { id: 3, title: "Book transportation", dueDate: "2025-06-28", priority: "low", event: "Corporate Retreat" },
    { id: 4, title: "Confirm AV equipment", dueDate: "2025-06-30", priority: "high", event: "Tech Summit 2025" }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed': return 'bg-green-500';
      case 'planning': return 'bg-blue-500';
      case 'draft': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 eventgrid-gradient rounded-lg flex items-center justify-center">
              <Calendar className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Dashboard</h1>
              <p className="text-sm text-muted-foreground">Welcome back, Sarah!</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm">
              <Bell className="w-4 h-4 mr-2" />
              Notifications
            </Button>
            <Button className="eventgrid-gradient">
              <Plus className="w-4 h-4 mr-2" />
              New Event
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Active Events</p>
                  <p className="text-3xl font-bold">12</p>
                  <p className="text-sm text-green-600 flex items-center mt-1">
                    <TrendingUp className="w-4 h-4 mr-1" />
                    +2 this month
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Calendar className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Attendees</p>
                  <p className="text-3xl font-bold">2,847</p>
                  <p className="text-sm text-green-600 flex items-center mt-1">
                    <TrendingUp className="w-4 h-4 mr-1" />
                    +15% vs last month
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Users className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Budget</p>
                  <p className="text-3xl font-bold">$1.2M</p>
                  <p className="text-sm text-blue-600 flex items-center mt-1">
                    <DollarSign className="w-4 h-4 mr-1" />
                    85% allocated
                  </p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Pending Tasks</p>
                  <p className="text-3xl font-bold">24</p>
                  <p className="text-sm text-orange-600 flex items-center mt-1">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    4 overdue
                  </p>
                </div>
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Events List */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Your Events</CardTitle>
                    <CardDescription>Manage and track your upcoming events</CardDescription>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input placeholder="Search events..." className="pl-10 w-64" />
                    </div>
                    <Button variant="outline" size="sm">
                      <Filter className="w-4 h-4 mr-2" />
                      Filter
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {events.map((event) => (
                    <div key={event.id} className="border border-border rounded-lg p-4 hover:bg-muted/50 transition-colors">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="font-semibold">{event.title}</h3>
                            <Badge className={`${getStatusColor(event.status)} text-white`}>
                              {event.status}
                            </Badge>
                          </div>
                          <div className="grid grid-cols-2 gap-4 text-sm text-muted-foreground mb-3">
                            <div className="flex items-center">
                              <Calendar className="w-4 h-4 mr-2" />
                              {new Date(event.date).toLocaleDateString()}
                            </div>
                            <div className="flex items-center">
                              <Users className="w-4 h-4 mr-2" />
                              {event.attendees} attendees
                            </div>
                            <div className="flex items-center">
                              <DollarSign className="w-4 h-4 mr-2" />
                              ${event.budget.toLocaleString()}
                            </div>
                            <div className="flex items-center">
                              <MapPin className="w-4 h-4 mr-2" />
                              {event.venue}
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-muted-foreground">Progress:</span>
                            <Progress value={event.progress} className="flex-1 max-w-32" />
                            <span className="text-sm font-medium">{event.progress}%</span>
                          </div>
                        </div>
                        <Button variant="ghost" size="sm">
                          <MoreHorizontal className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Upcoming Tasks */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Upcoming Tasks</CardTitle>
                <CardDescription>Your next priorities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {upcomingTasks.map((task) => (
                    <div key={task.id} className="border border-border rounded-lg p-3">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-medium text-sm">{task.title}</h4>
                        <Badge className={`text-xs ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground mb-2">{task.event}</p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center text-xs text-muted-foreground">
                          <Clock className="w-3 h-3 mr-1" />
                          Due {new Date(task.dueDate).toLocaleDateString()}
                        </div>
                        <Button variant="ghost" size="sm" className="h-6 px-2">
                          <CheckCircle className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
                <Button variant="outline" className="w-full mt-4">
                  View All Tasks
                </Button>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <Plus className="w-4 h-4 mr-2" />
                    Create New Event
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Search className="w-4 h-4 mr-2" />
                    Find Vendors
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <MapPin className="w-4 h-4 mr-2" />
                    Browse Venues
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Calendar className="w-4 h-4 mr-2" />
                    View Calendar
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

