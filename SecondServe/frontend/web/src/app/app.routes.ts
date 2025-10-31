import { Routes } from '@angular/router';
import { Landing } from '../landing/landing';
import { UserHome } from '../user-home/user-home';
import { OrgHome } from '../org-home/org-home';
import { DriverHome } from '../driver-home/driver-home';
import { Login } from '../login/login';
import { Register } from '../register/register';
import { AccountManagement } from '../manage-account/manage-account';
import { UserOrderHistory } from '../user-order-history/user-order-history';
import { OrgOrderHistory } from '../org-order-history/org-order-history';
import { DriverOrderHistory } from '../driver-order-history/driver-order-history';

export const routes: Routes = [
  { path: '', component: Landing },
  { path: 'user-home', component: UserHome },
  { path: 'org-home', component: OrgHome },
  { path: 'driver-home', component: DriverHome },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'account', component: AccountManagement },
  { path: 'user-history', component: UserOrderHistory },
  { path: 'org-history', component: OrgOrderHistory },
  { path: 'driver-history', component: DriverOrderHistory },
];
