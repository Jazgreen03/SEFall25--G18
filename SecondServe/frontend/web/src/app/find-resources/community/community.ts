import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

/**
 * Community Component
 * 
 * Displays the community resources directory and local organization listings.
 * This component provides users with access to community organizations, support services,
 * and local initiatives. It serves as a hub for discovering and connecting with
 * community resources and support networks.
 * 
 * Features:
 * - Standalone component architecture
 * - Router integration for organization detail navigation
 * - Community resource search and categorization
 * - Organization profiles and service information
 * - Location-based community resource discovery
 * 
 * @selector app-community
 * @standalone true
 * 
 * @usage
 * This component is rendered when navigating to the '/community' route and typically includes:
 * - Community organization directory with search and filters
 * - Resource categorization (food banks, shelters, healthcare, education, etc.)
 * - Organization profiles with contact information and services offered
 * - Location-based resource mapping
 * - Operating hours and availability status
 * - Volunteer opportunities and support needs
 */
@Component({
  selector: 'app-community',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './community.html',
  styleUrl: './community.css',
})
export class Community {
  /**
   * Community Component
   * 
   * This component serves as the central interface for discovering and accessing
   * community resources and local organizations. The actual implementation of
   * organization listings, search functionality, and resource categorization
   * are handled in the associated template and style files.
   * 
   * Potential future enhancements may include:
   * - Advanced filtering by service type, eligibility requirements, or location
   * - Real-time availability and capacity indicators
   * - Interactive map view of community resources
   * - Resource booking or appointment scheduling
   * - User reviews and feedback for organizations
   * - Volunteer sign-up and shift management
   * - Community event integration with organization calendars
   * - Multilingual resource information
   * - Accessibility information for physical locations
   * - Emergency service indicators and crisis resources
   * - Community need alerts and urgent requests
   * 
   * The component's responsive design and user-friendly interface are defined in community.css,
   * while the resource listing structure and navigation elements are handled in community.html.
   * RouterModule integration enables seamless navigation to detailed organization profiles
   * and related community services.
   */
}