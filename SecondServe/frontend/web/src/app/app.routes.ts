import { Routes } from '@angular/router';
import { Landing } from '../landing/landing';
import { Home } from '../home/home';
import { Login } from '../login/login';
import { Register } from '../register/register';
import { AccountManagement } from '../manage-account/manage-account';
import { OrderHistory } from '../history/history';
import { InventoryManagement } from '../inventory-management/inventory-management';
import { Deliveries } from '../deliveries/deliveries';
import { Donate } from './get-involved/donate/donate';
import { Restaurants } from './find-resources/restaurants/restaurants';
import { Community } from './find-resources/community/community';
import { Events } from './news-media/events/events';
import { Blog } from './news-media/blog/blog';
import { Mission } from './about-us/mission/mission';
import { Contact } from './about-us/contact/contact';

/**
 * Application Routes Configuration
 * 
 * Defines the routing structure for the entire Angular application.
 * Maps URL paths to their corresponding components for navigation.
 * 
 * Route Categories:
 * - Core Application: Landing, authentication, main dashboard
 * - User Management: Account settings, order history
 * - Operations: Inventory, deliveries management
 * - Get Involved: Donation and contribution flows
 * - Resources: Restaurant and community resource directories
 * - News & Media: Events, blog content
 * - About Us: Company information and contact
 * 
 * @constant routes
 * @type {Routes}
 */
export const routes: Routes = [
  // CORE APPLICATION ROUTES
  /** Default route - Landing page shown at application root */
  { path: '', component: Landing },

  /** Main dashboard/home page after authentication */
  { path: 'home', component: Home },
  //{ path: 'user-home', component: UserHome },
  { path: 'org-home', component: OrgHome },
  { path: 'driver-home', component: DriverHome },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'user-account', component: UserAccountManagement },
  { path: 'org-account', component: OrgAccountManagement },
  { path: 'driver-home', component: DriverHome },
  { path: 'driver-account', component: DriverAccountManagement },
  { path: 'user-history', component: UserOrderHistory },
  { path: 'org-history', component: OrgOrderHistory },
  { path: 'driver-history', component: DriverOrderHistory },

  // USER MANAGEMENT ROUTES
  /** User account settings and profile management */
  { path: 'account', component: AccountManagement },

  /** User order history and past transactions */
  { path: 'history', component: OrderHistory },

  // OPERATIONS ROUTES
  /** Inventory management for businesses/organizations */
  { path: 'inventory', component: InventoryManagement },

  /** Delivery tracking and management system */
  { path: 'deliveries', component: Deliveries },

  // GET INVOLVED ROUTES
  /** Donation portal for contributors and supporters */
  { path: 'donate', component: Donate },

  // RESOURCE DIRECTORY ROUTES
  /** Restaurant directory and food resource listings */
  { path: 'restaurants', component: Restaurants },

  /** Community resources and local organization directory */
  { path: 'community', component: Community },

  // NEWS & MEDIA ROUTES
  /** Events calendar and upcoming community events */
  { path: 'events', component: Events },

  /** Blog articles and news updates */
  { path: 'blog', component: Blog },

  // ABOUT US ROUTES
  /** Company mission, vision, and values information */
  { path: 'mission', component: Mission },

  /** Contact form and company contact information */
  { path: 'contact', component: Contact }
];