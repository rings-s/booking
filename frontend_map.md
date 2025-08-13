booking-app/
├── package.json
├── vite.config.js
├── svelte.config.js
├── app.html
├── .env.example
├── static/
│   ├── favicon.png
│   └── robots.txt
├── src/
│   ├── app.js
│   ├── app.html
│   ├── app.css
│   ├── hooks.client.js
│   ├── hooks.server.js
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.js
│   │   │   ├── auth.js
│   │   │   ├── businesses.js
│   │   │   ├── bookings.js
│   │   │   ├── services.js
│   │   │   ├── reviews.js
│   │   │   ├── customers.js
│   │   │   ├── notifications.js
│   │   │   └── subscriptions.js
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.svelte
│   │   │   │   ├── Card.svelte
│   │   │   │   ├── Modal.svelte
│   │   │   │   ├── Alert.svelte
│   │   │   │   ├── Spinner.svelte
│   │   │   │   ├── Input.svelte
│   │   │   │   ├── Select.svelte
│   │   │   │   └── Avatar.svelte
│   │   │   ├── layout/
│   │   │   │   ├── Header.svelte
│   │   │   │   ├── Footer.svelte
│   │   │   │   ├── Sidebar.svelte
│   │   │   │   ├── MobileMenu.svelte
│   │   │   │   └── NotificationBell.svelte
│   │   │   ├── business/
│   │   │   │   ├── BusinessCard.svelte
│   │   │   │   ├── BusinessForm.svelte
│   │   │   │   ├── BusinessHours.svelte
│   │   │   │   ├── ServiceList.svelte
│   │   │   │   ├── ServiceForm.svelte
│   │   │   │   └── QRCode.svelte
│   │   │   ├── booking/
│   │   │   │   ├── BookingCard.svelte
│   │   │   │   ├── BookingForm.svelte
│   │   │   │   ├── BookingCalendar.svelte
│   │   │   │   ├── TimeSlotPicker.svelte
│   │   │   │   ├── BookingStatus.svelte
│   │   │   │   └── BookingList.svelte
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsCard.svelte
│   │   │   │   ├── RevenueChart.svelte
│   │   │   │   ├── BookingChart.svelte
│   │   │   │   ├── ServiceChart.svelte
│   │   │   │   ├── CustomerChart.svelte
│   │   │   │   └── RecentActivity.svelte
│   │   │   ├── review/
│   │   │   │   ├── ReviewCard.svelte
│   │   │   │   ├── ReviewForm.svelte
│   │   │   │   ├── ReviewList.svelte
│   │   │   │   └── StarRating.svelte
│   │   │   └── subscription/
│   │   │       ├── PlanCard.svelte
│   │   │       ├── PricingTable.svelte
│   │   │       └── SubscriptionStatus.svelte
│   │   ├── stores/
│   │   │   ├── auth.js
│   │   │   ├── business.js
│   │   │   ├── booking.js
│   │   │   ├── notification.js
│   │   │   ├── cart.js
│   │   │   └── ui.js
│   │   ├── utils/
│   │   │   ├── validators.js
│   │   │   ├── formatters.js
│   │   │   ├── dates.js
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   └── config/
│   │       ├── app.js
│   │       └── navigation.js
│   └── routes/
│       ├── +layout.svelte
│       ├── +layout.js
│       ├── +page.svelte
│       ├── +error.svelte
│       ├── auth/
│       │   ├── login/
│       │   │   └── +page.svelte
│       │   ├── register/
│       │   │   └── +page.svelte
│       │   ├── forgot-password/
│       │   │   └── +page.svelte
│       │   └── logout/
│       │       └── +server.js
│       ├── dashboard/
│       │   ├── +page.svelte
│       │   ├── +page.js
│       │   └── +layout.svelte
│       ├── businesses/
│       │   ├── +page.svelte
│       │   ├── +page.js
│       │   ├── new/
│       │   │   └── +page.svelte
│       │   └── [slug]/
│       │       ├── +page.svelte
│       │       ├── +page.js
│       │       ├── edit/
│       │       │   └── +page.svelte
│       │       ├── services/
│       │       │   ├── +page.svelte
│       │       │   └── new/
│       │       │       └── +page.svelte
│       │       └── analytics/
│       │           └── +page.svelte
│       ├── bookings/
│       │   ├── +page.svelte
│       │   ├── +page.js
│       │   ├── new/
│       │   │   └── +page.svelte
│       │   └── [id]/
│       │       ├── +page.svelte
│       │       └── +page.js
│       ├── customers/
│       │   ├── +page.svelte
│       │   ├── profile/
│       │   │   └── +page.svelte
│       │   └── preferences/
│       │       └── +page.svelte
│       ├── reviews/
│       │   ├── +page.svelte
│       │   └── new/
│       │       └── +page.svelte
│       ├── notifications/
│       │   └── +page.svelte
│       ├── subscriptions/
│       │   ├── +page.svelte
│       │   └── upgrade/
│       │       └── +page.svelte
│       └── book/
│           └── [slug]/
│               └── +page.svelte 