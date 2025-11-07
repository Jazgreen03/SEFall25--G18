import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Router } from '@angular/router';

/**
 * Blog Component
 * 
 * Displays the blog section featuring articles, news updates, and educational content.
 * This component serves as a container for blog-related content and provides routing capabilities
 * for navigation within the blog section.
 * 
 * Features:
 * - Standalone component architecture
 * - Router integration for internal navigation
 * - External template and styling for maintainability
 * - Common module for basic Angular directives
 * 
 * @selector app-blog
 * @standalone true
 * 
 * @usage
 * This component is rendered when navigating to the '/blog' route and typically displays:
 * - Blog post listings with excerpts
 * - Article categories and tags
 * - Featured content highlights
 * - Author information and publication dates
 * - Pagination for blog post navigation
 */
@Component({
  selector: 'app-blog',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './blog.html',
  styleUrl: './blog.css',
})
export class Blog {
  /**
   * Blog Component
   * 
   * This component serves as the main container for the blog functionality.
   * The actual presentation logic, including blog post display, filtering,
   * and navigation is handled in the associated template and style files.
   * 
   * Future enhancements may include:
   * - Blog post filtering by category or tags
   * - Search functionality within blog content
   * - Featured post highlighting
   * - Social sharing capabilities
   * - Comment system integration
   * - Author profile displays
   * - Related posts suggestions
   * 
   * The component's visual design and layout are defined in blog.css,
   * while the structure and content presentation are handled in blog.html.
   */
  constructor(
    private router: Router,
  ) { }
  goToHome(): void {
    this.router.navigate(['/']);
  }
}