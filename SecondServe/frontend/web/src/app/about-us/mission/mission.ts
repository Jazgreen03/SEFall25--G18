import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

/**
 * Mission Component
 * 
 * Displays the organization's mission, vision, values, and overall purpose.
 * This component serves as an informational page that communicates the core
 * principles, goals, and philosophical foundation of the platform to users,
 * partners, and stakeholders.
 * 
 * Features:
 * - Standalone component architecture
 * - Router integration for seamless navigation within About Us section
 * - Engaging presentation of organizational philosophy
 * - Responsive design for optimal viewing across devices
 * 
 * @selector app-mission
 * @standalone true
 * 
 * @usage
 * This component is rendered when navigating to the '/mission' route and typically includes:
 * - Organization mission statement and core purpose
 * - Vision for the future and long-term goals
 * - Core values and guiding principles
 * - Impact metrics and success stories
 * - Team information and organizational structure
 * - Historical background and founding story
 */
@Component({
  selector: 'app-mission',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './mission.html',
  styleUrl: './mission.css',
})
export class Mission {
  /**
   * Mission Component
   * 
   * This component presents the foundational principles and purpose of the organization.
   * It serves to inspire trust, communicate values, and align users with the platform's
   * overarching goals. The content typically focuses on:
   * 
   * - The "why" behind the platform's existence
   * - The problem being solved or need being addressed
   * - The intended impact on the community or industry
   * - The ethical framework guiding decision-making
   * 
   * Potential content sections may include:
   * - Founding story and historical context
   * - Core mission statement and value proposition
   * - Vision for future growth and community impact
   * - Team member profiles and organizational culture
   * - Key milestones and achievement highlights
   * - Testimonials from community members or partners
   * - Call-to-action for involvement or support
   * 
   * The component's inspirational design and typographic hierarchy are defined in mission.css,
   * while the narrative structure and content presentation are handled in mission.html.
   * RouterModule integration allows for easy navigation to related About Us pages such as
   * Contact information or team details.
   */
}