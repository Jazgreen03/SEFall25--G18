import { Routes } from '@angular/router';
import { Landing } from '../landing/landing';
import { UserHome } from '../user-home/user-home';
import { OrgHome } from '../org-home/org-home';
import { DriverHome } from '../driver-home/driver-home';
import { Login } from '../login/login';
import { Register } from '../register/register';
import { AccountManagement } from '../manage-account/manage-account'
import { OrderHistory } from '../order-history/order-history';

export const routes: Routes = [
    { path: '', component: Landing },
    { path: 'user-home', component: UserHome },
    { path: 'org-home', component: OrgHome },
    { path: 'driver-home', component: DriverHome },
    { path: 'login', component: Login },
    { path: 'register', component: Register },
    { path: 'account', component: AccountManagement },
    { path: 'history', component: OrderHistory }
];
