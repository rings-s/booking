# Internationalization (i18n) System

A comprehensive internationalization system for the SvelteKit booking management application, built with `svelte-i18n`.

## Features

- **5 Supported Languages**: English (en), Spanish (es), French (fr), German (de), Arabic (ar)
- **Automatic Language Detection**: Browser language, localStorage, and Accept-Language header
- **SSR Compatible**: Works with SvelteKit's server-side rendering
- **RTL Support**: Right-to-left support for Arabic
- **Type Safety**: TypeScript interfaces for translations
- **Multiple Language Switcher Variants**: Dropdown, buttons, and select components
- **Advanced Formatting**: Date, time, number, and currency formatting
- **Fallback System**: Graceful fallback to English for missing translations

## Quick Start

### 1. Import and Use Translations

```svelte
<script>
  import { t } from '$lib/stores/i18n.js';
</script>

<h1>{$t('common.home')}</h1>
<button>{$t('common.save')}</button>
```

### 2. Add Language Switcher

```svelte
<script>
  import LanguageSwitcher from '$lib/components/common/LanguageSwitcher.svelte';
</script>

<!-- Dropdown variant -->
<LanguageSwitcher variant="dropdown" />

<!-- Button variant -->
<LanguageSwitcher variant="buttons" />

<!-- Select variant -->
<LanguageSwitcher variant="select" />
```

### 3. Format Dates and Numbers

```svelte
<script>
  import { formatDate, formatCurrency, formatNumber } from '$lib/stores/i18n.js';
  
  let date = new Date();
  let amount = 99.99;
</script>

<p>Date: {formatDate(date, 'long')}</p>
<p>Price: {formatCurrency(amount, 'USD')}</p>
<p>Number: {formatNumber(1234.56, 'decimal')}</p>
```

## File Structure

```
src/lib/i18n/
├── index.js              # Main i18n configuration
├── utils.js              # Utility functions
├── types.d.ts            # TypeScript type definitions
├── locales/              # Translation files
│   ├── en.json           # English translations
│   ├── es.json           # Spanish translations
│   ├── fr.json           # French translations
│   ├── de.json           # German translations
│   └── ar.json           # Arabic translations
└── README.md             # This file
```

## Translation Keys Structure

The translation keys are organized into logical groups:

- `common`: General UI elements (save, edit, delete, etc.)
- `navigation`: Navigation menu items
- `auth`: Authentication related text
- `business`: Business management features
- `booking`: Booking system features
- `service`: Service management
- `customer`: Customer management
- `dashboard`: Dashboard content
- `review`: Review system
- `notification`: Notification messages
- `subscription`: Subscription features
- `validation`: Form validation messages
- `error`: Error messages
- `success`: Success messages
- `time`: Time-related terms

## Adding New Translations

### 1. Add to Translation Files

Add the new key to all language files in `src/lib/i18n/locales/`:

```json
// en.json
{
  "newFeature": {
    "title": "New Feature",
    "description": "This is a new feature"
  }
}
```

```json
// es.json
{
  "newFeature": {
    "title": "Nueva Función",
    "description": "Esta es una nueva función"
  }
}
```

### 2. Update TypeScript Types

Add the new keys to `src/lib/i18n/types.d.ts`:

```typescript
export interface TranslationKey {
  // ... existing keys
  newFeature: {
    title: string;
    description: string;
  };
}
```

### 3. Use in Components

```svelte
<script>
  import { t } from '$lib/stores/i18n.js';
</script>

<h2>{$t('newFeature.title')}</h2>
<p>{$t('newFeature.description')}</p>
```

## Language Detection Priority

The system detects languages in this order:

1. **URL Path**: `/es/dashboard` → Spanish
2. **Cookie**: `locale=fr` → French
3. **Browser Language**: `navigator.language` → Detected language
4. **Accept-Language Header**: Server-side detection
5. **Default**: English (en)

## SSR Configuration

The system is configured for SvelteKit SSR:

- **Server**: Language detection in `hooks.server.js`
- **Client**: Hydration in `+layout.svelte`
- **HTML Attributes**: Automatic `lang` and `dir` attributes

## Changing Language Programmatically

```javascript
import { changeLocale } from '$lib/stores/i18n.js';

// Change to Spanish
await changeLocale('es');

// The system will:
// 1. Load the Spanish translations
// 2. Update localStorage
// 3. Update HTML lang/dir attributes
// 4. Dispatch a custom event
```

## RTL Support

Arabic language automatically enables RTL mode:

```javascript
import { isRTL } from '$lib/i18n/utils.js';

if (isRTL('ar')) {
  // Apply RTL-specific styles
}
```

## Formatting Options

### Date Formatting

```javascript
formatDate(date, 'short')    // 12/25/2024
formatDate(date, 'long')     // December 25, 2024
formatDate(date, 'time')     // 2:30 PM
formatDate(date, 'datetime') // Dec 25, 2024, 2:30 PM
```

### Number Formatting

```javascript
formatNumber(1234.56, 'decimal')  // 1,234.56
formatNumber(0.85, 'percent')     // 85%
formatCurrency(99.99, 'USD')      // $99.99
```

## Performance Considerations

- **Lazy Loading**: Translation files are loaded on demand
- **Caching**: Loaded translations are cached in memory
- **SSR Optimization**: Server-side language detection reduces client-side work
- **Tree Shaking**: Only used translation keys are included in the bundle

## Best Practices

### 1. Use Descriptive Keys

```javascript
// Good
$t('booking.confirmBooking')
$t('error.networkError')

// Avoid
$t('button1')
$t('msg')
```

### 2. Keep Translations Consistent

Maintain consistent terminology across all languages:

```json
{
  "common": {
    "save": "Save",
    "cancel": "Cancel"
  }
}
```

### 3. Handle Pluralization

Use ICU message format for complex pluralization:

```json
{
  "booking": {
    "count": {
      "singular": "1 booking",
      "plural": "{count} bookings"
    }
  }
}
```

### 4. Use Interpolation for Dynamic Content

```svelte
<script>
  import { t } from '$lib/stores/i18n.js';
</script>

<!-- Translation with interpolation -->
{$t('auth.signInWith', { values: { provider: 'Google' } })}
```

## Troubleshooting

### Missing Translations

The system will:
1. Log a warning in the console
2. Display the translation key
3. Fall back to English if available

### Language Not Loading

Check:
1. Translation file exists in `locales/` directory
2. Language is added to `supportedLocales` array
3. Import statement in `index.js` is correct

### SSR Issues

Ensure:
1. `+layout.server.js` passes locale data
2. `hooks.server.js` detects language correctly
3. Client-side hydration matches server state

## Testing Translations

```javascript
// Test language switching
import { changeLocale } from '$lib/stores/i18n.js';

await changeLocale('es');
// Verify UI updates to Spanish

// Test RTL
await changeLocale('ar');
// Verify direction changes to RTL
```

## Contributing

When adding new features:

1. Add translations to ALL language files
2. Update TypeScript types
3. Test with multiple languages
4. Verify RTL layout works
5. Test SSR functionality

## License

Part of the BookingPro application. See main project license.