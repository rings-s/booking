<!-- src/lib/components/layout/Footer.svelte -->
<script>
    const currentYear = new Date().getFullYear();
    
    const footerLinks = {
      company: [
        { name: 'About', href: '/about' },
        { name: 'Blog', href: '/blog' },
        { name: 'Careers', href: '/careers' },
        { name: 'Contact', href: '/contact' }
      ],
      support: [
        { name: 'Help Center', href: '/help' },
        { name: 'Safety', href: '/safety' },
        { name: 'Terms', href: '/terms' },
        { name: 'Privacy', href: '/privacy' }
      ],
      features: [
        { name: 'For Business', href: '/business' },
        { name: 'For Customers', href: '/customers' },
        { name: 'Pricing', href: '/pricing' },
        { name: 'Developers', href: '/developers' }
      ]
    };
  </script>
  
  <footer class="bg-gray-900">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="py-12 md:py-16">
        <div class="grid grid-cols-2 gap-8 md:grid-cols-4">
          <div>
            <h3 class="text-sm font-semibold text-gray-400 tracking-wider uppercase">Company</h3>
            <ul class="mt-4 space-y-3">
              {#each footerLinks.company as link}
                <li>
                  <a href={link.href} class="text-base text-gray-300 hover:text-white">
                    {link.name}
                  </a>
                </li>
              {/each}
            </ul>
          </div>
          
          <div>
            <h3 class="text-sm font-semibold text-gray-400 tracking-wider uppercase">Support</h3>
            <ul class="mt-4 space-y-3">
              {#each footerLinks.support as link}
                <li>
                  <a href={link.href} class="text-base text-gray-300 hover:text-white">
                    {link.name}
                  </a>
                </li>
              {/each}
            </ul>
          </div>
          
          <div>
            <h3 class="text-sm font-semibold text-gray-400 tracking-wider uppercase">Features</h3>
            <ul class="mt-4 space-y-3">
              {#each footerLinks.features as link}
                <li>
                  <a href={link.href} class="text-base text-gray-300 hover:text-white">
                    {link.name}
                  </a>
                </li>
              {/each}
            </ul>
          </div>
          
          <div>
            <h3 class="text-sm font-semibold text-gray-400 tracking-wider uppercase">
              Subscribe to our newsletter
            </h3>
            <p class="mt-4 text-base text-gray-300">
              Get the latest updates and offers.
            </p>
            <form class="mt-4 sm:flex sm:max-w-md">
              <input
                type="email"
                placeholder="Enter your email"
                class="w-full min-w-0 px-4 py-2 text-base text-gray-900 placeholder-gray-500 bg-white border border-transparent rounded-md appearance-none focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white focus:placeholder-gray-400"
              />
              <div class="mt-3 rounded-md sm:mt-0 sm:ml-3 sm:flex-shrink-0">
                <button
                  type="submit"
                  class="w-full px-4 py-2 text-base font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-indigo-500"
                >
                  Subscribe
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-700 py-8">
        <p class="text-base text-gray-400 text-center">
          © {currentYear} BookingPro. All rights reserved.
        </p>
      </div>
    </div>
  </footer>