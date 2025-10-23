import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering, withRoutes } from '@angular/ssr';
import { appConfig } from './app.config';
import { serverRoutes } from './app.routes.server';

/**
 * Merged Angular application configuration for server-side rendering (SSR).
 *
 * This configuration extends the client-side `appConfig` with server-specific providers.
 * 
 * Key features:
 * - Enables server-side rendering for the Angular application.
 * - Configures the server with application routes for pre-rendering and SSR requests.
 *
 * This is the configuration that should be used when bootstrapping the Angular app on the server.
 *
 * @example
 * ```ts
 * import { bootstrapApplication } from '@angular/platform-browser';
 * import { App } from './app/app';
 * import { config } from './app/app.config.server';
 *
 * bootstrapApplication(App, config).then(() => {
 *   console.log('Angular app bootstrapped with server configuration');
 * });
 * ```
 */
export const config: ApplicationConfig = mergeApplicationConfig(appConfig, {
  providers: [
    provideServerRendering(withRoutes(serverRoutes))
  ]
});
