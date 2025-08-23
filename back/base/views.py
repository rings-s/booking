# base/views.py
from rest_framework import viewsets, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied  # FIX: Added missing import
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg, Q, F, Min, Max
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, date

# Make pandas optional for now
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Make plotly imports optional to avoid dependency issues
try:
    import plotly.graph_objs as go
    import plotly.io as pio
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from .models import (
    Business, BusinessHours, Service, Customer,
    Booking, Review, Notification
)
from .serializers import (
    BusinessSerializer, BusinessHoursSerializer,
    ServiceSerializer, CustomerSerializer,
    BookingSerializer, ReviewSerializer,
    NotificationSerializer, DashboardSerializer
)
from accounts.permissions import (
    IsBusinessOwner, HasActiveSubscription,
    CanCreateBooking
)
from .utils import calculate_available_slots, send_booking_reminder, get_available_dates


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business model with dashboard analytics and charts
    """
    queryset = Business.objects.filter(is_active=True)
    serializer_class = BusinessSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'city', 'state', 'accepts_online_bookings']
    search_fields = ['name', 'description', 'category', 'city']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions required
        """
        if self.action in ['list', 'retrieve', 'available_slots', 'search', 'featured']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsBusinessOwner, HasActiveSubscription]
        elif self.action in ['update', 'partial_update', 'destroy', 'dashboard', 
                           'analytics_chart', 'revenue_report', 'update_hours']:
            permission_classes = [IsAuthenticated, IsBusinessOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set the owner to the current user when creating a business"""
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def dashboard(self, request, slug=None):
        """
        Get comprehensive dashboard data for business owner
        """
        business = self.get_object()
        
        # Verify ownership or admin access
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to view this dashboard'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Date ranges
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        last_90_days = today - timedelta(days=90)
        last_year = today - timedelta(days=365)
        
        # Get bookings for different periods
        bookings_30 = Booking.objects.filter(
            business=business,
            booking_date__gte=last_30_days
        )
        bookings_90 = Booking.objects.filter(
            business=business,
            booking_date__gte=last_90_days
        )
        
        # Calculate metrics
        dashboard_data = {
            # Overview metrics
            'total_bookings': bookings_30.count(),
            'total_revenue': float(
                bookings_30.filter(is_paid=True).aggregate(
                    total=Sum('total_price')
                )['total'] or 0
            ),
            'total_customers': Customer.objects.filter(
                bookings__business=business,
                bookings__booking_date__gte=last_30_days
            ).distinct().count(),
            'average_rating': float(
                business.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
            ),
            
            # Comparison with previous period
            'bookings_growth': self._calculate_growth(business, 'bookings'),
            'revenue_growth': self._calculate_growth(business, 'revenue'),
            
            # Time series data
            'bookings_by_date': self._get_bookings_by_date(bookings_30),
            'revenue_by_month': self._get_revenue_by_month(business),
            'bookings_by_hour': self._get_bookings_by_hour(bookings_90),
            'bookings_by_weekday': self._get_bookings_by_weekday(bookings_90),
            
            # Service analytics
            'popular_services': self._get_popular_services(business, last_30_days),
            'service_revenue': self._get_service_revenue(business, last_30_days),
            
            # Customer analytics
            'customer_demographics': self._get_customer_demographics(business),
            'top_customers': self._get_top_customers(business, last_90_days),
            'customer_retention': self._calculate_retention_rate(business),
            
            # Recent activity
            'recent_bookings': BookingSerializer(
                bookings_30.order_by('-created_at')[:10],
                many=True
            ).data,
            'recent_reviews': ReviewSerializer(
                business.reviews.order_by('-created_at')[:5],
                many=True
            ).data,
            
            # Status breakdown
            'booking_status_breakdown': self._get_booking_status_breakdown(bookings_30),
            
            # Forecast
            'next_week_bookings': self._get_upcoming_bookings(business),
        }
        
        serializer = DashboardSerializer(dashboard_data)
        return Response(serializer.data)
    
    def _calculate_growth(self, business, metric_type):
        """Calculate growth percentage compared to previous period"""
        today = timezone.now().date()
        current_start = today - timedelta(days=30)
        current_end = today
        previous_start = today - timedelta(days=60)
        previous_end = today - timedelta(days=30)
        
        if metric_type == 'bookings':
            current = Booking.objects.filter(
                business=business,
                booking_date__range=[current_start, current_end]
            ).count()
            previous = Booking.objects.filter(
                business=business,
                booking_date__range=[previous_start, previous_end]
            ).count()
        else:  # revenue
            current = Booking.objects.filter(
                business=business,
                booking_date__range=[current_start, current_end],
                is_paid=True
            ).aggregate(Sum('total_price'))['total_price__sum'] or 0
            previous = Booking.objects.filter(
                business=business,
                booking_date__range=[previous_start, previous_end],
                is_paid=True
            ).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / previous) * 100, 2)
    
    def _get_bookings_by_date(self, bookings):
        """Get bookings grouped by date"""
        data = bookings.values('booking_date').annotate(
            count=Count('id'),
            revenue=Sum('total_price', filter=Q(is_paid=True, status__in=['confirmed', 'completed']))
        ).order_by('booking_date')
        
        return [
            {
                'date': item['booking_date'].isoformat(),
                'bookings': item['count'],
                'revenue': float(item['revenue'] or 0)
            }
            for item in data
        ]
    
    def _get_revenue_by_month(self, business):
        """Get revenue for last 12 months"""
        today = timezone.now().date()
        months_data = []
        
        for i in range(12):
            month_end = today.replace(day=1) - timedelta(days=i * 30)
            month_start = month_end - timedelta(days=30)
            
            revenue = Booking.objects.filter(
                business=business,
                booking_date__range=[month_start, month_end],
                is_paid=True,
                status__in=['confirmed', 'completed']
            ).aggregate(Sum('total_price'))['total_price__sum'] or 0
            
            months_data.append({
                'month': month_end.strftime('%B %Y'),
                'revenue': float(revenue)
            })
        
        return list(reversed(months_data))
    
    def _get_bookings_by_hour(self, bookings):
        """Analyze booking patterns by hour of day"""
        hour_data = {}
        for booking in bookings:
            hour = booking.start_time.hour
            if hour not in hour_data:
                hour_data[hour] = 0
            hour_data[hour] += 1
        
        return [
            {'hour': hour, 'count': count}
            for hour, count in sorted(hour_data.items())
        ]
    
    def _get_bookings_by_weekday(self, bookings):
        """Analyze booking patterns by day of week"""
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday']
        weekday_data = {i: 0 for i in range(7)}
        
        for booking in bookings:
            weekday = booking.booking_date.weekday()
            weekday_data[weekday] += 1
        
        return [
            {'weekday': weekday_names[day], 'count': count}
            for day, count in weekday_data.items()
        ]
    
    def _get_popular_services(self, business, start_date):
        """Get most popular services by booking count"""
        services = Service.objects.filter(business=business).annotate(
            booking_count=Count(
                'bookings',
                filter=Q(bookings__booking_date__gte=start_date)
            ),
            total_revenue=Sum(
                'bookings__total_price',
                filter=Q(
                    bookings__booking_date__gte=start_date,
                    bookings__is_paid=True
                )
            )
        ).order_by('-booking_count')[:5]
        
        return [
            {
                'id': str(service.id),
                'name': service.name,
                'bookings': service.booking_count,
                'revenue': float(service.total_revenue or 0),
                'average_price': float(service.price)
            }
            for service in services
        ]
    
    def _get_service_revenue(self, business, start_date):
        """Get revenue breakdown by service"""
        services = Service.objects.filter(business=business).annotate(
            revenue=Sum(
                'bookings__total_price',
                filter=Q(
                    bookings__booking_date__gte=start_date,
                    bookings__is_paid=True
                )
            )
        ).exclude(revenue=None).order_by('-revenue')
        
        return [
            {
                'service': service.name,
                'revenue': float(service.revenue),
                'percentage': 0  # Calculate after getting total
            }
            for service in services
        ]
    
    def _get_customer_demographics(self, business):
        """Analyze customer demographics"""
        customers = Customer.objects.filter(
            bookings__business=business
        ).distinct()
        
        new_customers = customers.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        returning_customers = customers.annotate(
            booking_count=Count('bookings')
        ).filter(booking_count__gt=1).count()
        
        return {
            'total': customers.count(),
            'new_this_month': new_customers,
            'returning': returning_customers,
            'retention_rate': round(
                (returning_customers / customers.count() * 100) if customers.count() > 0 else 0,
                2
            )
        }
    
    def _get_top_customers(self, business, start_date):
        """Get top customers by booking frequency and spending"""
        customers = Customer.objects.filter(
            bookings__business=business,
            bookings__booking_date__gte=start_date
        ).annotate(
            booking_count=Count('bookings'),
            calculated_spent=Sum(
                'bookings__total_price',
                filter=Q(bookings__is_paid=True)
            )
        ).order_by('-calculated_spent')[:10]
        
        return [
            {
                'id': str(customer.id),
                'name': customer.user.full_name,
                'email': customer.user.email,
                'bookings': customer.booking_count,
                'total_spent': float(customer.calculated_spent or 0)
            }
            for customer in customers
        ]
    
    def _calculate_retention_rate(self, business):
        """Calculate customer retention rate"""
        today = timezone.now().date()
        
        # Customers from 60-90 days ago
        old_customers = Customer.objects.filter(
            bookings__business=business,
            bookings__booking_date__range=[today - timedelta(days=90), today - timedelta(days=60)]
        ).distinct()
        
        # How many of them booked again in last 30 days
        retained = old_customers.filter(
            bookings__business=business,
            bookings__booking_date__gte=today - timedelta(days=30)
        ).distinct().count()
        
        total = old_customers.count()
        
        return {
            'rate': round((retained / total * 100) if total > 0 else 0, 2),
            'retained': retained,
            'total': total
        }
    
    def _get_booking_status_breakdown(self, bookings):
        """Get breakdown of bookings by status"""
        status_data = bookings.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        return [
            {
                'status': item['status'],
                'count': item['count']
            }
            for item in status_data
        ]
    
    def _get_upcoming_bookings(self, business):
        """Get upcoming bookings for next 7 days"""
        today = timezone.now().date()
        next_week = today + timedelta(days=7)
        
        upcoming = Booking.objects.filter(
            business=business,
            booking_date__range=[today, next_week],
            status__in=['confirmed', 'pending']
        ).count()
        
        return upcoming
    
    @action(detail=True, methods=['get'])
    def analytics_chart(self, request, slug=None):
        """
        Generate interactive Plotly charts for business analytics
        """
        if not PLOTLY_AVAILABLE:
            return Response(
                {'error': 'Plotly is not installed. Please install plotly to use charts.'},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
            
        business = self.get_object()
        chart_type = request.query_params.get('type', 'bookings')
        period = request.query_params.get('period', '30')
        
        try:
            period_days = int(period)
        except ValueError:
            period_days = 30
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=period_days)
        
        if chart_type == 'bookings':
            chart_html = self._generate_bookings_chart(business, start_date, end_date)
        elif chart_type == 'revenue':
            chart_html = self._generate_revenue_chart(business, start_date, end_date)
        elif chart_type == 'services':
            chart_html = self._generate_services_chart(business, start_date, end_date)
        elif chart_type == 'customers':
            chart_html = self._generate_customers_chart(business, start_date, end_date)
        elif chart_type == 'heatmap':
            chart_html = self._generate_booking_heatmap(business, start_date, end_date)
        else:
            return Response(
                {'error': 'Invalid chart type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({'chart': chart_html})
    
    def _generate_bookings_chart(self, business, start_date, end_date):
        """Generate bookings over time chart"""
        bookings = Booking.objects.filter(
            business=business,
            booking_date__range=[start_date, end_date]
        ).values('booking_date').annotate(
            count=Count('id')
        ).order_by('booking_date')
        
        df = pd.DataFrame(bookings)
        if df.empty:
            df = pd.DataFrame({'booking_date': [start_date], 'count': [0]})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['booking_date'],
            y=df['count'],
            mode='lines+markers',
            name='Bookings',
            line=dict(color='#4CAF50', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Bookings Over Time',
            xaxis_title='Date',
            yaxis_title='Number of Bookings',
            hovermode='x unified',
            showlegend=False,
            template='plotly_white'
        )
        
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="bookings-chart")
    
    def _generate_revenue_chart(self, business, start_date, end_date):
        """Generate revenue over time chart"""
        revenue_data = Booking.objects.filter(
            business=business,
            booking_date__range=[start_date, end_date],
            is_paid=True
        ).values('booking_date').annotate(
            revenue=Sum('total_price')
        ).order_by('booking_date')
        
        df = pd.DataFrame(revenue_data)
        if df.empty:
            df = pd.DataFrame({'booking_date': [start_date], 'revenue': [0]})
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['booking_date'],
            y=df['revenue'],
            name='Revenue',
            marker_color='#2196F3'
        ))
        
        fig.update_layout(
            title='Revenue Over Time',
            xaxis_title='Date',
            yaxis_title='Revenue ($)',
            hovermode='x unified',
            showlegend=False,
            template='plotly_white'
        )
        
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="revenue-chart")
    
    def _generate_services_chart(self, business, start_date, end_date):
        """Generate service popularity pie chart"""
        services = Service.objects.filter(business=business).annotate(
            booking_count=Count(
                'bookings',
                filter=Q(
                    bookings__booking_date__range=[start_date, end_date]
                )
            )
        ).exclude(booking_count=0)
        
        labels = [s.name for s in services]
        values = [s.booking_count for s in services]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3
        )])
        
        fig.update_layout(
            title='Service Distribution',
            template='plotly_white'
        )
        
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="services-chart")
    
    def _generate_customers_chart(self, business, start_date, end_date):
        """Generate new vs returning customers chart"""
        customers = Customer.objects.filter(
            bookings__business=business,
            bookings__booking_date__range=[start_date, end_date]
        ).distinct()
        
        new_customers = customers.filter(
            created_at__gte=start_date
        ).count()
        
        returning_customers = customers.filter(
            created_at__lt=start_date
        ).count()
        
        fig = go.Figure(data=[
            go.Bar(name='New', x=['Customers'], y=[new_customers]),
            go.Bar(name='Returning', x=['Customers'], y=[returning_customers])
        ])
        
        fig.update_layout(
            title='New vs Returning Customers',
            barmode='stack',
            template='plotly_white'
        )
        
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="customers-chart")
    
    def _generate_booking_heatmap(self, business, start_date, end_date):
        """Generate booking heatmap by day and hour"""
        bookings = Booking.objects.filter(
            business=business,
            booking_date__range=[start_date, end_date]
        )
        
        # Create matrix for heatmap
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = list(range(24))
        matrix = [[0 for _ in hours] for _ in days]
        
        for booking in bookings:
            day_idx = booking.booking_date.weekday()
            hour = booking.start_time.hour
            matrix[day_idx][hour] += 1
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=[f"{h:02d}:00" for h in hours],
            y=days,
            colorscale='Viridis'
        ))
        
        fig.update_layout(
            title='Booking Heatmap',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            template='plotly_white'
        )
        
        return pio.to_html(fig, include_plotlyjs='cdn', div_id="heatmap-chart")
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, slug=None):
        """
        Get available booking slots for a specific date and service
        """
        business = self.get_object()
        service_id = request.query_params.get('service')
        date_str = request.query_params.get('date')
        
        if not service_id or not date_str:
            return Response(
                {'error': 'service and date parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = Service.objects.get(id=service_id, business=business)
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (Service.DoesNotExist, ValueError):
            return Response(
                {'error': 'Invalid service or date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Don't allow booking in the past
        if booking_date < timezone.now().date():
            return Response(
                {'error': 'Cannot book for past dates'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        available_slots = calculate_available_slots(business, service, booking_date)
        
        return Response({
            'date': booking_date.isoformat(),
            'service': service.name,
            'slots': available_slots
        })
    
    @action(detail=True, methods=['get'])
    def available_dates(self, request, slug=None):
        """
        Get available dates for a specific service
        """
        business = self.get_object()
        service_id = request.query_params.get('service')
        days_ahead = int(request.query_params.get('days_ahead', 90))
        
        if not service_id:
            return Response(
                {'error': 'service parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = Service.objects.get(id=service_id, business=business, is_active=True)
        except Service.DoesNotExist:
            return Response(
                {'error': 'Service not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        available_dates = get_available_dates(business, service, days_ahead=days_ahead)
        
        return Response({
            'business': business.name,
            'service': service.name,
            'available_dates': available_dates,
            'total_dates': len(available_dates)
        })
    
    # FIX: Removed duplicate stats method - keeping only one
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def stats(self, request, slug=None):
        """Get business statistics"""
        business = self.get_object()
        period = request.query_params.get('period', 'month')
        
        # Check if user owns this business
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculate date range
        now = timezone.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        elif period == 'quarter':
            start_date = now - timedelta(days=90)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(days=30)
        
        # Get stats
        bookings = Booking.objects.filter(business=business, created_at__gte=start_date)
        total_revenue = bookings.filter(status__in=['confirmed', 'completed'], is_paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_bookings = bookings.count()
        confirmed_bookings = bookings.filter(status__in=['confirmed', 'completed']).count()
        customers = Customer.objects.filter(bookings__business=business).distinct().count()
        reviews = Review.objects.filter(business=business)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Calculate changes from previous period
        prev_start = start_date - (now - start_date)
        prev_bookings = Booking.objects.filter(
            business=business,
            created_at__gte=prev_start,
            created_at__lt=start_date
        )
        
        prev_revenue = prev_bookings.filter(status__in=['confirmed', 'completed'], is_paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        prev_bookings_count = prev_bookings.count()
        prev_customers = Customer.objects.filter(
            bookings__business=business,
            bookings__created_at__gte=prev_start,
            bookings__created_at__lt=start_date
        ).distinct().count()
        
        # Calculate percentage changes
        revenue_change = ((float(total_revenue) - float(prev_revenue)) / max(float(prev_revenue), 1)) * 100 if prev_revenue else 0
        bookings_change = ((total_bookings - prev_bookings_count) / max(prev_bookings_count, 1)) * 100 if prev_bookings_count else 0
        customers_change = ((customers - prev_customers) / max(prev_customers, 1)) * 100 if prev_customers else 0
        
        return Response({
            'revenue': float(total_revenue),
            'bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'customers': customers,
            'rating': round(avg_rating, 1),
            'revenueChange': round(revenue_change, 1),
            'bookingsChange': round(bookings_change, 1),
            'customersChange': round(customers_change, 1),
            'ratingChange': 0  # Would need historical rating data
        })
    
    # FIX: Removed duplicate revenue_data method - keeping the one with better implementation
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def revenue_data(self, request, slug=None):
        """Get revenue data for charts"""
        business = self.get_object()
        period = request.query_params.get('period', 'month')
        
        # Check if user owns this business
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculate date range
        now = timezone.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=30)
        
        # Get daily revenue data
        revenue_data = []
        current_date = start_date.date()
        end_date = now.date()
        
        while current_date <= end_date:
            daily_revenue = Booking.objects.filter(
                business=business,
                booking_date=current_date,
                status__in=['confirmed', 'completed'],
                is_paid=True
            ).aggregate(Sum('total_price'))['total_price__sum'] or 0
            
            revenue_data.append({
                'date': current_date.isoformat(),
                'revenue': float(daily_revenue)
            })
            current_date += timedelta(days=1)
        
        return Response(revenue_data)
    
    # FIX: Removed duplicate service_stats method - keeping one implementation
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def service_stats(self, request, slug=None):
        """Get service statistics"""
        business = self.get_object()
        
        # Check if user owns this business
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        services_data = Service.objects.filter(business=business).annotate(
            booking_count=Count('bookings'),
            total_revenue=Sum('bookings__total_price', filter=Q(bookings__status__in=['confirmed', 'completed'], bookings__is_paid=True))
        ).values('name', 'booking_count', 'total_revenue', 'price')
        
        return Response(list(services_data))
    
    # FIX: Removed duplicate recent_activity method - keeping one implementation
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def recent_activity(self, request, slug=None):
        """Get recent business activity"""
        business = self.get_object()
        
        # Check if user owns this business
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get recent bookings
        recent_bookings = Booking.objects.filter(business=business).order_by('-created_at')[:10]
        activities = []
        
        for booking in recent_bookings:
            activities.append({
                'type': 'booking',
                'title': f'New booking for {booking.service.name}',
                'description': f'Customer: {booking.customer.user.full_name}',
                'date': booking.created_at.isoformat(),
                'status': booking.status
            })
        
        # Get recent reviews
        recent_reviews = Review.objects.filter(
            business=business
        ).select_related('customer__user').order_by('-created_at')[:5]
        
        for review in recent_reviews:
            customer_name = f"{review.customer.user.first_name} {review.customer.user.last_name}".strip()
            if not customer_name:
                customer_name = review.customer.user.email or "Unknown Customer"
            
            activities.append({
                'id': str(review.id),
                'type': 'review',
                'title': f'New {review.rating}-star review',
                'description': f'{customer_name} left a review',
                'date': review.created_at.isoformat(),
                'rating': review.rating
            })
        
        # Sort by date
        activities.sort(key=lambda x: x['date'], reverse=True)
        
        return Response(activities[:15])
    
    @action(detail=True, methods=['post'])
    def update_hours(self, request, slug=None):
        """
        Update business hours
        """
        business = self.get_object()
        
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to update business hours'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        hours_data = request.data.get('hours', [])
        
        for hour_data in hours_data:
            weekday = hour_data.get('weekday')
            if weekday is None:
                continue
            
            BusinessHours.objects.update_or_create(
                business=business,
                weekday=weekday,
                defaults={
                    'opening_time': hour_data.get('opening_time'),
                    'closing_time': hour_data.get('closing_time'),
                    'is_closed': hour_data.get('is_closed', False)
                }
            )
        
        return Response({'status': 'Business hours updated successfully'})
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search for businesses with filters
        """
        queryset = self.get_queryset()
        
        # Search query
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__icontains=search) |
                Q(city__icontains=search)
            )
        
        # Category filter
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        # Location filter
        location = request.query_params.get('location')
        if location:
            queryset = queryset.filter(
                Q(city__icontains=location) |
                Q(state__icontains=location) |
                Q(address__icontains=location)
            )
        
        # Price range filter
        price_range = request.query_params.get('priceRange')
        if price_range:
            if price_range == 'low':
                queryset = queryset.filter(services__price__lt=50).distinct()
            elif price_range == 'medium':
                queryset = queryset.filter(services__price__range=[50, 100]).distinct()
            elif price_range == 'high':
                queryset = queryset.filter(services__price__gt=100).distinct()
        
        # Rating filter
        rating = request.query_params.get('rating')
        if rating:
            try:
                min_rating = float(rating)
                queryset = queryset.annotate(
                    avg_rating=Avg('reviews__rating')
                ).filter(avg_rating__gte=min_rating)
            except ValueError:
                pass
        
        # Open now filter
        open_now = request.query_params.get('openNow')
        if open_now == 'true':
            now = timezone.now()
            current_time = now.time()
            current_weekday = now.weekday()
            
            # FIX: Changed field name from business_hours to hours
            queryset = queryset.filter(
                hours__weekday=current_weekday,
                hours__is_closed=False,
                hours__opening_time__lte=current_time,
                hours__closing_time__gte=current_time
            ).distinct()
        
        # Has offers filter - FIX: Removed non-existent field
        # has_offers = request.query_params.get('hasOffers')
        # Services don't have a has_discount field in the model
        
        # Sorting
        sort_by = request.query_params.get('sort_by', 'relevance')
        if sort_by == 'rating':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        elif sort_by == 'reviews':
            queryset = queryset.annotate(review_count=Count('reviews')).order_by('-review_count')
        elif sort_by == 'distance':
            # For now, just order by name since we don't have user location
            queryset = queryset.order_by('name')
        elif sort_by == 'price_low':
            queryset = queryset.annotate(min_price=Min('services__price')).order_by('min_price')
        elif sort_by == 'price_high':
            queryset = queryset.annotate(max_price=Max('services__price')).order_by('-max_price')
        else:  # relevance
            if search:
                # FIX: Use annotate instead of extra for better compatibility
                queryset = queryset.annotate(
                    name_match=Count('id', filter=Q(name__icontains=search)),
                    desc_match=Count('id', filter=Q(description__icontains=search)),
                    cat_match=Count('id', filter=Q(category__icontains=search))
                ).order_by('-name_match', '-desc_match', '-cat_match', '-created_at')
            else:
                queryset = queryset.order_by('-created_at')
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured businesses
        """
        queryset = self.get_queryset().annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).filter(
            avg_rating__gte=4.0,
            review_count__gte=5
        ).order_by('-avg_rating', '-review_count')[:10]
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def revenue_report(self, request, slug=None):
        """
        Generate detailed revenue report
        """
        business = self.get_object()
        
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to view revenue reports'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        period = request.query_params.get('period', 'month')
        
        if period == 'week':
            start_date = timezone.now().date() - timedelta(days=7)
        elif period == 'month':
            start_date = timezone.now().date() - timedelta(days=30)
        elif period == 'quarter':
            start_date = timezone.now().date() - timedelta(days=90)
        elif period == 'year':
            start_date = timezone.now().date() - timedelta(days=365)
        else:
            start_date = timezone.now().date() - timedelta(days=30)
        
        bookings = Booking.objects.filter(
            business=business,
            booking_date__gte=start_date,
            is_paid=True
        )
        
        report = {
            'period': period,
            'start_date': start_date,
            'end_date': timezone.now().date(),
            'total_revenue': float(
                bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
            ),
            'total_bookings': bookings.count(),
            'average_booking_value': float(
                bookings.aggregate(Avg('total_price'))['total_price__avg'] or 0
            ),
            'revenue_by_service': self._get_service_revenue(business, start_date),
            'revenue_by_day': self._get_revenue_by_day(bookings),
            'payment_methods': self._get_payment_method_breakdown(bookings),
            'top_revenue_customers': self._get_top_customers(business, start_date)[:5]
        }
        
        return Response(report)
    
    def _get_revenue_by_day(self, bookings):
        """Get daily revenue breakdown"""
        return list(
            bookings.values('booking_date').annotate(
                revenue=Sum('total_price')
            ).order_by('booking_date').values('booking_date', 'revenue')
        )
    
    def _get_payment_method_breakdown(self, bookings):
        """Get payment method breakdown"""
        return list(
            bookings.values('payment_method').annotate(
                count=Count('id'),
                total=Sum('total_price')
            ).order_by('-total')
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        """
        Get businesses owned by the authenticated user
        """
        businesses = Business.objects.filter(
            owner=request.user,
            is_active=True
        ).order_by('-created_at')
        
        serializer = self.get_serializer(businesses, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Service model
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'duration_minutes', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Override create to handle business association properly"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get business from validated data
        business_id = serializer.validated_data.get('business')
        if not business_id:
            raise serializers.ValidationError("Business ID is required")
            
        business = get_object_or_404(Business, id=business_id)
        
        # Allow superusers to create services for any business
        if not self.request.user.is_superuser:
            # For non-superusers, verify they own the business
            if business.owner != self.request.user:
                raise PermissionDenied("You can only add services to your own business")
        
        # Remove business UUID from validated_data and save with business instance
        serializer.validated_data.pop('business', None)
        service = serializer.save(business=business)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """
        Bulk update multiple services
        """
        updates = request.data.get('updates', [])
        if not updates:
            return Response({'error': 'No updates provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_services = []
        errors = []
        
        for update_data in updates:
            service_id = update_data.get('id')
            if not service_id:
                errors.append({'error': 'Service ID is required', 'data': update_data})
                continue
            
            try:
                service = Service.objects.get(id=service_id, business__owner=request.user)
                
                # Update allowed fields
                allowed_fields = ['name', 'description', 'price', 'duration_minutes', 'is_active']
                for field in allowed_fields:
                    if field in update_data:
                        setattr(service, field, update_data[field])
                
                service.save()
                updated_services.append(service.id)
            except Service.DoesNotExist:
                errors.append({'error': f'Service with ID {service_id} not found or access denied'})
        
        return Response({
            'updated': updated_services,
            'errors': errors,
            'message': f'{len(updated_services)} services updated successfully'
        })
    
    @action(detail=False, methods=['post'])
    def update_order(self, request):
        """
        Update the display order of services
        """
        updates = request.data.get('updates', [])
        if not updates:
            return Response({'error': 'No updates provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_services = []
        errors = []
        
        for update_data in updates:
            service_id = update_data.get('id')
            display_order = update_data.get('display_order')
            
            if not service_id or display_order is None:
                errors.append({'error': 'Service ID and display_order are required', 'data': update_data})
                continue
            
            try:
                service = Service.objects.get(id=service_id, business__owner=request.user)
                service.display_order = display_order
                service.save(update_fields=['display_order'])
                updated_services.append(service.id)
            except Service.DoesNotExist:
                errors.append({'error': f'Service with ID {service_id} not found or access denied'})
        
        return Response({
            'updated': updated_services,
            'errors': errors,
            'message': f'{len(updated_services)} service orders updated successfully'
        })


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking model with status management
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'service', 'booking_date']
    ordering_fields = ['booking_date', 'start_time', 'created_at']
    ordering = ['-booking_date', '-start_time']
    
    def get_queryset(self):
        """Filter bookings based on user type"""
        user = self.request.user
        queryset = super().get_queryset()
        
        if user.user_type == 'business_owner':
            queryset = queryset.filter(business__owner=user)
        elif user.user_type == 'customer':
            queryset = queryset.filter(customer__user=user)
        elif user.user_type == 'admin':
            pass  # Admins can see all bookings
        else:
            queryset = queryset.none()
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                booking_date__range=[start_date, end_date]
            )
        
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), CanCreateBooking()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Create booking with customer profile"""
        customer, created = Customer.objects.get_or_create(
            user=self.request.user,
            defaults={'phone': ''}
        )
        
        # Get business and service from validated data (already validated in serializer)
        business = serializer.validated_data.get('business')
        service = serializer.validated_data.get('service')
        
        # Calculate total price with any additional fees
        total_price = service.price
        
        # Save booking with all validated data
        booking = serializer.save(
            customer=customer,
            business=business,
            service=service,
            total_price=total_price
        )
        
        # Auto-confirm if business setting allows
        if business.auto_confirm_bookings:
            booking.status = 'confirmed'
            booking.save()
        
        # Send notifications
        self._send_booking_notification(booking, 'created')
        
        # Update customer stats
        Customer.objects.filter(id=customer.id).update(
            total_bookings=F('total_bookings') + 1
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def chart_data(self, request):
        """
        Get booking chart data for dashboard analytics
        """
        user = request.user
        
        # Check permissions - allow authenticated users but filter data appropriately
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get period filter
        period = request.query_params.get('period', 'week')
        
        # Calculate date range
        now = timezone.now()
        if period in ['week', '7d']:
            start_date = now - timedelta(days=7)
        elif period in ['month', '30d']:
            start_date = now - timedelta(days=30)
        elif period in ['quarter', '90d']:
            start_date = now - timedelta(days=90)
        elif period in ['year', '365d']:
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(days=7)
        
        # Get base queryset
        queryset = self.get_queryset()
        
        # Filter for business owners - they should only see their own businesses' data
        if user.user_type == 'business_owner':
            queryset = queryset.filter(business__owner=user)
        
        # Get business filter
        business_param = request.query_params.get('business')
        if business_param:
            try:
                # Try to get business by slug first, then by ID if it's a valid UUID
                import uuid
                business = None
                
                # First try to get by slug (more URL-friendly)
                try:
                    business = Business.objects.get(slug=business_param)
                except Business.DoesNotExist:
                    # If slug doesn't work, try UUID if parameter is a valid UUID
                    try:
                        uuid.UUID(business_param)  # Check if it's a valid UUID
                        business = Business.objects.get(id=business_param)
                    except (ValueError, Business.DoesNotExist):
                        pass  # Neither slug nor UUID worked
                
                if not business:
                    return Response(
                        {'error': f'Business not found with identifier: {business_param}'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Only allow business owners to see their own data
                if user.user_type == 'business_owner' and business.owner != user:
                    return Response(
                        {'error': 'Permission denied'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                queryset = queryset.filter(business=business)
            except Exception as e:
                return Response(
                    {'error': f'Error processing business parameter: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Filter by date range
        bookings = queryset.filter(
            created_at__gte=start_date
        ).values('booking_date', 'status').annotate(
            count=Count('id')
        ).order_by('booking_date')
        
        # Prepare chart data
        chart_data = []
        current_date = start_date.date()
        end_date = now.date()
        
        while current_date <= end_date:
            day_bookings = bookings.filter(booking_date=current_date)
            
            confirmed = sum(b['count'] for b in day_bookings if b['status'] == 'confirmed')
            pending = sum(b['count'] for b in day_bookings if b['status'] == 'pending')
            cancelled = sum(b['count'] for b in day_bookings if b['status'] == 'cancelled')
            total = confirmed + pending + cancelled
            
            chart_data.append({
                'date': current_date.isoformat(),
                'confirmed': confirmed,
                'pending': pending,
                'cancelled': cancelled,
                'total': total
            })
            
            current_date += timedelta(days=1)
        
        return Response({
            'period': period,
            'data': chart_data
        })
    
    def perform_update(self, serializer):
        """Handle booking updates"""
        old_status = serializer.instance.status
        booking = serializer.save()
        new_status = booking.status
        
        # Send notification if status changed
        if old_status != new_status:
            self._send_booking_notification(booking, 'status_changed')
    
    def _send_booking_notification(self, booking, notification_type):
        """Send booking-related notifications"""
        if notification_type == 'created':
            # Notification to business owner
            Notification.objects.create(
                user=booking.business.owner,
                type='booking_confirmed',
                title='New Booking',
                message=f'New booking from {booking.customer.user.full_name} for {booking.service.name}',
                booking=booking,
                business=booking.business
            )
            
            # Notification to customer
            Notification.objects.create(
                user=booking.customer.user,
                type='booking_confirmed',
                title='Booking Confirmed',
                message=f'Your booking for {booking.service.name} on {booking.booking_date} at {booking.start_time} has been received',
                booking=booking,
                business=booking.business
            )
        
        elif notification_type == 'status_changed':
            Notification.objects.create(
                user=booking.customer.user,
                type='booking_confirmed' if booking.status == 'confirmed' else 'booking_cancelled',
                title=f'Booking {booking.status.title()}',
                message=f'Your booking for {booking.service.name} has been {booking.status}',
                booking=booking,
                business=booking.business
            )
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a pending booking"""
        booking = self.get_object()
        
        if booking.business.owner != request.user:
            return Response(
                {'error': 'You can only confirm your own business bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'pending':
            return Response(
                {'error': 'Only pending bookings can be confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        
        self._send_booking_notification(booking, 'status_changed')
        
        return Response({'status': 'Booking confirmed'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # Check permission
        can_cancel = (
            booking.customer.user == request.user or
            booking.business.owner == request.user
        )
        
        if not can_cancel:
            return Response(
                {'error': 'You do not have permission to cancel this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status in ['cancelled', 'completed']:
            return Response(
                {'error': f'Cannot cancel a {booking.status} booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        self._send_booking_notification(booking, 'status_changed')
        
        # Update customer stats if paid booking was cancelled
        if booking.is_paid:
            customer = booking.customer
            customer.total_spent = F('total_spent') - booking.total_price
            customer.save()
        
        return Response({'status': 'Booking cancelled'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark booking as completed"""
        booking = self.get_object()
        
        if booking.business.owner != request.user:
            return Response(
                {'error': 'You can only complete your own business bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'confirmed':
            return Response(
                {'error': 'Only confirmed bookings can be completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'completed'
        booking.save()
        
        # Update customer spent amount
        if booking.is_paid:
            customer = booking.customer
            customer.total_spent = F('total_spent') + booking.total_price
            customer.save()
        
        # Send review request notification
        Notification.objects.create(
            user=booking.customer.user,
            type='review_request',
            title='How was your experience?',
            message=f'Please leave a review for {booking.service.name} at {booking.business.name}',
            booking=booking,
            business=booking.business
        )
        
        return Response({'status': 'Booking completed'})
    
    @action(detail=True, methods=['post'])
    def mark_no_show(self, request, pk=None):
        """Mark booking as no-show"""
        booking = self.get_object()
        
        if booking.business.owner != request.user:
            return Response(
                {'error': 'You can only mark no-show for your own business bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        booking.status = 'no_show'
        booking.save()
        
        return Response({'status': 'Booking marked as no-show'})
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming bookings for the authenticated user"""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(
            booking_date__gte=today,
            status__in=['confirmed', 'pending']
        ).order_by('booking_date', 'start_time')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get booking history for the authenticated user"""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(
            booking_date__lt=today
        ).order_by('-booking_date', '-start_time')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer model
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
    ordering_fields = ['created_at', 'total_bookings', 'total_spent']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter customers based on user type"""
        user = self.request.user
        
        if user.user_type == 'business_owner':
            # Show only customers who have booked with the business
            return Customer.objects.filter(
                bookings__business__owner=user
            ).distinct()
        elif user.user_type == 'customer':
            # Customers can only see their own profile
            return Customer.objects.filter(user=user)
        elif user.user_type == 'admin':
            return Customer.objects.all()
        
        return Customer.objects.none()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's customer profile"""
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'phone': ''}
        )
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_preferred_business_me(self, request):
        """Add a business to current user's preferred list"""
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'phone': ''}
        )
        
        business_id = request.data.get('business_id')
        try:
            business = Business.objects.get(id=business_id)
            customer.preferred_businesses.add(business)
            return Response({'status': 'Business added to favorites'})
        except Business.DoesNotExist:
            return Response(
                {'error': 'Business not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def add_preferred_business(self, request, pk=None):
        """Add a business to preferred list"""
        customer = self.get_object()
        
        if customer.user != request.user:
            return Response(
                {'error': 'You can only modify your own preferences'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        business_id = request.data.get('business_id')
        try:
            business = Business.objects.get(id=business_id)
            customer.preferred_businesses.add(business)
            return Response({'status': 'Business added to favorites'})
        except Business.DoesNotExist:
            return Response(
                {'error': 'Business not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def analytics(self, request):
        """
        Get customer analytics data for dashboard
        """
        user = request.user
        
        # Check permissions - allow authenticated users but filter data appropriately
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get period filter
        period = request.query_params.get('period', 'month')
        
        # Calculate date range
        now = timezone.now()
        if period in ['week', '7d']:
            start_date = now - timedelta(days=7)
        elif period in ['month', '30d']:
            start_date = now - timedelta(days=30)
        elif period in ['quarter', '90d']:
            start_date = now - timedelta(days=90)
        elif period in ['year', '365d']:
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(days=30)
        
        # Get base queryset
        queryset = self.get_queryset()
        
        # Filter by creation date
        customers_in_period = queryset.filter(
            created_at__gte=start_date
        )
        
        # Calculate analytics
        total_customers = queryset.count()
        new_customers = customers_in_period.count()
        repeat_customers = queryset.filter(total_bookings__gt=1).count()
        
        # Customer acquisition over time
        daily_customers = []
        current_date = start_date.date()
        end_date = now.date()
        
        while current_date <= end_date:
            daily_count = queryset.filter(
                created_at__date=current_date
            ).count()
            
            daily_customers.append({
                'date': current_date.isoformat(),
                'count': daily_count
            })
            
            current_date += timedelta(days=1)
        
        # Top customers by spending
        top_customers = queryset.order_by('-total_spent')[:10].values(
            'user__first_name', 'user__last_name', 'user__email', 
            'total_spent', 'total_bookings'
        )
        
        return Response({
            'period': period,
            'summary': {
                'total_customers': total_customers,
                'new_customers': new_customers,
                'repeat_customers': repeat_customers,
                'retention_rate': round((repeat_customers / total_customers * 100) if total_customers > 0 else 0, 2)
            },
            'daily_acquisition': daily_customers,
            'top_customers': list(top_customers)
        })
    
    @action(detail=True, methods=['post'])
    def remove_preferred_business(self, request, pk=None):
        """Remove a business from customer's preferred list"""
        customer = self.get_object()
        
        if customer.user != request.user:
            return Response(
                {'error': 'You can only modify your own preferences'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        business_id = request.data.get('business_id')
        try:
            business = Business.objects.get(id=business_id)
            customer.preferred_businesses.remove(business)
            return Response({'status': 'Business removed from favorites'})
        except Business.DoesNotExist:
            return Response(
                {'error': 'Business not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def booking_history(self, request, pk=None):
        """Get customer's booking history"""
        customer = self.get_object()
        
        if customer.user != request.user and request.user.user_type != 'admin':
            return Response(
                {'error': 'You can only view your own booking history'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        bookings = customer.bookings.all().order_by('-created_at')
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        business_filter = request.query_params.get('business')
        if business_filter:
            bookings = bookings.filter(business_id=business_filter)
        
        # Pagination
        page = self.paginate_queryset(bookings)
        if page is not None:
            from .serializers import BookingSerializer
            serializer = BookingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        from .serializers import BookingSerializer
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get customer statistics"""
        customer = self.get_object()
        
        if customer.user != request.user and request.user.user_type != 'admin':
            return Response(
                {'error': 'You can only view your own statistics'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculate stats
        total_bookings = customer.bookings.count()
        completed_bookings = customer.bookings.filter(status='completed').count()
        cancelled_bookings = customer.bookings.filter(status='cancelled').count()
        total_spent = customer.bookings.filter(status='completed').aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        
        favorite_businesses_count = customer.preferred_businesses.count()
        
        # Recent activity
        recent_bookings = customer.bookings.order_by('-created_at')[:5]
        from .serializers import BookingSerializer
        recent_bookings_data = BookingSerializer(recent_bookings, many=True).data
        
        return Response({
            'total_bookings': total_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_spent': float(total_spent),
            'favorite_businesses_count': favorite_businesses_count,
            'completion_rate': round((completed_bookings / total_bookings * 100) if total_bookings > 0 else 0, 2),
            'recent_bookings': recent_bookings_data
        })


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review model
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business', 'rating', 'is_verified']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by business if specified
        business_id = self.request.query_params.get('business')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        # Filter by rating range
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Create review with customer profile"""
        customer, created = Customer.objects.get_or_create(
            user=self.request.user,
            defaults={'phone': ''}
        )
        
        # Check if booking exists and belongs to customer
        booking_id = self.request.data.get('booking_id')
        if booking_id:
            try:
                booking = Booking.objects.get(
                    id=booking_id,
                    customer=customer,
                    status='completed'
                )
                serializer.save(customer=customer, booking=booking, is_verified=True)
            except Booking.DoesNotExist:
                serializer.save(customer=customer, is_verified=False)
        else:
            serializer.save(customer=customer, is_verified=False)
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Business owner responds to a review"""
        review = self.get_object()
        
        if review.business.owner != request.user:
            return Response(
                {'error': 'You can only respond to reviews for your business'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        response_text = request.data.get('response')
        if not response_text:
            return Response(
                {'error': 'Response text is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        review.business_response = response_text
        review.response_date = timezone.now()
        review.save()
        
        # Notify customer of business response
        Notification.objects.create(
            user=review.customer.user,
            type='general',
            title='Business responded to your review',
            message=f'{review.business.name} has responded to your review',
            business=review.business
        )
        
        return Response({'status': 'Response added successfully'})
    
    @action(detail=True, methods=['post'])
    def mark_featured(self, request, pk=None):
        """Mark a review as featured"""
        review = self.get_object()
        
        if review.business.owner != request.user:
            return Response(
                {'error': 'You can only feature reviews for your business'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        review.is_featured = True
        review.save()
        
        return Response({'status': 'Review marked as featured'})


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notification model
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get notifications for authenticated user only"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return Response({'status': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({'status': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        """Delete all read notifications"""
        deleted_count = Notification.objects.filter(
            user=request.user,
            is_read=True
        ).delete()[0]
        
        return Response({
            'status': 'Read notifications cleared',
            'deleted_count': deleted_count
        })


class BusinessHoursViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessHours model
    """
    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHoursSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by business"""
        queryset = super().get_queryset()
        business_id = self.request.query_params.get('business')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        return queryset.order_by('weekday', 'opening_time')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessOwner()]