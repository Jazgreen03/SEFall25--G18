import { BootstrapContext, bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { config } from './app/app.config.server';

/**
 * Bootstraps the Angular application for server-side rendering.
 *
 * @param context - The `BootstrapContext` provided by Angular SSR,
 *                  containing platform-specific information and dependency injection context.
 * @returns A Promise that resolves once the Angular application has been bootstrapped.
 *
 * @example
 * ```ts
 * import bootstrap from './main.server';
 *
 * bootstrap(context).then(() => {
 *   console.log('Angular app bootstrapped for SSR');
 * });
 * ```
 */
const bootstrap = (context: BootstrapContext) =>
    bootstrapApplication(App, config, context);

/**
 * Default export of the server-side bootstrap function.
 *
 * Used by Angular SSR engine to render the application on the server.
 */
export default bootstrap;
