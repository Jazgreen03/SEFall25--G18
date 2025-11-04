import {
  AngularNodeAppEngine,
  createNodeRequestHandler,
  isMainModule,
  writeResponseToNodeResponse,
} from '@angular/ssr/node';
import express from 'express';
import { join } from 'node:path';

/**
 * The folder containing the browser (client-side) build output.
 * This is used to serve static assets like JS, CSS, and images.
 */
const browserDistFolder = join(import.meta.dirname, '../browser');

/**
 * The Express application instance.
 */
const app = express();

/**
 * Angular SSR engine instance for handling server-side rendering of the Angular app.
 */
const angularApp = new AngularNodeAppEngine();

/**
 * Example Express REST API endpoints can be defined here.
 *
 * Uncomment and define endpoints as necessary.
 *
 * Example:
 * ```ts
 * app.get('/api/{*splat}', (req, res) => {
 *   // Handle API request
 * });
 * ```
 */

/**
 * Middleware to serve static files from the `browserDistFolder`.
 *
 * Files are cached for 1 year (`maxAge: '1y'`) and no automatic index files or redirects are generated.
 */
app.use(
  express.static(browserDistFolder, {
    maxAge: '1y',
    index: false,
    redirect: false,
  }),
);

/**
 * Middleware to handle all other requests by rendering the Angular application.
 *
 * @param req - The incoming Express request.
 * @param res - The Express response to write the rendered HTML to.
 * @param next - The next middleware in the Express chain.
 */
app.use((req, res, next) => {
  angularApp
    .handle(req)
    .then((response) =>
      response ? writeResponseToNodeResponse(response, res) : next(),
    )
    .catch(next);
});

/**
 * Starts the Express server if this module is the main entry point or run via PM2.
 *
 * The server listens on the port specified in the `PORT` environment variable, or defaults to `4000`.
 */
if (isMainModule(import.meta.url) || process.env['pm_id']) {
  const port = process.env['PORT'] || 4000;
  app.listen(port, (error) => {
    if (error) {
      throw error;
    }

    console.log(`Node Express server listening on http://localhost:${port}`);
  });
}

/**
 * Request handler for integrating the Angular SSR server with external environments.
 *
 * Can be used by:
 * - Angular CLI dev-server
 * - Firebase Cloud Functions
 *
 * Example usage:
 * ```ts
 * export const handler = reqHandler;
 * ```
 */
export const reqHandler = createNodeRequestHandler(app);
