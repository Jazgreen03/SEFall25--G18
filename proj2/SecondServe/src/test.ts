/***************************************************************************************************
 * Zone.js and Angular testing setup
 **************************************************************************************************/
import 'zone.js'; // Required by Angular
import 'zone.js/testing'; // Required for Angular testing utilities

import { getTestBed } from '@angular/core/testing';
import {
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting,
} from '@angular/platform-browser-dynamic/testing';

// Initialize the Angular testing environment
getTestBed().initTestEnvironment(BrowserDynamicTestingModule, platformBrowserDynamicTesting());
