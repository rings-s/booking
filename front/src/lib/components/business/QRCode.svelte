<!-- src/lib/components/business/QRCode.svelte -->
<script>
    import { onMount } from 'svelte';
    import QRCode from 'qrcode';
    import Button from '../common/Button.svelte';
    import Card from '../common/Card.svelte';
    import Input from '../common/Input.svelte';
    import toast from 'svelte-french-toast';
    
    export let business;
    export let size = 256;
    export let showCustomization = false;
    
    let canvas;
    let qrCodeDataUrl = '';
    let bookingUrl = '';
    let customUrl = '';
    let useCustomUrl = false;
    
    // QR Code customization options
    let options = {
      width: size,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      errorCorrectionLevel: 'M'
    };
    
    let darkColor = '#000000';
    let lightColor = '#FFFFFF';
    let includelogo = false;
    
    onMount(() => {
      generateQRCode();
    });
    
    async function generateQRCode() {
      bookingUrl = customUrl || `${window.location.origin}/book/${business.slug}`;
      
      try {
        // Generate QR code
        qrCodeDataUrl = await QRCode.toDataURL(bookingUrl, {
          ...options,
          color: {
            dark: darkColor,
            light: lightColor
          }
        });
        
        if (canvas) {
          const ctx = canvas.getContext('2d');
          const img = new Image();
          
          img.onload = () => {
            ctx.clearRect(0, 0, size, size);
            ctx.drawImage(img, 0, 0, size, size);
            
            // Add logo if available and enabled
            if (includelogo && business.logo) {
              const logo = new Image();
              logo.crossOrigin = 'anonymous';
              
              logo.onload = () => {
                const logoSize = size * 0.2;
                const logoX = (size - logoSize) / 2;
                const logoY = (size - logoSize) / 2;
                
                // Draw white background circle for logo
                ctx.fillStyle = lightColor;
                ctx.beginPath();
                ctx.arc(size / 2, size / 2, logoSize / 2 + 5, 0, 2 * Math.PI);
                ctx.fill();
                
                // Draw logo
                ctx.save();
                ctx.beginPath();
                ctx.arc(size / 2, size / 2, logoSize / 2, 0, 2 * Math.PI);
                ctx.clip();
                ctx.drawImage(logo, logoX, logoY, logoSize, logoSize);
                ctx.restore();
              };
              
              logo.src = business.logo;
            }
          };
          
          img.src = qrCodeDataUrl;
        }
      } catch (error) {
        console.error('Error generating QR code:', error);
        toast.error('Failed to generate QR code');
      }
    }
    
    function downloadQRCode(format = 'png') {
      const link = document.createElement('a');
      link.download = `${business.slug}-qr-code.${format}`;
      
      if (format === 'svg') {
        QRCode.toString(bookingUrl, {
          type: 'svg',
          ...options,
          color: {
            dark: darkColor,
            light: lightColor
          }
        }, (err, svg) => {
          if (err) {
            toast.error('Failed to generate SVG');
            return;
          }
          const blob = new Blob([svg], { type: 'image/svg+xml' });
          link.href = URL.createObjectURL(blob);
          link.click();
        });
      } else {
        link.href = qrCodeDataUrl;
        link.click();
      }
      
      toast.success(`QR code downloaded as ${format.toUpperCase()}`);
    }
    
    function printQRCode() {
      const printWindow = window.open('', '_blank');
      printWindow.document.write(`
        <html>
          <head>
            <title>QR Code - ${business.name}</title>
            <style>
              body {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
              }
              h1 { 
                margin-bottom: 20px;
                color: #333;
              }
              .info {
                margin-top: 20px;
                text-align: center;
                color: #666;
              }
              .url {
                margin-top: 10px;
                padding: 10px;
                background: #f5f5f5;
                border-radius: 5px;
                font-family: monospace;
                word-break: break-all;
              }
              @media print {
                body { padding: 0; }
              }
            </style>
          </head>
          <body>
            <h1>${business.name}</h1>
            <img src="${qrCodeDataUrl}" alt="QR Code" style="width: 300px; height: 300px;" />
            <div class="info">
              <p><strong>Scan to book online</strong></p>
              <div class="url">${bookingUrl}</div>
            </div>
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
    
    function copyUrl() {
      navigator.clipboard.writeText(bookingUrl);
      toast.success('Booking URL copied to clipboard');
    }
    
    function shareQRCode() {
      if (navigator.share) {
        navigator.share({
          title: `Book at ${business.name}`,
          text: `Book your appointment online at ${business.name}`,
          url: bookingUrl
        }).catch(err => console.log('Error sharing:', err));
      } else {
        copyUrl();
      }
    }
    
    $: if (darkColor || lightColor || useCustomUrl) {
      generateQRCode();
    }
  </script>
  
  <Card>
    <div slot="header" class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">Booking QR Code</h3>
      {#if showCustomization}
        <button
          type="button"
          class="text-sm text-indigo-600 hover:text-indigo-500"
          on:click={() => showCustomization = !showCustomization}
        >
          Customize
        </button>
      {/if}
    </div>
    
    <div class="flex flex-col items-center">
      <!-- QR Code Display -->
      <div class="p-4 bg-white rounded-lg shadow-inner">
        <canvas
          bind:this={canvas}
          width={size}
          height={size}
          class="rounded-lg"
        ></canvas>
      </div>
      
      <!-- Business Info -->
      <div class="mt-4 text-center">
        <p class="text-lg font-medium text-gray-900">{business.name}</p>
        <p class="text-sm text-gray-500 mt-1">Scan to book online</p>
      </div>
      
      <!-- Booking URL -->
      <div class="mt-4 w-full">
        <div class="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
          <input
            type="text"
            value={bookingUrl}
            readonly
            class="flex-1 text-sm font-mono text-gray-600 bg-transparent border-none focus:outline-none"
          />
          <button
            type="button"
            class="text-indigo-600 hover:text-indigo-500"
            on:click={copyUrl}
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Customization Options -->
      {#if showCustomization}
        <div class="mt-6 w-full space-y-4 p-4 bg-gray-50 rounded-lg">
          <h4 class="text-sm font-medium text-gray-900">Customize QR Code</h4>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-700 mb-1">Dark Color</label>
              <input
                type="color"
                bind:value={darkColor}
                class="h-10 w-full rounded cursor-pointer"
              />
            </div>
            
            <div>
              <label class="block text-sm text-gray-700 mb-1">Light Color</label>
              <input
                type="color"
                bind:value={lightColor}
                class="h-10 w-full rounded cursor-pointer"
              />
            </div>
          </div>
          
          {#if business.logo}
            <label class="flex items-center">
              <input
                type="checkbox"
                bind:checked={includelogo}
                on:change={generateQRCode}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-700">Include business logo</span>
            </label>
          {/if}
          
          <div>
            <label class="flex items-center mb-2">
              <input
                type="checkbox"
                bind:checked={useCustomUrl}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-700">Use custom URL</span>
            </label>
            
            {#if useCustomUrl}
              <Input
                bind:value={customUrl}
                placeholder="https://yourdomain.com/book"
                on:blur={generateQRCode}
              />
            {/if}
          </div>
          
          <Button variant="outline" size="sm" on:click={() => {
            darkColor = '#000000';
            lightColor = '#FFFFFF';
            includelogo = false;
            useCustomUrl = false;
            customUrl = '';
            generateQRCode();
          }}>
            Reset to Default
          </Button>
        </div>
      {/if}
      
      <!-- Action Buttons -->
      <div class="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 w-full">
        <Button variant="outline" size="sm" on:click={() => downloadQRCode('png')}>
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          PNG
        </Button>
        
        <Button variant="outline" size="sm" on:click={() => downloadQRCode('svg')}>
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          SVG
        </Button>
        
        <Button variant="outline" size="sm" on:click={printQRCode}>
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          Print
        </Button>
        
        <Button variant="outline" size="sm" on:click={shareQRCode}>
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m9.032 4.026a3 3 0 10-4.732 0M3 20.364a9 9 0 0118 0" />
          </svg>
          Share
        </Button>
      </div>
      
      <!-- Usage Instructions -->
      <div class="mt-6 p-4 bg-blue-50 rounded-lg w-full">
        <h4 class="text-sm font-medium text-blue-900 mb-2">How to use this QR code:</h4>
        <ul class="text-sm text-blue-700 space-y-1">
          <li>• Print and display at your business location</li>
          <li>• Add to business cards and flyers</li>
          <li>• Share on social media</li>
          <li>• Include in email signatures</li>
        </ul>
      </div>
    </div>
  </Card>