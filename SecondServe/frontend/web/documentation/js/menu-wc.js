'use strict';

customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">web documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                                <li class="link">
                                    <a href="overview.html" data-type="chapter-link">
                                        <span class="icon ion-ios-keypad"></span>Overview
                                    </a>
                                </li>

                            <li class="link">
                                <a href="index.html" data-type="chapter-link">
                                    <span class="icon ion-ios-paper"></span>
                                        README
                                </a>
                            </li>
                                <li class="link">
                                    <a href="dependencies.html" data-type="chapter-link">
                                        <span class="icon ion-ios-list"></span>Dependencies
                                    </a>
                                </li>
                                <li class="link">
                                    <a href="properties.html" data-type="chapter-link">
                                        <span class="icon ion-ios-apps"></span>Properties
                                    </a>
                                </li>

                    </ul>
                </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#components-links"' :
                            'data-bs-target="#xs-components-links"' }>
                            <span class="icon ion-md-cog"></span>
                            <span>Components</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="components-links"' : 'id="xs-components-links"' }>
                            <li class="link">
                                <a href="components/App.html" data-type="entity-link" >App</a>
                            </li>
                            <li class="link">
                                <a href="components/Blog.html" data-type="entity-link" >Blog</a>
                            </li>
                            <li class="link">
                                <a href="components/Community.html" data-type="entity-link" >Community</a>
                            </li>
                            <li class="link">
                                <a href="components/Contact.html" data-type="entity-link" >Contact</a>
                            </li>
                            <li class="link">
                                <a href="components/Deliveries.html" data-type="entity-link" >Deliveries</a>
                            </li>
                            <li class="link">
                                <a href="components/Donate.html" data-type="entity-link" >Donate</a>
                            </li>
                            <li class="link">
                                <a href="components/DriverAccountManagement.html" data-type="entity-link" >DriverAccountManagement</a>
                            </li>
                            <li class="link">
                                <a href="components/DriverHome.html" data-type="entity-link" >DriverHome</a>
                            </li>
                            <li class="link">
                                <a href="components/DriverOrderHistory.html" data-type="entity-link" >DriverOrderHistory</a>
                            </li>
                            <li class="link">
                                <a href="components/Events.html" data-type="entity-link" >Events</a>
                            </li>
                            <li class="link">
                                <a href="components/Home.html" data-type="entity-link" >Home</a>
                            </li>
                            <li class="link">
                                <a href="components/InventoryManagement.html" data-type="entity-link" >InventoryManagement</a>
                            </li>
                            <li class="link">
                                <a href="components/Landing.html" data-type="entity-link" >Landing</a>
                            </li>
                            <li class="link">
                                <a href="components/Login.html" data-type="entity-link" >Login</a>
                            </li>
                            <li class="link">
                                <a href="components/Mission.html" data-type="entity-link" >Mission</a>
                            </li>
                            <li class="link">
                                <a href="components/OrgAccountManagement.html" data-type="entity-link" >OrgAccountManagement</a>
                            </li>
                            <li class="link">
                                <a href="components/OrgHome.html" data-type="entity-link" >OrgHome</a>
                            </li>
                            <li class="link">
                                <a href="components/OrgOrderHistory.html" data-type="entity-link" >OrgOrderHistory</a>
                            </li>
                            <li class="link">
                                <a href="components/Register.html" data-type="entity-link" >Register</a>
                            </li>
                            <li class="link">
                                <a href="components/Restaurants.html" data-type="entity-link" >Restaurants</a>
                            </li>
                            <li class="link">
                                <a href="components/UserAccountManagement.html" data-type="entity-link" >UserAccountManagement</a>
                            </li>
                            <li class="link">
                                <a href="components/UserHome.html" data-type="entity-link" >UserHome</a>
                            </li>
                            <li class="link">
                                <a href="components/UserOrderHistory.html" data-type="entity-link" >UserOrderHistory</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#injectables-links"' :
                                'data-bs-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/AuthService.html" data-type="entity-link" >AuthService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interfaces-links"' :
                            'data-bs-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/Delivery.html" data-type="entity-link" >Delivery</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Delivery-1.html" data-type="entity-link" >Delivery</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Delivery-2.html" data-type="entity-link" >Delivery</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Delivery-3.html" data-type="entity-link" >Delivery</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/InventoryItem.html" data-type="entity-link" >InventoryItem</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/InventoryItem-1.html" data-type="entity-link" >InventoryItem</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Order.html" data-type="entity-link" >Order</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Order-1.html" data-type="entity-link" >Order</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/OrgOrder.html" data-type="entity-link" >OrgOrder</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/PickupRequest.html" data-type="entity-link" >PickupRequest</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Restaurant.html" data-type="entity-link" >Restaurant</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/User.html" data-type="entity-link" >User</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/User-1.html" data-type="entity-link" >User</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/User-2.html" data-type="entity-link" >User</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#miscellaneous-links"'
                            : 'data-bs-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <a data-type="chapter-link" href="routes.html"><span class="icon ion-ios-git-branch"></span>Routes</a>
                        </li>
                    <li class="chapter">
                        <a data-type="chapter-link" href="coverage.html"><span class="icon ion-ios-stats"></span>Documentation coverage</a>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});