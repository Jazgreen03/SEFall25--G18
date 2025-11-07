import { RenderMode, ServerRoute } from '@angular/ssr';

/**
 * Server-Side Rendering (SSR) Routes Configuration
 * 
 * Defines rendering strategies for Angular Universal server-side rendering.
 * Configures how different routes should be handled during server-side rendering.
 * 
 * This configuration enables static site generation (prerendering) for all routes,
 * providing optimal performance and SEO benefits across the entire application.
 * 
 * @constant serverRoutes
 * @type {ServerRoute[]}
 * 
 * @see RenderMode.Prerender - Generates static HTML at build time for fast loading
 * @see https://angular.io/guide/ssr#prerendering for more information on prerendering
 */
export const serverRoutes: ServerRoute[] = [
  /**
   * Catch-all route configuration
   * 
   * Applies prerendering to ALL application routes using the wildcard pattern '**'
   * This means every route in the application will be pre-rendered as static HTML
   * during the build process, providing:
   * - Faster initial page loads
   * - Better SEO through server-rendered content
   * - Improved performance on slow client devices
   * - Consistent rendering across different environments
   * 
   * @path '**' - Matches all routes in the application
   * @renderMode RenderMode.Prerender - Enables static generation at build time
   */
  {
    path: '**',
    renderMode: RenderMode.Prerender
  }
];