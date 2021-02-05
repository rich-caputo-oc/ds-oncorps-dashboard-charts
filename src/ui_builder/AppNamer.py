import os
import jsbeautifier

class AppNamer():

    def __init__(self, name='Generic Dashboard'):
        self.name = name

    def build_pages(self, path):
        """ Ensures app name perpetuates UI code. """
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        opts.max_preserve_newlines = 30

        index_html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title>{self.name}</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <app-root></app-root>
</body>
</html>
        """
        login_html = f"""
<div class="login">

  <p><img src="../assets/images/ey-logo-beam-tag-h.svg" width="150"></p>

  <h1 class="app-title">{self.name}<span>Dashboard</span></h1>

  <button mat-raised-button color="primary" (click)="login()">Login</button>

</div>
        """
        header_ts = """
        import { Component, HostListener, Input, OnInit } from '@angular/core';
        import { Event as NavigationEvent, NavigationEnd, Router } from '@angular/router';
        import { StorageKeys } from 'src/app/enums/storageKeys.enum';
        import { AuthService } from '../../../core/auth/auth.service';

        @Component({
          selector: 'app-header',
          templateUrl: './header.component.html',
          styleUrls: ['./header.component.scss']
        })

        export class HeaderComponent implements OnInit {
          @Input() sideNavEvent: any;
          """
        header_ts += f"""
        public title = '{self.name}';
        """
        header_ts += """
          public redirectUrl = '';
          public headerOptions = [{
            url: '/dashboard',
            title: 'Dashboard',
            redirectUrl: '/dashboard'
          }];
          public isScrolled: Boolean = false;

          constructor(private auth: AuthService, private router: Router) { }

          /**
           * Invoked the auth logout method
           */
          public logout() {
            this.auth.logout();
          }

          /**
           * Gets the username for the header from local storage
           *
           * @returns a string representing the users username
           */
          public getUsername() {
            const { userName } = JSON.parse(localStorage.getItem(StorageKeys.USER_DATA));

            return userName;
          }

          /**
           * Toggles the material side nav component and dispatces a resize event for Plotly to understand when to redraw the charts
           */
          public toggleSideNav() {
            window.dispatchEvent(new Event('resize'));
            this.sideNavEvent.toggle();
          }

          /**
           * Determines if a user is authenticated via the auth service
           *
           * @returns true if the user is authenticated
           */
          public userIsAuthenticated() {
            return this.auth.isAuthenticated();
          }

          /**
           * Listens for a scroll event to be emitted by the window object and sets the isScrolled property
           */
          @HostListener('window:scroll', [])
          onWindowScroll() {
            const verticalOffset =
              window.pageYOffset ||
              document.documentElement.scrollTop ||
              document.body.scrollTop ||
              0;

            this.isScrolled = verticalOffset > 0;
          }

          /**
           * Sets the title on the header
           *
           * @param data Data represents the header config
           */
          private setTitle(data: any) {
            this.title = data ? data.title : this.title;
          }

          /**
           * Sets the redirectUrl
           *
           * @param data Data represents the header config
           */
          private setRedirectUrl(data: any) {
            this.redirectUrl = data ? data.redirectUrl : this.redirectUrl;
          }

          /**
           * A method that gets invoked when the component comes into view
           */
          ngOnInit() {
            this.router.events.subscribe((event: NavigationEvent) => {
              if (event instanceof NavigationEnd) {
                const data = this.headerOptions.find(item => event.urlAfterRedirects.includes(item.url));
                this.setTitle(data);
                this.setRedirectUrl(data);
              }
            });
          }
        }
        """
        readme = f"""
# {self.name}

This is the Angular frontend for any stand alone dashboard apps (typically works with one or more python flask apps that serve APIs returning plotly.js configurations).


## Installation

To ensure a consistent dev environment please use the supplied Docker container.

Firstly ensure you have latest version of [Docker](https://docs.docker.com/install/)

In Terminal navigate to this folder

Run `docker-compose build`

When complete run `docker-compose up -d`

Then run bash from new container with `docker-compose exec angular bash`

Finally install project dependancies in the container by running `npm install`

**IMPORTANT**

Regularly run `npm install` via the container to ensure your project is using the correct dependencies

## Development server

Run `npm start`. Navigate to `http://localhost:4200/`.
The app will automatically reload if  you change any of the source files.


## Code scaffolding

Run `ng generate component component-name` to generate a new component.
You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.


## Build

Run `npm build` to build the project. The build artifacts will be stored in the `dist/` directory.
Use the `--prod` flag for a production build.

To build for specific environments use the appropriate commands below:

`ng build --configuration="dev"`

`ng build --configuration="stage"`

`ng build --configuration="prod"`


## Running unit tests

Run `npm test` to execute the unit tests via [Karma](https://karma-runner.github.io).


## Running end-to-end tests

Run `npm e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).


## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
        """

        with open(f"{path}/src/index.html", 'w') as index_html_file:
            index_html_file.write(index_html)

        with open(f"{path}/src/app/modules/login/pages/login.component.html", 'w') as login_html_file:
            login_html_file.write(login_html)

        with open(f"{path}/src/app/shared/components/header/header.component.ts", 'w') as header_ts_file:
            header_ts_file.write(jsbeautifier.beautify(header_ts, opts))

        with open(f"{path}/README.md", 'w') as readme_file:
            readme_file.write(readme)
