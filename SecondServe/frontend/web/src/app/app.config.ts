import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { routes } from './app.routes';

/**
 * Angular client-side application configuration.
 *
 * This configuration sets up global providers for the browser application.
 * 
 * Key features:
 * - Enables global error listeners for uncaught errors and unhandled promise rejections.
 * - Configures Angular Zone change detection with event coalescing for performance.
 * - Provides router configuration with application routes.
 * - Enables client-side hydration for server-side rendered content with event replay.
 *
 * @example
 * ```ts
 * import { bootstrapApplication } from '@angular/platform-browser';
 * import { App } from './app/app';
 * import { appConfig } from './app/app.config';
 *
 * bootstrapApplication(App, appConfig).then(() => {
 *   console.log('Angular app bootstrapped with client config');
 * });
 * ```
 */
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideClientHydration(withEventReplay())
  ]
};
